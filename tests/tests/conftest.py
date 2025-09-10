import os

import pytest


@pytest.fixture(scope="function", autouse=True)
def collection_path(request):
    # return os.path.dirname(os.path.dirname(__file__))
    return os.path.dirname(str(request.fspath))
