import pytest
from read_file import narrow, read_selected, read_DASHR, read_file_data
import datetime

DASHRlut = {9307: "E://", 435:"F://", 0000:"H://"}


def test_narrow():
    assert narrow([9307, 435], DASHRlut) = {9307: "E://", 435:"F://"}


def test_read_selected(mkfakeEdir, mkfakeFdir):
    log = {
            "logpins": [9307, 435],
            "numfiles": [1, 1],
            "notes": [[] []]
            }
    assert log == read_selected({9307: mkfakeEdir, 435: mkfakeFdir})


def test_read_DASHR(mkfakeEdir):
    ret = [1, 1]
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    assert ret == read_DASHR(9307, mkfakeEdir, now)


def test_read_file():
    with open("./test.txt", "w") as f:
        f.write("HELLO WORLD")
    assert read_file_data("./test.txt", 9307,
                          datetime.datetime.now()) == 1
    assert read_file_data("./test.txt", 9307,
                          datetime.datetime.now()) == 0
    with open("./test.txt", "w") as f:
        f.write("HI HUMANS")
        assert read_file_data("./test.txt", 9307,
                              datetime.datetime.now()) == 1
