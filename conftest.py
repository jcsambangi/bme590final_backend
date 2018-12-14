import pytest


@pytest.fixture
def mktestEfile(tmpdir_factory):
    """Creates test file for unit testing in tempEdir.

    :param tmpdir_factory:
    :returns: path of file for pin 9307 test
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
    """Returns 1/2 temporary directories for DASHR emulation.

    :param mktestEfile: fixture of path from created file
    :returns: path of parent directory E (9307)
    """
    tempEPath = mktestEfile[:-12]
    return tempEPath


@pytest.fixture
def mktestdir(tmpdir_factory):
    """Creates temporary directory for text files during testing.

    :param tmpdir_factory:
    :returns: directory fixture
    """
    testdir = tmpdir_factory.mktemp('testing')
    return testdir


@pytest.fixture
def testFile1(mktestdir):
    """Creates empty text file 1/2 for testing.

    :param mktestdir: directory fixture
    :returns: path of text file for file reading test
    """
    testFile = mktestdir.join('testFile1.txt')
    testFile1Path = testFile.strpath
    return testFile1Path


@pytest.fixture
def testFile2(mktestdir):
    """Creates empty text file 2/2 for testing.

    :param mktestdir: directory fixture
    :returns: path of text file for file reading test
    """
    testFile = mktestdir.join('testFile2.txt')
    testFile2Path = testFile.strpath
    return testFile2Path


@pytest.fixture
def mktestFfile(tmpdir_factory):
    """Creates test file for unit testing in tempFdir.

    :param tmpdir_factory:
    :returns: path of file for pin 435 test
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
    """Returns 2/2 temporary directories for DASHR emulation.

    :param mktestFfile: fixture of path from created file
    :returns: path of parent directory F (435)
    """
    tempFPath = mktestFfile[:-11]
    return tempFPath
