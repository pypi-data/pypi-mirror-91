import pytest

from dkist_processing_common._util.data import publish_messages
from dkist_processing_common._util.interservice_bus import CatalogFrameMessage
from dkist_processing_common._util.interservice_bus import CatalogObjectMessage


def test_publish_messages(mocker):
    mocker.patch("dkist_processing_common._util.data.DurableBlockingProducerWrapper")
    messages = [CatalogFrameMessage(), CatalogObjectMessage(objectType="MOVIE")]
    publish_messages(messages)


def test_invalid_publish_messages(mocker):
    mocker.patch("dkist_processing_common._util.data.DurableBlockingProducerWrapper")
    messages = ["a"]
    with pytest.raises(AttributeError):
        publish_messages(messages)
