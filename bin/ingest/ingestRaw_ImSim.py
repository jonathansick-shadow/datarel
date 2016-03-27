#!/usr/bin/env python

#
# LSST Data Management System
# Copyright 2008, 2009, 2010 LSST Corporation.
#
# This product includes software developed by the
# LSST Project (http://www.lsst.org/).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the LSST License Statement and
# the GNU General Public License along with this program.  If not,
# see <http://www.lsstcorp.org/LegalNotices/>.
#

import argparse
import os
import subprocess
import sys
from textwrap import dedent

import lsst.daf.base as dafBase
import lsst.daf.persistence as dafPersist
from lsst.obs.lsstSim import LsstSimMapper
import lsst.afw.coord as afwCoord
import lsst.afw.image as afwImage

from lsst.datarel.csvFileWriter import CsvFileWriter
from lsst.datarel.mysqlExecutor import MysqlExecutor, addDbOptions


if not 'SCISQL_DIR' in os.environ:
    print >>sys.stderr, "Please setup the scisql package and try again"
    sys.exit(1)

scisqlIndex = os.path.join(os.environ['SCISQL_DIR'], 'bin', 'scisql_index')

rafts = ["0,1", "0,2", "0,3",
                "1,0", "1,1", "1,2", "1,3", "1,4",
                "2,0", "2,1", "2,2", "2,3", "2,4",
                "3,0", "3,1", "3,2", "3,3", "3,4",
                "4,1", "4,2", "4,3"]

filterMap = ["u", "g", "r", "i", "z", "y"]


