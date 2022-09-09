import pytest
from parser.parser import Parcer
from .fixtures import mocker_ip_raw_file, EXPECTED_DATA

def test_parcer_success(mocker_ip_raw_file):
    parcer = Parcer()
    assert parcer.extract_ips_from_file("fakefile.txt") == EXPECTED_DATA

def test_parcer_file_not_found():
    parcer = Parcer()
    with pytest.raises(FileNotFoundError):
        parcer.extract_ip_from_file("fakefile.txt")
