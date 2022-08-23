from typing import Callable

import pytest


@pytest.fixture(scope="module")
def vcr_config():
    return {"filter_query_parameters": ["api_key"]}


@pytest.fixture
def create_api_path() -> Callable[[str], str]:
    def inner(path: str) -> str:
        return "http://localhost:8000/v1" + path

    return inner
