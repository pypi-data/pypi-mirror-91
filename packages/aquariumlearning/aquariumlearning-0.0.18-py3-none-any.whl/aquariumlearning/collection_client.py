"""collection_client.py
============
The extended client module for collection campaigns.
"""

import os
import datetime
from random import random
import time
import uuid
import json
from uuid import uuid4
from io import IOBase
from tempfile import NamedTemporaryFile
from google.resumable_media.requests import ChunkedDownload
from google.resumable_media.common import InvalidResponse, DataCorruption
from typing import Any, Callable, Optional, Union, List, Dict, Tuple, Callable

from requests.adapters import prepend_scheme_if_needed

from .util import (
    requests_retry,
    raise_resp_exception_error,
    _is_one_gb_available,
    TEMP_FILE_PATH,
    MAX_CHUNK_SIZE,
)
from .client import Client
from .dataset import LabeledDataset, LabeledFrame
from .inference import Inferences, InferencesFrame
from .sampling_agent import RandomSamplingAgent

# from .embedding_distance_sampling import EmbeddingDistanceSamplingAgent


class CollectionClient(Client):
    """Client class that interacts with the Aquarium REST API.
    Also handles extra work around collecting samples for collection campigns

    Args:
        api_endpoint (str, optional): The API endpoint to hit. Defaults to "https://illume.aquariumlearning.com/api/v1".
    """

    def __init__(self, *args, **kwargs) -> "CollectionClient":
        super().__init__(*args, **kwargs)
        self.active_coll_camp_summaries = []
        self.camp_ids = []
        self.issue_uuids = []
        self.camp_id_to_campaign_details = {}

        # self.sampling_agent = EmbeddingDistanceSamplingAgent
        self.sampling_agent = RandomSamplingAgent
        self.camp_id_to_sample_agent = {}

        self.camp_id_to_example_frame_filepath = {}
        self.camp_id_to_unique_dataset_and_inference_set = {}
        self.dataset_name_to_preprocessed_filepath = {}
        self.inference_set_name_to_preprocessed_filepath = {}

        self.frame_batch_uuid_to_temp_file_path = {}
        self.frame_batch_uuid_to_camp_id_to_probability_score = {}

    def _save_content_to_temp(
        self, file_name_prefix: str, writefunc: Callable, mode: str = "w"
    ) -> Optional[str]:
        """saves whatever the write function wants to a temp file and returns the file path

        Args:
            file_name_prefix (str): prefix for the filename being saved
            writefunc ([filelike): function used to write data to the file opened

        Returns:
            str or None: path of file or none if nothing written
        """

        if not _is_one_gb_available():
            raise OSError(
                "Attempting to flush dataset to disk with less than 1 GB of available disk space. Exiting..."
            )

        data_rows_content = NamedTemporaryFile(
            mode=mode, delete=False, prefix=file_name_prefix, dir=TEMP_FILE_PATH
        )
        data_rows_content_path = data_rows_content.name
        writefunc(data_rows_content)

        # Nothing was written, return None
        if data_rows_content.tell() == 0:
            return None

        data_rows_content.seek(0)
        data_rows_content.close()
        return data_rows_content_path

    def write_to_file(self, frames: List[Dict[str, any]], filelike: IOBase) -> None:
        """Write the frame content to a text filelike object (File handle, StringIO, etc.)

        Args:
            filelike (filelike): The destination file-like to write to.
        """
        for frame in frames:
            filelike.write(json.dumps(frame) + "\n")

    def download_to_file(self, signed_url: str, filelike: IOBase) -> None:
        xml_api_headers = {
            "content-type": "application/octet-stream",
        }
        download = ChunkedDownload(signed_url, MAX_CHUNK_SIZE, filelike)
        while not download.finished:
            try:
                download.consume_next_chunk(requests_retry)
            except (InvalidResponse, DataCorruption, ConnectionError):
                if download.invalid:
                    continue
                continue

    def _read_rows_from_disk(self, file_path: str) -> List[Dict[str, Any]]:
        """reads temp files from disk and loads the dicts in them into memory

        Args:
            file_path (str): file path to read from

        Returns:
            List[Dict[str, Any]]: List of LabeledFrames in a dict structure
        """
        with open(file_path, "r") as frame_file:
            return [json.loads(line.strip()) for line in frame_file.readlines()]

    def _get_all_campaigns(self) -> List[Dict[str, Any]]:
        """Gets all collection campaign summaries

        Returns:
            List[Dict[str, Any]]: List of dicts containing collection campaign summaries
        """
        r = requests_retry.get(
            self.api_endpoint + "/collection_campaigns/summaries",
            headers=self._get_creds_headers(),
        )

        raise_resp_exception_error(r)
        return r.json()

    def _get_issue_for_campaign(self, issue_uuid: str) -> Dict[str, Any]:
        """Gets the detailed collection campaign information given an issue id

        Args:
            issue_uuid (str): Issue UUID associated with a collection campaign

        Returns:
            Dict[str, Any]: returns a Dict of all the Collection Campaign detailed info including sample frames
        """
        r = requests_retry.get(
            self.api_endpoint + "/collection_campaigns/for_issue/" + issue_uuid,
            headers=self._get_creds_headers(),
        )

        raise_resp_exception_error(r)
        return r.json()

    def _get_elt_data_from_gcs(
        self, signed_url: str, format_version: int
    ) -> List[Dict[str, Any]]:
        """Gets all cached issue element info associated with a campaign

        Returns:
            List[Dict[str, Any]]: List of dicts containing issue element info
        """
        r = requests_retry.get(signed_url)

        raise_resp_exception_error(r)
        return [json.loads(row.decode()) for row in r.iter_lines()]

    def _get_preprocessed_collection_signed_urls(
        self, project_id: str, dataset_id: str, category: str
    ) -> Dict[str, str]:
        """[summary]

        Args:
            project_id (str): name of project associated with dataset
            dataset_id (str): name of dataset id (can include inferences)
            category (str): name of cateogory, either frames or crops only

        Returns:
            Dict[str, str]: links to urls and signed downloads
        """
        r = requests_retry.get(
            self.api_endpoint
            + f"/projects/{project_id}/datasets/{dataset_id}/get_signed_collection_postprocessed_urls",
            params={"category": category},
            headers=self._get_creds_headers(),
        )

        raise_resp_exception_error(r)
        return r.json()

    def _post_collection_frames(self, collection_frames: Dict[str, Any]) -> None:
        """takes frames for collection and posts it to the API

        Args:
            collection_frames (Dict[str, Any]): Dict structure containing all the collected frames for a campaign to post
        """
        r = requests_retry.post(
            self.api_endpoint + "/projects/blah/collection_frames",
            headers=self._get_creds_headers(),
            json=collection_frames,
        )

        raise_resp_exception_error(r)

    def sync_state(self) -> None:
        """Downloads all collection campaigns and preps sampler with sample frames"""
        print("Starting Sync")
        all_coll_camps = self._get_all_campaigns()
        self.active_coll_camp_summaries = [
            x for x in filter(lambda camp: camp["active"], all_coll_camps)
        ]

        print(
            f"Found {len(self.active_coll_camp_summaries)} Active Collection Campaigns"
        )
        self.camp_ids = [camp["id"] for camp in self.active_coll_camp_summaries]
        self.issue_uuids = [
            camp["issue_uuid"] for camp in self.active_coll_camp_summaries
        ]
        self.camp_id_to_campaign_details = {
            camp_id: self._get_issue_for_campaign(issue_uuid)
            for camp_id, issue_uuid in zip(self.camp_ids, self.issue_uuids)
        }

        print(
            f"Got {len(self.camp_id_to_campaign_details)} Collection Campaign Details"
        )
        self.camp_id_to_sample_agent = {
            camp_id: self.sampling_agent() for camp_id in self.camp_ids
        }

        print(f"Getting sampling dataset for each Collection Campaign")
        for camp_id, camp_details in self.camp_id_to_campaign_details.items():

            # download frame data to a file
            frame_data_signed_url = camp_details["cached_elt_data_signed_url"]

            current_time = datetime.datetime.now()
            random_uuid = uuid4().hex
            temp_frame_prefix = "al_{}_collection_campaign_example_frames_{}_{}".format(
                current_time.strftime("%Y%m%d_%H%M%S_%f"), str(camp_id), random_uuid
            )
            frame_path = self._save_content_to_temp(
                temp_frame_prefix,
                lambda x: self.download_to_file(frame_data_signed_url, x),
                mode="wb",
            )
            self.camp_id_to_example_frame_filepath[camp_id] = frame_path

            # read first element from frame file to get information around dataset, project, and categoru
            example_frame = self._read_rows_from_disk(frame_path)[0]
            full_set_name = example_frame["dataset_name"]
            if example_frame["inference_set_name"]:
                full_set_name = example_frame["inference_set_name"]
            category = "frames"
            if example_frame["frame_id"] != example_frame["element_id"]:
                category = "crops"
            project = full_set_name.split(".")[0]
            set_name = full_set_name.split(".")[1]

            # download each of the preprocessed files for the example dataset locally
            signed_urls = self._get_preprocessed_collection_signed_urls(
                project, set_name, category
            )
            url_key_to_downloaded_file_path = {}
            for url_key, signed_url in signed_urls.items():
                if signed_url is None:
                    url_key_to_downloaded_file_path[url_key] = None
                    continue
                current_time = datetime.datetime.now()
                random_uuid = uuid4().hex
                temp_file_prefix = "al_{}_{}_{}_{}".format(
                    current_time.strftime("%Y%m%d_%H%M%S_%f"),
                    str(camp_id),
                    url_key,
                    random_uuid,
                )
                file_path = self._save_content_to_temp(
                    temp_file_prefix,
                    lambda x: self.download_to_file(signed_url, x),
                    mode="wb",
                )
                url_key_to_downloaded_file_path[url_key] = file_path

            path_key_to_downloaded_file_path = {
                k[:-3] + "path": v for k, v in url_key_to_downloaded_file_path.items()
            }

            # load data into agent for each campaign
            agent = self.camp_id_to_sample_agent[camp_id]
            agent.load_sampling_dataset(
                data=self._read_rows_from_disk(frame_path),
                preprocessed_info=path_key_to_downloaded_file_path,
            )

        # print(f"Identifying unique dataset and inference set IDs across all campaigns")
        # for (
        #     camp_id,
        #     example_frame_file_path,
        # ) in self.camp_id_to_example_frame_filepath.items():
        #     example_frames = self._read_rows_from_disk(example_frame_file_path)
        #     dataset_names = [frame["dataset_name"] for frame in example_frames]
        #     inference_set_names = [
        #         frame["inference_set_name"] for frame in example_frames
        #     ]
        #     self.camp_id_to_unique_dataset_and_inference_set[camp_id] = {}
        #     self.camp_id_to_unique_dataset_and_inference_set[camp_id][
        #         "dataset_names"
        #     ] = set(dataset_names)
        #     self.camp_id_to_unique_dataset_and_inference_set[camp_id][
        #         "inference_set_names"
        #     ] = set(inference_set_names)

        # all_unique_dataset_names = set().union(
        #     *[
        #         sets["dataset_names"]
        #         for sets in self.camp_id_to_unique_dataset_and_inference_set.values()
        #     ]
        # )
        # all_unique_inference_set_names = set().union(
        #     *[
        #         sets["inference_set_names"]
        #         for sets in self.camp_id_to_unique_dataset_and_inference_set.values()
        #     ]
        # )

        # temp_preprocessing_prefix = "al_{}_collection_campaign_dataset_tree_{}_{}".format(
        #     current_time.strftime("%Y%m%d_%H%M%S_%f"), str(camp_id), random_uuid
        # )
        # agent.load_sampling_dataset(camp_details["elt_frame_data"])

    def sample_probabilities(self, frames: List[LabeledFrame]) -> None:
        """Takes a list of Labeled Frames and stores scores for each based on each synced collection campaigns

        Args:
            frames (List[LabeledFrame]): a List of Labeled frames to score based on synced Collection Campaigns
        """
        # print(
        #     f"Sampling Similarity Probabilities for {len(frames)} frames across {len(self.camp_ids)} Collection Campaigns"
        # )
        batch_uuid = uuid4().hex
        self.frame_batch_uuid_to_camp_id_to_probability_score[batch_uuid] = {
            camp_id: [
                self.camp_id_to_sample_agent[camp_id].score_frame(frame)
                for frame in frames
            ]
            for camp_id in self.camp_ids
        }
        current_time = datetime.datetime.now()
        temp_frame_prefix = "al_{}_collection_campaign_candidate_frames_{}_".format(
            current_time.strftime("%Y%m%d_%H%M%S_%f"), batch_uuid
        )
        frame_path = self._save_content_to_temp(
            temp_frame_prefix,
            lambda x: self.write_to_file([frame.to_dict() for frame in frames], x),
        )
        self.frame_batch_uuid_to_temp_file_path[batch_uuid] = frame_path
        return self.frame_batch_uuid_to_camp_id_to_probability_score[batch_uuid]

    def save_for_collection(self, score_threshold: float = 0.7) -> None:
        """Based on the score threshold, take all sampled frames and upload those that score above
        the score threshold for each Collection Campaign.

        Args:
            score_threshold (float, optional): Score threshold for all campaigns to save to server. Defaults to 0.7.
        """
        for frame_batch_uuid in self.frame_batch_uuid_to_temp_file_path.keys():
            frames = self._read_rows_from_disk(
                self.frame_batch_uuid_to_temp_file_path[frame_batch_uuid]
            )
            camp_id_to_probability_score = (
                self.frame_batch_uuid_to_camp_id_to_probability_score[frame_batch_uuid]
            )
            for camp_id, camp_details in self.camp_id_to_campaign_details.items():
                scores = camp_id_to_probability_score[camp_id]
                filtered_frame_indexes_and_scores = filter(
                    lambda score: score[1] >= score_threshold, enumerate(scores)
                )
                filtered_frame_indexes = map(
                    lambda score: score[0], filtered_frame_indexes_and_scores
                )
                filtered_frames_dict = []
                for idx in filtered_frame_indexes:
                    frame_dict = frames[idx]
                    frame_dict["sampling_probability"] = scores[idx]
                    filtered_frames_dict.append(frame_dict)

                if len(filtered_frames_dict) == 0:
                    continue

                print(f"Uploading Frames for Collection Campaign ID {camp_id}")

                payload = {
                    "collection_campaign_id": camp_id,
                    "issue_uuid": camp_details["issue_uuid"],
                    "dataframes": filtered_frames_dict,
                }
                self._post_collection_frames(payload)
