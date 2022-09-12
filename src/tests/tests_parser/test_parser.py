import pytest
from parser.parser_service import Parcer
from .fixtures import mocker_ip_raw_file, EXPECTED_DATA

def test_parcer_success(mocker_ip_raw_file):
    parcer = Parcer()
    assert parcer.extract_ips_from_file("fakefile.txt")["data"] == EXPECTED_DATA

def test_parcer_file_not_found():
    parcer = Parcer()
    result = parcer.extract_ips_from_file("fakefile.txt")

    assert result["success"] == False
    assert result["error"] == "file_not_found"
