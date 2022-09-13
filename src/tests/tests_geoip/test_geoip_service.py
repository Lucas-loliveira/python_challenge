from unittest import mock
from geoip.geoip_service import GeoIP
from .conftest import ID_LIST, GEOIP_DATA


@mock.patch("geoip.geoip_service.GeoIP.write_result_file", return_value={"success": True})
@mock.patch("geoip.ip_api_service.IpApiClient.get_geoip_batch", return_value={"success": True, "data": GEOIP_DATA})
def test_geoip(mock_write_result_file,mock_geoip):
    geoip = GeoIP(ID_LIST)
    file_name = "result_data/test.txt"
    result =  geoip.process_geoip(file_name)
    assert result["success"] == True
    assert result["data"] == file_name


@mock.patch("geoip.geoip_service.GeoIP.write_result_file", return_value={"success": True})
@mock.patch("geoip.ip_api_service.IpApiClient.get_geoip_batch", return_value={"success": False, "error": "error"})
def test_geoip_ip_api_fail(mock_write_result_file,mock_geoip):
    geoip = GeoIP(ID_LIST)
    file_name = "result_data/test.txt"
    result =  geoip.process_geoip(file_name)
    assert result["success"] == False
    assert result["error"] == "ip api return error"


@mock.patch("geoip.geoip_service.GeoIP.write_result_file", return_value={"success": False, "error": f"result_file not found"})
@mock.patch("geoip.ip_api_service.IpApiClient.get_geoip_batch", return_value={"success": True, "data": GEOIP_DATA})
def test_geoip_file_not_found(mock_write_result_file,mock_geoip):
    geoip = GeoIP(ID_LIST)
    file_name = "result_data/test.txt"
    result =  geoip.process_geoip(file_name)
    assert result["success"] == False
    assert result["error"] == "result_file not found"