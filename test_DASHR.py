import pytest
from DASHR import findSNs, determineDASHRs, readSN


def test_findSNs(mkfakeEdir, mkfakeFdir):
    LUT = {9307: mkfakeEdir, 435: mkfakeFdir}
    assert findSNs([mkfakeEdir, mkfakeFdir]) == LUT

def test_determineDASHRs(mkfakeEdir):
    assert determineDASHRs(mkfakeEdir) == 261791206


def test_readSN(mktestEfile):
    assert readSN(mktestEfile) == 261791206
