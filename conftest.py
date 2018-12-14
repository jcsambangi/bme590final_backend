import pytest


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


@pytest.fixture
def mktestdir(tmpdir_factory):
    testdir = tmpdir_factory.mktemp('testing')
    return testdir


@pytest.fixture
def testFile1(mktestdir):
    testFile = mktestdir.join('testFile1.txt')
    testFile1Path = testFile.strpath
    return testFile1Path


@pytest.fixture
def testFile2(mktestdir):
    testFile = mktestdir.join('testFile2.txt')
    testFile2Path = testFile.strpath
    return testFile2Path


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
