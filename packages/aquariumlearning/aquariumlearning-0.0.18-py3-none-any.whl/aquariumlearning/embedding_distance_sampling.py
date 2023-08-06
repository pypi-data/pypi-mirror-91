import random
from pprint import pprint
from typing import Any, Optional, Union, List, Dict, Tuple
from .sampling_agent import SamplingAgent
from .dataset import LabeledDataset, LabeledFrame

from google.cloud import storage
from google.cloud.storage.blob import Blob
import joblib
import json
from annoy import AnnoyIndex
import numpy as np
from sklearn.preprocessing import normalize


# TODO: Add pip dependencies for client
# TODO: How do we know if it's a frame issue vs a crop issue?
# Currently just only working with frame data.
# TODO: Pass these in more properly
# ANN_GSPATH = "gs://tsne_embeddings/2020-12-22T14:21:11Z/nuimages_geo_all4.singapore_onenorth_val_0.frame_index.ann"
# HDBSCAN_GSPATH = "gs://tsne_embeddings/2020-12-22T14:21:11Z/nuimages_geo_all4.singapore_onenorth_val_0.frame_clusterer.joblib"
# PCA_GSPATH = "gs://tsne_embeddings/2020-12-22T14:21:11Z/nuimages_geo_all4.singapore_onenorth_val_0.frame_pca.joblib"

# ANN_FILEPATH = "/home/quinn/embdata/annoy.ann"
# HDBSCAN_FILEPATH = "/home/quinn/embdata/hdbscan.joblib"
# PCA_FILEPATH = "/home/quinn/embdata/pca.joblib"
# FRAME_IDS_FILEPATH = "/home/quinn/embdata/ordered_frame_ids.json"

PCA_CLUSTERING_DIM = 64
ANNOY_METRIC = "euclidean"

# TODO: Should we also keep track of exactly which ids were used to generate the clusterer tree?


