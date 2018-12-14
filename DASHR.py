import sys
import os
import pathlib
import psutil
import numpy
from pin_lookup import pin


def compCrawl():
    """Finds local removable partitions.

    :returns: list of paths of removable partitions
    """
    allPartitions = psutil.disk_partitions()
    maybeDASHRpartitions = []
    for sdiskpart in allPartitions:
        if sdiskpart[3] == 'rw,removable':
            maybeDASHRpartitions.append(sdiskpart[1])
    return maybeDASHRpartitions


def findSNs():
    """Finds serial numbers associated with DASHRs with data.

    :returns: list of serial numbers as strings
    """
    maybeDASHRpartitions = compCrawl()
    DASHRlut = {}
    for possibleDASHR in maybeDASHRpartitions:
        hold = determineDASHRs(possibleDASHR)
        if hold is not False:
            try:
                pin_num = pin(hold)
                DASHRlut[pin_num] = possibleDASHR
            except FileNotFoundError:
                DASHRlut[int(hold)] = possibleDASHR
    print(DASHRlut)
    return DASHRlut


def determineDASHRs(maybeDASHRpartition):
    """Determines whether partition is a DASHR.

    :param maybeDASHRpartition: paths of all local removable drives
    :returns: serial number as int if partition has L0.BIN, False otherwise
    """
    for path, subdirs, files in os.walk(maybeDASHRpartition):
        for name in files:
            if name[0] == "L" and name[-3:] == "BIN":
                return readSN(pathlib.PurePath(path, name).as_posix())
    return False


def readSN(path):
    """Reads serial number from L0.BIN.

    :param path: string path of particular L0.BIN file
    :returns SN: integer serial number
    """
    return numpy.fromfile(path, dtype="uint32")[104]
