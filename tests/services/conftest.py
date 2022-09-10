import pytest 
import requests_cache


@pytest.fixture(scope="session", autouse=True)
def clear_cache():
    session = requests_cache.CachedSession('client_cache')
    session.cache.clear()