class CsvGenerator(object):

    def __init__(self, root, registry=None, compress=True):
        if registry is None:
            registry = os.path.join(root, "registry.sqlite3")
        self.mapper = LsstSimMapper(root=root, registry=registry)
        bf = dafPersist.ButlerFactory(mapper=self.mapper)
        self.butler = bf.create()

        self.expFile = CsvFileWriter("Raw_Amp_Exposure.csv",
                                     compress=compress)
        self.mdFile = CsvFileWriter("Raw_Amp_Exposure_Metadata.csv",
                                    compress=compress)
        self.rToSFile = CsvFileWriter("Raw_Amp_To_Science_Ccd_Exposure.csv",
                                      compress=compress)
        self.polyFile = open("Raw_Amp_Exposure_Poly.tsv", "wb")

    def csvAll(self):
        for visit, raft, sensor in self.butler.queryMetadata("raw", "sensor",
                                                             ("visit", "raft", "sensor")):
            if self.butler.datasetExists("raw", visit=visit, snap=0,
                                         raft=raft, sensor=sensor, channel="0,0"):
                self.toCsv(visit, raft, sensor)
        self.expFile.flush()
        self.mdFile.flush()
        self.rToSFile.flush()
        self.polyFile.flush()
        self.polyFile.close()

    def getFullMetadata(self, datasetType, **keys):
        filename = self.mapper.map(datasetType, keys).getLocations()[0]
        return afwImage.readMetadata(filename)

    def toCsv(self, visit, raft, sensor):
        r1, comma, r2 = raft
        s1, comma, s2 = sensor
        raftNum = rafts.index(raft)
        raftId = int(r1) * 5 + int(r2)
        ccdNum = int(s1) * 3 + int(s2)
        sciCcdExposureId = (long(visit) << 9) + raftId * 10 + ccdNum

        for snap in xrange(2):
            rawCcdExposureId = (sciCcdExposureId << 1) + snap

            for channelY in xrange(2):
                for channelX in xrange(8):
                    channel = "%d,%d" % (channelY, channelX)
                    channelNum = (channelY << 3) + channelX
                    rawAmpExposureId = (rawCcdExposureId << 4) + channelNum

                    try:
                        md = self.getFullMetadata("raw",
                                                  visit=visit, snap=snap,
                                                  raft=raft, sensor=sensor, channel=channel)
                    except:
                        print ("*** Unable to read metadata for " +
                               "visit %d snap %d " +
                               "raft %s sensor %s channel %s") % \
                            (visit, snap, raft, sensor, channel)
                        continue

                    self.rToSFile.write(rawAmpExposureId, sciCcdExposureId,
                                        snap, channelNum)

                    width = md.get('NAXIS1')
                    height = md.get('NAXIS2')
                    wcs = afwImage.makeWcs(md.deepCopy())
                    cen = wcs.pixelToSky(0.5*width - 0.5, 0.5*height - 0.5).toIcrs()
                    corner1 = wcs.pixelToSky(-0.5, -0.5).toIcrs()
                    corner2 = wcs.pixelToSky(-0.5, height - 0.5).toIcrs()
                    corner3 = wcs.pixelToSky(width - 0.5, height - 0.5).toIcrs()
                    corner4 = wcs.pixelToSky(width - 0.5, -0.5).toIcrs()
                    mjd = md.get('MJD-OBS')
                    if mjd == 0.0:
                        mjd = 49563.270671
                    obsStart = dafBase.DateTime(mjd,
                                                dafBase.DateTime.MJD, dafBase.DateTime.UTC)
                    expTime = md.get('EXPTIME')
                    obsMidpoint = dafBase.DateTime(obsStart.nsecs() +
                                                   long(expTime * 1000000000L / 2))
                    filterName = md.get('FILTER').strip()
                    self.expFile.write(rawAmpExposureId,
                                       visit, snap, raftNum, raft, ccdNum,
                                       sensor, channelNum, channel,
                                       filterMap.index(filterName), filterName,
                                       cen.getRa().asDegrees(), cen.getDec().asDegrees(),
                                       md.get('EQUINOX'), md.get('RADESYS'),
                                       md.get('CTYPE1'), md.get('CTYPE2'),
                                       md.get('CRPIX1'), md.get('CRPIX2'),
                                       md.get('CRVAL1'), md.get('CRVAL2'),
                                       md.get('CD1_1'), md.get('CD1_2'),
                                       md.get('CD2_1'), md.get('CD2_2'),
                                       corner1.getRa().asDegrees(),
                                       corner1.getDec().asDegrees(),
                                       corner2.getRa().asDegrees(),
                                       corner2.getDec().asDegrees(),
                                       corner3.getRa().asDegrees(),
                                       corner3.getDec().asDegrees(),
                                       corner4.getRa().asDegrees(),
                                       corner4.getDec().asDegrees(),
                                       obsStart.get(dafBase.DateTime.MJD,
                                                    dafBase.DateTime.TAI),
                                       obsStart,
                                       obsMidpoint.get(dafBase.DateTime.MJD,
                                                       dafBase.DateTime.TAI),
                                       expTime,
                                       md.get('AIRMASS'), md.get('DARKTIME'),
                                       md.get('ZENITH'))
                    for name in md.paramNames():
                        if md.typeOf(name) == md.TYPE_Int:
                            self.mdFile.write(rawAmpExposureId, name, 1,
                                              md.getInt(name), None, None)
                        elif md.typeOf(name) == md.TYPE_Double:
                            self.mdFile.write(rawAmpExposureId, name, 1,
                                              None, md.getDouble(name), None)
                        else:
                            self.mdFile.write(rawAmpExposureId, name, 1,
                                              None, None, str(md.get(name)))
                    self.polyFile.write("\t".join([
                        str(rawAmpExposureId),
                        repr(corner1.getRa().asDegrees()), repr(corner1.getDec().asDegrees()),
                        repr(corner2.getRa().asDegrees()), repr(corner2.getDec().asDegrees()),
                        repr(corner3.getRa().asDegrees()), repr(corner3.getDec().asDegrees()),
                        repr(corner4.getRa().asDegrees()), repr(corner4.getDec().asDegrees())]))
                    self.polyFile.write("\n")

        print "Processed visit %d raft %s sensor %s" % (visit, raft, sensor)


