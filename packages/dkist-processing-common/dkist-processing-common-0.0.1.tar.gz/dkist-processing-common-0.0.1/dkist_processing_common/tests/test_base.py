from pathlib import Path

import pytest
from astropy.io import fits

from dkist_processing_common._util.graphql import CreateRecipeRunStatusResponse
from dkist_processing_common._util.graphql import InputDatasetResponse
from dkist_processing_common._util.graphql import ProcessingCandidateResponse
from dkist_processing_common._util.graphql import RecipeInstanceResponse
from dkist_processing_common._util.graphql import RecipeRunResponse
from dkist_processing_common._util.graphql import RecipeRunStatusResponse


class FakeGQLClient:
    @staticmethod
    def execute_gql_query(**kwargs):
        query_base = kwargs["query_base"]

        if query_base == "recipeRunStatuses":
            return [RecipeRunStatusResponse(recipeRunStatusId=1)]
        if query_base == "recipeRuns":
            return [
                RecipeRunResponse(
                    recipeInstance=RecipeInstanceResponse(
                        processingCandidate=ProcessingCandidateResponse(
                            observingProgramExecutionId="abc", proposalId="123"
                        ),
                        inputDataset=InputDatasetResponse(
                            inputDatasetDocument='{"bucket": "bucket-name", "parameters": [{"parameterName": "", "parameterValues": [{"parameterValueId": 1, "parameterValue": "[[1,2,3],[4,5,6],[7,8,9]]", "parameterValueStartDate": "1/1/2000"}]}], "frames": ["objectKey1", "objectKey2", "objectKeyN"]}'
                        ),
                    )
                )
            ]

    @staticmethod
    def execute_gql_mutation(**kwargs):
        mutation_base = kwargs["mutation_base"]

        if mutation_base == "updateRecipeRun":
            return
        if mutation_base == "createRecipeRunStatus":
            return CreateRecipeRunStatusResponse(
                recipeRunStatus=RecipeRunStatusResponse(recipeRunStatusId=1)
            )


def test_change_status_to_in_progress(support_task, mocker):
    mocker.patch("dkist_processing_common.base.graph_ql_client", new=FakeGQLClient)
    support_task.change_status_to_in_progress()


def test_change_status_to_completed_successfully(support_task, mocker):
    mocker.patch("dkist_processing_common.base.graph_ql_client", new=FakeGQLClient)
    support_task.change_status_to_completed_successfully()


def test_input_dir(support_task, tmp_path):
    directory = support_task.input_dir(base=tmp_path)
    assert directory.exists()
    assert directory.parts[-1] == "input"
    assert directory.parts[-2] == "1"


def test_support_dir(support_task, tmp_path):
    directory = support_task.support_dir(base=tmp_path)
    assert directory.exists()
    assert directory.parts[-1] == "support"
    assert directory.parts[-2] == "1"


def test_output_dir(support_task, tmp_path):
    directory = support_task.output_dir(base=tmp_path)
    assert directory.exists()
    assert directory.parts[-1] == "output"
    assert directory.parts[-2] == "1"


def test_input_dataset(support_task, mocker, tmp_path):
    mocker.patch("dkist_processing_common.base.graph_ql_client", new=FakeGQLClient)
    r_all = support_task.input_dataset(base=tmp_path)
    r_section = support_task.input_dataset(section="parameters", base=tmp_path)
    assert r_all["bucket"] == "bucket-name"
    assert len(r_all["frames"]) == 3
    assert r_section[0]["parameterValues"][0]["parameterValueId"] == 1
    assert r_section[0]["parameterValues"][0]["parameterValue"] == "[[1,2,3],[4,5,6],[7,8,9]]"
    assert r_section[0]["parameterValues"][0]["parameterValueStartDate"] == "1/1/2000"


@pytest.mark.skip
def test_write_intermediate_data(tmp_path, support_task, fits_hdulist):
    filename = "file.fits"
    support_task.write_intermediate_data(data=fits_hdulist, filename=filename, filepath=tmp_path)
    fits.open(tmp_path / "support" / filename)


@pytest.mark.skip
def test_write_output_data(tmp_path, support_task, fits_hdulist):
    filename = "file.fits"
    support_task.write_output_data(data=fits_hdulist, filename=filename, filepath=tmp_path)
    fits.open(tmp_path / "output" / filename)


@pytest.mark.skip
def test_write_movie(tmp_path, support_task):
    pass


def test_get_proposal_id(support_task, mocker):
    mocker.patch("dkist_processing_common.base.graph_ql_client", new=FakeGQLClient)
    assert support_task.proposal_id == "123"


def test_frame_message(support_task):
    msg = support_task.create_frame_message(object_filepath="/test/object/path.ext")
    assert msg.objectName == "/test/object/path.ext"
    assert msg.conversationId == "1"
    assert msg.bucket == "data"
    assert msg.incrementDatasetCatalogReceiptCount


def test_movie_message(support_task):
    msg = support_task.create_movie_message(object_filepath="/test/object/path.ext")
    assert msg.objectName == "/test/object/path.ext"
    assert msg.conversationId == "1"
    assert msg.bucket == "data"
    assert msg.objectType == "MOVIE"
    assert msg.groupName == "DATASET"
    assert msg.incrementDatasetCatalogReceiptCount


def test_add_new_recipe_run_status(support_task, mocker):
    mocker.patch("dkist_processing_common.base.graph_ql_client", new=FakeGQLClient)
    with pytest.raises(TypeError):
        support_task.add_new_recipe_run_status(status=4, is_complete=True)
    with pytest.raises(TypeError):
        support_task.add_new_recipe_run_status(status="INPROGRESS", is_complete="true")
    with pytest.raises(KeyError):
        support_task.add_new_recipe_run_status(status="READY", is_complete=True)
    assert isinstance(
        support_task.add_new_recipe_run_status(status="INPROGRESS", is_complete=True), int
    )
