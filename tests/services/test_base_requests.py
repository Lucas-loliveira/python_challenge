import pytest
from requests.models import Response
from requests.exceptions import ConnectionError
from src.services.base_requests import BaseClient


def test_request_connection_error(requests_mock):
    requests_mock.get('https://test.io', exc=ConnectionError)
    requests_mock.post('https://test.io', exc=ConnectionError)

    base = BaseClient()
    assert base._request_get('https://test.io','token') is False

def test_cache(requests_mock):
    requests_mock.get('https://test-cache.io', text='cached response')
    base = BaseClient()
    response = base._request_get('https://test-cache.io','token', ttl = 2)
    assert response.from_cache == False
    
    response_cached = base._request_get('https://test-cache.io','token')
    assert response_cached.from_cache == True