def dbLoad(sql):
    subprocess.call([scisqlIndex, "-l", "11",
                     "Raw_Amp_Exposure_To_Htm11.tsv",
                     "Raw_Amp_Exposure_Poly.tsv"])
    sql.execStmt(dedent("""\
        LOAD DATA LOCAL INFILE '%s' REPLACE INTO TABLE Raw_Amp_Exposure
        FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' (
            rawAmpExposureId, visit, snap, raft, raftName,
            ccd, ccdName, amp, ampName, filterId, filterName,
            ra, decl,
            equinox, raDeSys,
            ctype1, ctype2,
            crpix1, crpix2,
            crval1, crval2,
            cd1_1, cd1_2, cd2_1, cd2_2,
            corner1Ra, corner1Decl,
            corner2Ra, corner2Decl,
            corner3Ra, corner3Decl,
            corner4Ra, corner4Decl,
            taiMjd, obsStart, expMidpt, expTime,
            airmass, darkTime, zd
        ) SET htmId20 = scisql_s2HtmId(ra, decl, 20),
              poly = scisql_s2CPolyToBin(corner1Ra, corner1Decl,
                                         corner2Ra, corner2Decl,
                                         corner3Ra, corner3Decl,
                                         corner4Ra, corner4Decl);
        SHOW WARNINGS;
        """ % os.path.abspath("Raw_Amp_Exposure.csv")))
    sql.execStmt(dedent("""\
        LOAD DATA LOCAL INFILE '%s' REPLACE INTO TABLE Raw_Amp_Exposure_Metadata
        FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' (
            rawAmpExposureId,
            metadataKey,
            exposureType,
            intValue,
            doubleValue,
            stringValue);
        SHOW WARNINGS;
        """ % os.path.abspath("Raw_Amp_Exposure_Metadata.csv")))
    sql.execStmt(dedent("""\
        LOAD DATA LOCAL INFILE '%s' REPLACE INTO TABLE Raw_Amp_To_Science_Ccd_Exposure
        FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' (
            rawAmpExposureId,
            scienceCcdExposureId,
            snap,
            amp);
        SHOW WARNINGS;
        """ % os.path.abspath("Raw_Amp_To_Science_Ccd_Exposure.csv")))
    sql.execStmt(dedent("""\
        LOAD DATA LOCAL INFILE '%s' REPLACE INTO TABLE Raw_Amp_Exposure_To_Htm11 (
            rawAmpExposureId,
            htmId11);
        SHOW WARNINGS;
        """ % os.path.abspath("Raw_Amp_Exposure_To_Htm11.tsv")))


def main():
    parser = argparse.ArgumentParser(description="Program which converts raw LSST "
                                     "Sim exposure metadata to CSV files suitable for loading into MySQL. If "
                                     "a database name is specified in the options, the CSVs are also loaded "
                                     "into that database.",
                                     epilog="Make sure to run prepareDb.py before database loads - this "
                                     "instantiates the LSST schema in the target database.")
    addDbOptions(parser)
    parser.add_argument(
        "-d", "--database", dest="database",
        help="MySQL database to load CSV files into.")
    parser.add_argument(
        "-R", "--registry", dest="registry", help="Input registry path; "
        "used for all input roots. If omitted, a file named registry.sqlite3 "
        "must exist in each input root.")
    parser.add_argument("root", help="input root directory")
    ns = parser.parse_args()
    doLoad = ns.database != None
    if doLoad:
        if ns.user == None:
            parser.error("No database user name specified and $USER " +
                         "is undefined or empty")
        sql = MysqlExecutor(ns.host, ns.database, ns.user, ns.port)
    c = CsvGenerator(ns.root, ns.registry, not doLoad)
    c.csvAll()
    if doLoad:
        dbLoad(sql)

if __name__ == '__main__':
    main()

