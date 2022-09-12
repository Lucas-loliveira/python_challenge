import pytest 
import requests_cache


@pytest.fixture(autouse=True)
def clear_cache():
    backend = requests_cache.RedisCache(host='cache', port=6379,password='eYVX7EwVmmxKPCDmwMtyKVge8oLd2t81')
    session = requests_cache.CachedSession('client_cache',backend)
    session.cache.clear()

@pytest.fixture()
def requests_mock_get(requests_mock):
    return requests_mock.get('https://test-cache.io', text='cached response')


@pytest.fixture()
def requests_mock_post(requests_mock):
    return requests_mock.post('https://test-cache.io', text='cached response')
