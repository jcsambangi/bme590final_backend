import pytest


@pytest.fixture
def mkfakeEdir(tmpdir_factory):
    """Creates 1/2 temporary directories for unit testing-required files.
    :param tmpdir_factory:
    :returns: tmpdir object
    """
    fakeEdir = tmpdir_factory.mktemp('fakeE')
    return fakeEdir


@pytest.fixture
def mktestEfile(mkfakeEdir):
    """Creates test file for unit testing in fakeEdir.
    """
    testFile = mkfakeEdir.join('L9307L0.BIN')
    test9307Path = testFile.strpath
    with open('9307L0.BIN', 'rb') as binaryFile:
        hold = binaryFile.read()
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
def mktestFfile(mkfakeFdir):
    """Creates test file for unit testing in fakeHdir.
    """
    testFile = mkfakeFdir.join('L435L0.BIN')
    test435Path = testFile.strpath
    with open('435L0.BIN', 'rb') as binaryFile:
        hold = binaryFile.read()
    with open(test435Path, 'wb') as binaryFile:
        binaryFile.write(hold)
    return test435Path
