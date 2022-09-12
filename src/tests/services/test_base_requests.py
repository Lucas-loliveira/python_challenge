from time import sleep
import pytest
from requests.models import Response
from requests.exceptions import ConnectionError
from services.base_requests import BaseClient


def test_cache_get(requests_mock_get):
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


def test_request_connection_error_get(requests_mock):
    requests_mock.get('https://test.io', exc=ConnectionError)

    base = BaseClient()
    response = base.request_get('https://test.io','token')
    assert response.status_code == 500
    assert response.json()["error"] == 'connection error'


def test_cache_post(requests_mock_post):
    base = BaseClient()
    
    response = base.request_post_with_cache('https://test-cache.io','token', {"ip": "2.2"}, ttl = 5)
    assert response.from_cache == False
    
    response_cached = base.request_post_with_cache('https://test-cache.io','token', {"ip": "2.2"})
    assert response_cached.from_cache == True


def test_request_connection_error_post(requests_mock):
    requests_mock.post('https://test.io', exc=ConnectionError)

    base = BaseClient()
    
    response =  base.request_post_with_cache('https://test.io','token',{"ip": "2.2"})
    assert response.status_code == 500
    assert response.json()["error"] == 'connection error'