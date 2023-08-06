from os import environ
from pathlib import Path
from shutil import rmtree

from dkist_processing_common._util.data import input_dataset
from dkist_processing_common._util.data import publish_messages
from dkist_processing_common._util.globus import submit_globus_transfer
from dkist_processing_common._util.graphql import DatasetCatalogReceiptAccountMutation
from dkist_processing_common._util.graphql import graph_ql_client
from dkist_processing_common.base import SupportTaskBase


class TransferInputData(SupportTaskBase):
    def run(self) -> None:
        self.change_status_to_in_progress()

        bucket = input_dataset(section="bucket", recipe_run_id=self.recipe_run_id)
        frames = input_dataset(section="frames", recipe_run_id=self.recipe_run_id)

        source_files = [Path("/", bucket, frame) for frame in frames]
        destination_files = [
            Path("/", self.recipe_run_id, "/input/", frame.split("/"[-1])) for frame in frames
        ]

        submit_globus_transfer(
            source_files=source_files,
            destination_files=destination_files,
            source_endpoint=environ.get("DTN_ENDPOINT"),
            destination_endpoint=environ.get("SCRATCH_ENDPOINT"),
        )


class TransferOutputData(SupportTaskBase):
    def run(self) -> None:
        destination_files = [
            Path("/data", self.proposal_id, self.dataset_id, filepath.parts[-1])
            for filepath in self.output_filepaths
        ]

        submit_globus_transfer(
            source_files=self.output_filepaths,
            destination_files=destination_files,
            source_endpoint=environ["SCRATCH_ENDPOINT"],
            destination_endpoint=environ["DTN_ENDPOINT"],
        )


class AddDatasetReceiptAccount(SupportTaskBase):
    def run(self) -> None:
        expected_object_count = len(self.output_filepaths)
        graph_ql_client.execute_gql_mutation(
            mutation_base="createDatasetCatalogReceiptAccount",
            mutation_parameters=DatasetCatalogReceiptAccountMutation(
                datasetId=self.dataset_id, expectedObjectCount=expected_object_count
            ),
        )


class PublishCatalogMessages(SupportTaskBase):
    def run(self) -> None:
        destination_files = [
            Path("/data", self.proposal_id, self.dataset_id, filepath.parts[-1])
            for filepath in self.output_filepaths
        ]
        object_filepaths = [str(file[file.find(self.proposal_id) :]) for file in destination_files]
        messages = []
        for filepath in object_filepaths:
            if filepath.lower().endswith(".fits"):
                messages.append(self.create_frame_message(object_filepath=filepath))
            elif filepath.lower().endswith(".mp4"):
                messages.append(self.create_movie_message(object_filepath=filepath))
        publish_messages(messages=messages)


class Teardown(SupportTaskBase):
    def run(self) -> None:
        self.change_status_to_completed_successfully()
        self.clean_local_fs()

    def clean_local_fs(self):
        rmtree(Path(environ.get("LOCAL_FILESYSTEM_ROOT")), str(self.recipe_run_id))
