import sys
import os
import pathlib
import psutil
import numpy


def findSNs():
    """Finds serial numbers associated with DASHRs with data.

    :returns: list of serial numbers as strings
    """
    allPartitions = psutil.disk_partitions()
    maybeDASHRpartitions = []
    for sdiskpart in allPartitions:
        if sdiskpart[3] == 'rw,removable':
            maybeDASHRpartitions.append(sdiskpart[1])
    DASHRlut = {}
    for possibleDASHR in maybeDASHRpartitions:
        hold = determineDASHRs(possibleDASHR)
        if hold is not False:
            DASHRlut[hold] = possibleDASHR
    return DASHRlut


def determineDASHRs(maybeDASHRpartition):
    """Determines whether partition is a DASHR.

    :param maybeDASHRpartition: paths of all local removable drives
    :returns: serial number as int if partition has L0.BIN, False otherwise
    """
    for path, subdirs, files in os.walk(maybeDASHRpartition):
        for name in files:
            if name == "L0.BIN":
                return readSN(pathlib.PurePath(path,name).as_posix())
    return False


def readSN(path):
    """Reads serial number from L0.BIN.

    :param path: string path of particular L0.BIN file
    :returns SN: integer serial number
    """
    return numpy.fromfile(path, dtype="uint32")[104]    
