from unittest import mock
from unittest.mock import MagicMock
from geoip.ip_api_service import IpApiClient
from .conftest import ID_LIST, GEOIP_DATA
from geoip.constants import IP_API_TIMEOUT_LIMIT, IP_API_LIMIT_SIZE


@mock.patch("services.base_requests.BaseClient.request_post_with_cache")
def test_get_geoip_batch(mock_post_cache):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.headers = {'X-Rl':1, 'X-Ttl': 1}
    mock_response.json.return_value = GEOIP_DATA
    mock_response.from_cache = False
    mock_post_cache.return_value = mock_response
    
    ip_api = IpApiClient()
    result = ip_api.get_geoip_batch(ID_LIST)
    assert result["success"] == True
    assert result["data"] == GEOIP_DATA


@mock.patch("services.base_requests.BaseClient.request_post_with_cache")
def test_get_geoip_batch_400_code(mock_post_cache):
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_post_cache.return_value = mock_response
    
    ip_api = IpApiClient()
    result = ip_api.get_geoip_batch(ID_LIST)
    assert result["success"] == False
    assert result["error"] == f"{mock_response.status_code} status code"

@mock.patch("services.base_requests.BaseClient.request_post_with_cache")
def test_get_geoip_batch_time_out(mock_post_cache):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.headers = {'X-Rl':0, 'X-Ttl': IP_API_TIMEOUT_LIMIT+1}
    mock_response.json.return_value = GEOIP_DATA
    mock_response.from_cache = False
    mock_post_cache.return_value = mock_response
    
    ip_api = IpApiClient()
    result = ip_api.get_geoip_batch(ID_LIST)
    assert result["success"] == True
    assert result["data"] == GEOIP_DATA

    result = ip_api.get_geoip_batch(ID_LIST)
    assert result["success"] == False
    assert result["error"] == "ip api unavailable"


def test_get_geoip_batch_size_limit():
    ip_api = IpApiClient()
    result = ip_api.get_geoip_batch([i for i in range(IP_API_LIMIT_SIZE+1)])

    assert result["success"] == False
    assert result["error"] == f"ip list needs to have less than {IP_API_LIMIT_SIZE} elements"

