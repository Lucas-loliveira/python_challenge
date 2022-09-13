from unittest import mock
from rdap.rdap_service import RADP
from .conftest import ID_LIST, RDAP_DATA



@mock.patch("rdap.rdap_service.RADP.write_result_file", return_value={"success": True})
@mock.patch("rdap.api_rdap_client.RDAPApiClient.get_rdap_from_ip", return_value={"success": True, "data": RDAP_DATA})
def test_get_rdap(mock_write_result_file,mock_rdap):
    rdap = RADP(ID_LIST)
    file_name = "result_data/test.txt"
    result = rdap.process_rdap(file_name)
    assert result["success"] == True
    assert result["data"] == file_name


@mock.patch("rdap.rdap_service.RADP.write_result_file", return_value={"success": True})
@mock.patch("rdap.api_rdap_client.RDAPApiClient.get_rdap_from_ip", return_value={"success": False, "data": {"success": False, "error": "error"}})
def test_get_rdap_fail(mock_write_result_file,mock_rdap):
    rdap = RADP(ID_LIST)
    file_name = "result_data/test.txt"
    result = rdap.process_rdap(file_name)
    assert result["success"] == True
    assert result["data"] == file_name


@mock.patch("rdap.rdap_service.RADP.write_result_file", return_value={"success": False, "error": f"result_file not found"})
@mock.patch("rdap.api_rdap_client.RDAPApiClient.get_rdap_from_ip", return_value={"success": False, "data": {"success": False, "error": "error"}})
def test_get_rdap_file_not_found(mock_write_result_file,mock_rdap):
    rdap = RADP(ID_LIST)
    file_name = "result_data/test.txt"
    result = rdap.process_rdap(file_name)
    assert result["success"] == False
    assert result["error"] == "result_file not found"

