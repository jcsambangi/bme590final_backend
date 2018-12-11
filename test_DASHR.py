import pytest
from DASHR import determineDASHRs, readSN


def test_determineDASHRs(mkfakeEdir):
    assert determineDASHRs(mkfakeEdir) == 261791206


def test_readSN(mktestEfile):
    assert readSN(mktestEfile) == 261791206
