"""
Global test fixtures
"""
import pytest
from astropy.io import fits

from dkist_processing_common.base import SupportTaskBase


@pytest.fixture(scope="session")
def support_task():
    """
    Create task class for usage in tests
    """

    class TaskClass(SupportTaskBase):
        def run(self) -> None:
            pass

    return TaskClass(recipe_run_id=1, workflow_name="workflow_name", workflow_version="version")


@pytest.fixture(scope="session")
def fits_hdulist():
    """
    Create fits hdulist
    """
    hdu = fits.PrimaryHDU(range(100))
    return fits.HDUList([hdu])
