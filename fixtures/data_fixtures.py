import pytest

from helpers.testdata import D


@pytest.fixture
def case_data():
    return D


@pytest.fixture(scope="session")
def db():
    from helpers.db_client import DbClient

    return DbClient.from_env()