class EmbeddingDistanceSamplingAgent(SamplingAgent):
    def __init__(self, random_seed=None):
        self.random_seed = random_seed

        self.ann = AnnoyIndex(PCA_CLUSTERING_DIM, ANNOY_METRIC)
        # self.ann.load(ANN_FILEPATH)
        self.clusterer = None  # joblib.load(HDBSCAN_FILEPATH)
        self.pca = None  # joblib.load(PCA_FILEPATH)
        self.ordered_element_ids = None
        # with open(FRAME_IDS_FILEPATH, "r") as f:
        #     self.ordered_element_ids = json.load(f)

        self.issue_id_str_set = set()
        self.issue_id_int_set = set()

    def load_sampling_dataset(
        self, data: List[Any], preprocessed_info: Dict[str, Any] = None
    ) -> None:
        self.ann.load(preprocessed_info["ann_path"])
        self.clusterer = joblib.load(preprocessed_info["hdbscan_path"])
        self.pca = joblib.load(preprocessed_info["pca_path"])
        with open(preprocessed_info["dataset_ordered_id_path"], "r") as f:
            self.ordered_element_ids = json.load(f)

        self.training_data = data
        for entry in data:
            self.issue_id_str_set.add(entry["element_id"])

        # Convert string ids to int ids
        for idx, str_id in enumerate(self.ordered_element_ids):
            if str_id in self.issue_id_str_set:
                self.issue_id_int_set.add(idx)

        # Get 64 dim embeddings for all elements
        el_embs = []
        for idx in self.issue_id_int_set:
            el_embs.append(self.ann.get_item_vector(idx))

        # Identify nearest equivalents to each in the clustering.
        # TODO: This is if we're looking for a set of things that
        # has any representation at all in the clustering.
        #
        # If we don't see anything close (how do we define this?)
        # how do we want to treat searching for it as an outlier?

        raw_data = self.clusterer.prediction_data_.raw_data
        slt_df = self.clusterer.single_linkage_tree_.to_pandas()

        # TODO: Can this be more dynamically set?
        CORE_SIZE = 16
        (
            distances_lists,
            nearest_indices_lists,
        ) = self.clusterer.prediction_data_.tree.query(el_embs, k=CORE_SIZE)
        nearest_indices = [x[0] for x in nearest_indices_lists]

        # We have to recompute core distances because min samples may be set lower during
        # initial clustering vs what we want here (such as to 1)
        # TODO: Should we keep it higher during initial clustering / linkage computing?

        core_distances = [x[-1] for x in distances_lists]
        # core_distances = [self.clusterer.prediction_data_.core_distances[i] for i in nearest_indices]
        zipped = zip(core_distances, nearest_indices)

        # At this point, our goal is to identify redundant points, and reduce the
        # problem to checking distance from K target points.

        # An equivalent framing of this is that we want to cluster the input points
        # together given the ~global linkage tree, and the additional information that
        # these input points represent relatively few sub-clusters, while also capturing
        # the ideal range that should match each cluster (which may be larger than)
        # the examples from the issue.
        #
        # This lets us inform what the optimal "cuts" are of the tree, vs arbitrary
        # density/stability based metrics used by hdbscan.

        # Proposed v0 approach, which doesn't use the linkage info:
        #
        # Start by having 0 microclusters
        # For each included element:
        #   For each existing microcluster:
        #       If it would be included in said cluster:
        #           Add it
        #           Adjust range of microcluster
        #           Break
        #   Create a new microcluster
        #   Initialize range based on local distances, as estimated by the single linkage tree.
        #

        microclusters = []
        microcluster_centroids = []

        radii = []
        seen = set()

        for core_dist, idx in zipped:
            # Skip dupes
            if idx in seen:
                continue
            seen.add(idx)

            vec = np.array(raw_data[idx])

            # Check if it should be merged into an existing microcluster
            # We don't care about merging *all*, because ultimately this is an optimization to reduce checks,
            # vs actually having to have informative single flat clusters.
            found = False
            for j in range(len(microclusters)):
                centroid = microcluster_centroids[j]
                dist = np.linalg.norm(vec - centroid)
                if dist < radii[j]:
                    # TODO: Incremental update vs recomputing.
                    microclusters[j].append(idx)
                    points = [raw_data[n] for n in microclusters[j]]
                    centroid = np.mean(points, axis=0)
                    microcluster_centroids[j] = centroid

                    max_delta = -1000000.0
                    for dim_i in range(PCA_CLUSTERING_DIM):
                        minval = min([v[dim_i] for v in points])
                        maxval = max([v[dim_i] for v in points])
                        delta = maxval - minval
                        if delta > max_delta:
                            max_delta = delta

                    if max_delta > radii[j]:
                        radii[j] = max_delta

                    # Hit, mark as found and update centroid
                    found = True
                    break

            if found:
                continue

            # Initialize a new microcluster.
            # Pick an initial radius based on the 5th nearest neighbor.
            # Pick a radius based on linkage tree, goal is to capture "local density"
            # to understand the distance that should be considered "similar"

            microclusters.append([idx])
            microcluster_centroids.append(vec)
            radius = 1.0 * core_dist
            radii.append(radius)

        self.microclusters = microclusters
        self.microcluster_centroids = microcluster_centroids
        self.microcluster_radii = radii

    def score_frame(self, frame: LabeledFrame) -> float:
        if not frame.embedding:
            raise Exception(
                "Frames for embedding distance sampling must have embeddings."
            )

        if not frame.embedding.get("embedding"):
            raise Exception(
                "Frames for embedding distance sampling must have a valid, non-empty embedding."
            )

        raw_emb = frame.embedding.get("embedding")
        wrapped = np.array([raw_emb])
        normalized = normalize(wrapped)
        vec = self.pca.transform(normalized)[0]

        for j in range(len(self.microclusters)):
            target_centroid = self.microcluster_centroids[j]
            dist = np.linalg.norm(vec - target_centroid)
            if dist < self.microcluster_radii[j]:
                return 1.0

        return 0.0
