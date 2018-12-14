import sys
import os
import pathlib
import psutil
import numpy
from pin_lookup import pin
from datetime import datetime


def compCrawl():
    """Finds local removable partitions. No associated unit test.

    :returns: list of paths of removable partitions
    """
    allPartitions = psutil.disk_partitions()
    maybeDASHRpartitions = []
    for sdiskpart in allPartitions:
        if sdiskpart[3] == 'rw,removable':
            maybeDASHRpartitions.append(sdiskpart[1])
    return maybeDASHRpartitions


def findSNs(maybeDASHRpartitions):
    """Finds serial numbers associated with DASHRs with data.

    :param maybeDASHRpartitions: array of partitions that may be DASHRs
    :returns: list of serial numbers or PINs as strings
    """
    DASHRlut = {}
    for possibleDASHR in maybeDASHRpartitions:
        hold = determineDASHRs(possibleDASHR)
        if hold is not False:
            try:
                pin_num = pin(hold)
                DASHRlut[pin_num] = possibleDASHR
            except FileNotFoundError:
                DASHRlut[int(hold)] = possibleDASHR
    return DASHRlut


def dateOverview(DASHRlut):
    """Compiles dates and numbers of files for all input DASHRs.

    :param: dicionary with keys as pins and values as DASHR paths
    :returns: dictionary with keys as pins and values arrays [date numFiles]
    """
    dateLUT = {}
    for pin in DASHRlut:
        oneDASHRdatesData = dateBreakdown(DASHRlut[pin])
        dateLUT[pin] = []
        for key in oneDASHRdatesData:
            dateArr = []
            dateArr.append(key)
            dateArr.append(oneDASHRdatesData[key])
            dateLUT[pin].append(dateArr)
    return dateLUT


def dateBreakdown(possibleDASHR):
    """Determines spread of files per dates on given DASHR partition.

    :param possibleDASHR: partition path of DASHR
    :returns: dictionary with dates as keys and numbers of files as values
    """
    dateHarvest = {}
    for path, subdirs, files in os.walk(possibleDASHR):
        for name in files:
            if name[0] == "L" and name[-3:] == "BIN":
                s = os.path.getmtime(pathlib.PurePath(path, name).as_posix())
                reg = datetime.fromtimestamp(s).strftime('%m-%d-%Y')
                if reg not in dateHarvest:
                    dateHarvest[reg] = 1
                else:
                    dateHarvest[reg] = dateHarvest[reg] + 1
    return dateHarvest


def determineDASHRs(maybeDASHRpartition):
    """Determines whether partition is a DASHR.

    :param maybeDASHRpartition: paths of all local removable drives
    :returns: int serial number if partition starts with L and ends with BIN
    """
    for path, subdirs, files in os.walk(maybeDASHRpartition):
        for name in files:
            if name[0] == "L" and name[-3:] == "BIN":
                return readSN(pathlib.PurePath(path, name).as_posix())
    return False


def readSN(path):
    """Reads serial number from .BIN file.

    :param path: string path of particular .BIN file
    :returns SN: integer serial number
    """
    return numpy.fromfile(path, dtype="uint32")[104]
