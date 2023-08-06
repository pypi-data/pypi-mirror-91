"""

"""
import json
from abc import ABC
from abc import abstractmethod
from contextlib import contextmanager
from os import environ
from os import umask
from pathlib import Path
from typing import Optional
from typing import Union

from dkist_processing_core import TaskBase

from dkist_processing_common._util.graphql import CreateRecipeRunStatusResponse
from dkist_processing_common._util.graphql import graph_ql_client
from dkist_processing_common._util.graphql import RecipeRunInputDatasetQuery
from dkist_processing_common._util.graphql import RecipeRunMutation
from dkist_processing_common._util.graphql import RecipeRunResponse
from dkist_processing_common._util.graphql import RecipeRunStatusMutation
from dkist_processing_common._util.graphql import RecipeRunStatusQuery
from dkist_processing_common._util.graphql import RecipeRunStatusResponse
from dkist_processing_common._util.interservice_bus import CatalogFrameMessage
from dkist_processing_common._util.interservice_bus import CatalogObjectMessage


class TaskBaseExt(TaskBase, ABC):
    @staticmethod
    @contextmanager
    def mask():
        old_mask = umask(0)
        try:
            yield
        finally:
            umask(old_mask)

    def get_directory(self, directory_name, base: Optional[Path] = None):
        if not base:
            base = Path(environ.get("LOCAL_FILESYSTEM_ROOT", "tmp/"))
        directory = base / str(self.recipe_run_id) / directory_name
        directory.mkdir(parents=True, exist_ok=True)
        return directory

    def input_dir(self, base: Optional[Path] = None):
        return self.get_directory(directory_name="input", base=base)

    def support_dir(self, base: Optional[Path] = None):
        return self.get_directory(directory_name="support", base=base)

    def output_dir(self, base: Optional[Path] = None):
        return self.get_directory(directory_name="output", base=base)

    def input_dataset(self, section: str = "all", base: Optional[Path] = None) -> Union[dict, None]:
        local_input_dataset_path = self.support_dir(base=base) / "input_dataset.json"

        if not local_input_dataset_path.exists():
            # Get input dataset from db
            input_dataset_response = graph_ql_client.execute_gql_query(
                query_base="recipeRuns",
                query_response_cls=RecipeRunResponse,
                query_parameters=RecipeRunInputDatasetQuery(recipeRunId=self.recipe_run_id),
            )
            # Write document to disk for future use
            with open(local_input_dataset_path, "w") as f:
                f.write(
                    str(input_dataset_response[0].recipeInstance.inputDataset.inputDatasetDocument)
                )

        with local_input_dataset_path.open("r") as f:
            input_dataset_document = json.loads(f.read())

        section = section.lower()
        if section == "all":
            return input_dataset_document
        return input_dataset_document.get(section, None)

    # def write_fits(
    #     self,
    #     hdulist: Type[fits.hdu.HDUList],
    #     filename: str,
    #     filepath: Path,
    # ):
    #     with self.mask():
    #         filepath.mkdir(parents=True, exist_ok=True)
    #     hdulist.writeto(filepath / filename, overwrite=True, checksum=True)
    #
    # def write_intermediate_data(self, data, filename: str, filepath: Optional[Path] = None):
    #     filepath = filepath or self.filepath
    #     filepath = filepath / "support"
    #     self.write_fits(hdulist=data, filename=filename, filepath=filepath)
    #
    # def write_output_data(self, data, filename: str, filepath: Optional[Path] = None):
    #     filepath = filepath or self.filepath
    #     filepath = filepath / "output"
    #     self.write_fits(hdulist=data, filename=filename, filepath=filepath)

    def write_movie(self):
        raise NotImplementedError


class SupportTaskBase(TaskBaseExt, ABC):
    recipe_run_statuses = {
        "INPROGRESS": "Recipe run is currently undergoing processing",
        "COMPLETEDSUCCESSFULLY": "Recipe run processing completed with no errors",
    }

    @property
    def output_filepaths(self) -> list:
        return list(
            Path(
                "/",
                environ.get("LOCAL_FILESYSTEM_ROOT", "tmp"),
                str(self.recipe_run_id),
                "output",
            ).glob("*.fits")
        )

    def change_status_to_in_progress(self):
        self._change_status(status="INPROGRESS", is_complete=False)

    def change_status_to_completed_successfully(self):
        self._change_status(status="COMPLETEDSUCCESSFULLY", is_complete=True)

    def _change_status(self, status: str, is_complete: bool):
        status_response = self.get_message_status_query(status=status)

        # If the status was found
        if len(status_response) > 0:
            # Get the status ID
            recipe_run_status_id = status_response[0].recipeRunStatusId
        else:
            # Add the status to the db and get the new status ID
            recipe_run_status_id = self.add_new_recipe_run_status(
                status=status, is_complete=is_complete
            )

        self.apply_status_id_to_recipe_run(recipe_run_status_id=recipe_run_status_id)

    @staticmethod
    def get_message_status_query(status: str):
        return graph_ql_client.execute_gql_query(
            query_base="recipeRunStatuses",
            query_response_cls=RecipeRunStatusResponse,
            query_parameters=RecipeRunStatusQuery(recipeRunStatusName=status),
        )

    def add_new_recipe_run_status(self, status: str, is_complete: bool) -> int:
        if not isinstance(status, str):
            raise TypeError(f"status must be of type str: {status}")
        if not isinstance(is_complete, bool):
            raise TypeError(f"is_complete must be of type bool: {is_complete}")
        recipe_run_status_response = graph_ql_client.execute_gql_mutation(
            mutation_base="createRecipeRunStatus",
            mutation_response_cls=CreateRecipeRunStatusResponse,
            mutation_parameters=RecipeRunStatusMutation(
                recipeRunStatusName=status,
                isComplete=is_complete,
                recipeRunStatusDescription=self.recipe_run_statuses[status],
            ),
        )
        return recipe_run_status_response.recipeRunStatus.recipeRunStatusId

    def apply_status_id_to_recipe_run(self, recipe_run_status_id: int):
        graph_ql_client.execute_gql_mutation(
            mutation_base="updateRecipeRun",
            mutation_parameters=RecipeRunMutation(
                recipeRunId=self.recipe_run_id, recipeRunStatusId=recipe_run_status_id
            ),
        )

    @property
    def proposal_id(self) -> str:
        try:
            getattr(self, "_proposal_id")
        except AttributeError:
            self._proposal_id = graph_ql_client.execute_gql_query(
                query_base="recipeRuns",
                query_response_cls=RecipeRunResponse,
                query_parameters=RecipeRunInputDatasetQuery(recipeRunId=self.recipe_run_id),
            )[0].recipeInstance.processingCandidate.proposalId
        return self._proposal_id

    def create_frame_message(self, object_filepath: str):
        catalog_frame_message = CatalogFrameMessage(
            objectName=object_filepath, conversationId=str(self.recipe_run_id)
        )
        return catalog_frame_message

    def create_movie_message(self, object_filepath: str):
        catalog_movie_message = CatalogObjectMessage(
            objectType="MOVIE",
            objectName=object_filepath,
            groupId=self.dataset_id,
            conversationId=str(self.recipe_run_id),
        )
        return catalog_movie_message


class ScienceTaskBase(TaskBaseExt):
    def record_provenance(self):
        pass  # TODO

    @abstractmethod
    def run(self) -> None:
        """
        Abstract method that must be overridden to execute the desired DAG task.
        """
