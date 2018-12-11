import pytest
from read_file import narrow, read_selected, read_DASHR, read_file_data
import datetime

DASHRlut = {9307: "E://", 435:"F://", 0000:"H://"}


@pytest.fixture
def mkfakeEdir(tmpdir_factory):
    """Creates 1/2 temporary directories for unit testing-required files.
    :param tmpdir_factory:
    :returns: tmpdir object
    """
    fakeEdir = tmpdir_factory.mktemp('fakeE')
    return fakeEdir


@pytest.fixture
def mktestfile(fakeEdir):
    """Creates test file for unit testing in fakeEdir.
    """
    testFile = tmpdir.join('9307L0.BIN')
    test9307Path = testFile.strpath
    with open('9307L0.BIN', 'rb') as binaryFile:
        hold = binaryFile.read(64)
    with open(test9307Path, 'wb') as binaryFile:
        binaryFile.write(hold)
    return test9307Path


@pytest.fixture
def mkfakeFdir(tmpdir_factory):
    """Creates 2/2 temporary directories for unit testing-required files.
    :param tmpdir_factory:
    :returns: tmpdir object
    """
    fakeFdir = tmpdir_factory.mktemp('fakeF')
    return fakeFdir


@pytest.fixture
def mktestfile(fakeFdir):
    """Creates test file for unit testing in fakeHdir.
    """
    testFile = tmpdir.join('435L0.BIN')
    test435Path = testFile.strpath
    with open('435L0.BIN', 'rb') as binaryFile:
        hold = binaryFile.read(64)
    with open(test435Path, 'wb') as binaryFile:
        binaryFile.write(hold)
    return test435Path


def test_narrow():
    assert narrow([9307, 435], DASHRlut) = {9307: "E://", 435:"F://"}


def test_read_selected():
    read_selected({9307: "E://", 435:"F://"})


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
