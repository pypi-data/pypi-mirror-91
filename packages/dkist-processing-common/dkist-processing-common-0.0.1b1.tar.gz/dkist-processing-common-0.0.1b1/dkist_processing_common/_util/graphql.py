import json
from collections import defaultdict
from dataclasses import dataclass
from os import environ

from gqlclient import GraphQLClient


@dataclass
class RecipeRunMutation:
    recipeRunId: int
    recipeRunStatusId: int
    authToken: str = environ.get("GQL_AUTH_TOKEN")


@dataclass
class RecipeRunStatusResponse:
    recipeRunStatusId: int


@dataclass
class RecipeRunStatusQuery:
    recipeRunStatusName: str


@dataclass
class CreateRecipeRunStatusResponse:
    recipeRunStatus: RecipeRunStatusResponse


@dataclass
class RecipeRunStatusMutation:
    recipeRunStatusName: str
    isComplete: bool
    recipeRunStatusDescription: str = "To add a description, use the processing-preparation-worker"
    authToken: str = environ.get("GQL_AUTH_TOKEN")


@dataclass
class InputDatasetResponse:
    inputDatasetDocument: str


@dataclass
class ProcessingCandidateResponse:
    observingProgramExecutionId: str
    proposalId: str


@dataclass
class RecipeInstanceResponse:
    inputDataset: InputDatasetResponse
    processingCandidate: ProcessingCandidateResponse


@dataclass
class RecipeRunResponse:
    recipeInstance: RecipeInstanceResponse


@dataclass
class RecipeRunInputDatasetQuery:
    recipeRunId: int


@dataclass
class DatasetCatalogReceiptAccountMutation:
    """
    Dataclass used to write the dataset_catalog_receipt_account record for the run.
    It sets an expected object count for a dataset so that dataset inventory creation
    doesn't happen until all objects are transferred and inventoried.
    """

    datasetId: str
    expectedObjectCount: int
    authToken: str = environ.get("GQL_AUTH_TOKEN")


# Environment variable indicating how to connect to dependencies on the service mesh
MESH_CONFIG = json.loads(environ.get("MESH_CONFIG", default="null"))
host_port_default = {"mesh_address": "MISSING", "mesh_port": 999}
mesh_default = defaultdict(lambda: host_port_default, {})
MESH_CONFIG = MESH_CONFIG or mesh_default

graph_ql_client = GraphQLClient(
    f'http://{MESH_CONFIG["internal-api-gateway"]["mesh_address"]}:{MESH_CONFIG["internal-api-gateway"]["mesh_port"]}/graphql'
)
