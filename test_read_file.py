from read_file import read_file_data


def test_read_file():
    assert read_file_data("..\..\..\Downloads\L0.BIN") == 1

