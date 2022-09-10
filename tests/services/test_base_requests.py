from time import sleep
import pytest
from requests.models import Response
from requests.exceptions import ConnectionError
from src.services.base_requests import BaseClient


def test_cache(requests_mock_get):
    base = BaseClient()
    response = base.request_get('https://test-cache.io','token', ttl = 2)

    assert response.from_cache == False
    
    response_cached = base.request_get('https://test-cache.io','token')
    assert response_cached.from_cache == True

def test_cache_ttl(requests_mock_get):
    base = BaseClient()
    response = base.request_get('https://test-cache.io','token', ttl = 1)
    assert response.from_cache == False
    sleep(2)
    response_not_cached = base.request_get('https://test-cache.io','token')
    assert response_not_cached.from_cache == False


def test_request_connection_error(requests_mock):
    requests_mock.get('https://test.io', exc=ConnectionError)

    base = BaseClient()
    assert base.request_get('https://test.io','token') is False