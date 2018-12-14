import pytest
import logging


#@pytest.fixture
#def mkfakeEdir(tmpdir_factory):
#    """Creates 1/2 temporary directories for unit testing-required files.
#    :param tmpdir_factory:
#    :returns: tmpdir object
#    """
#    fakeEdir = tmpdir_factory.mktemp('fakeE')
#    return fakeEdir


@pytest.fixture
def mktestEfile(tmpdir_factory):
    """Creates test file for unit testing in fakeEdir.
    """
    tempEdir = tmpdir_factory.mktemp('tempE')
    testFile = tempEdir.join('L9307L0.BIN')
    test9307Path = testFile.strpath
    with open('./testing/9307L0.BIN', 'rb') as binaryFile:
        hold = binaryFile.read()
    with open(test9307Path, 'wb') as binaryFile:
        binaryFile.write(hold)
    return test9307Path


@pytest.fixture
def mkfakeEdir(mktestEfile):
    """Creates 1/2 temporary directories for unit testing-required files.
    :param tmpdir_factory:
    :returns: tmpdir object
    """
    tempEPath = mktestEfile[:-12]
    return tempEPath


#@pytest.fixture
#def mkfakeFdir(tmpdir_factory):
#    """Creates 2/2 temporary directories for unit testing-required files.
#    :param tmpdir_factory:
#    :returns: tmpdir object
#    """
#    fakeFdir = tmpdir_factory.mktemp('fakeF')
#    return fakeFdir


@pytest.fixture
def mktestFfile(tmpdir_factory):
    """Creates test file for unit testing in fakeHdir.
    """
    tempFdir = tmpdir_factory.mktemp('tempF')
    testFile = tempFdir.join('L435L0.BIN')
    test435Path = testFile.strpath
    with open('./testing/435L0.BIN', 'rb') as binaryFile:
        hold = binaryFile.read()
    with open(test435Path, 'wb') as binaryFile:
        binaryFile.write(hold)
    return test435Path


@pytest.fixture
def mkfakeFdir(mktestFfile):
    """Creates 2/2 temporary directories for unit testing-required files.
    :param tmpdir_factory:
    :returns: tmpdir object
    """
    tempFPath = mktestFfile[:-11]
    return tempFPath
