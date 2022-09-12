import pytest

RAW_DATA_TEST = "236.220.190.72 208.128.240.232 \n 208.128.240.230 \n 123.42.170.221"
EXPECTED_DATA = ['236.220.190.72', '208.128.240.232', '208.128.240.230', '123.42.170.221']

@pytest.fixture
def mocker_ip_raw_file(mocker):
    mocked_etc_release_data = mocker.mock_open(read_data=RAW_DATA_TEST)
    builtin_open = "builtins.open"
    mocker.patch(builtin_open, mocked_etc_release_data)



