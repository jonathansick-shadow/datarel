#! /usr/bin/env python

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
from __future__ import with_statement
import argparse
import os

from lsst.datarel.mysqlExecutor import MysqlExecutor, addDbOptions

loadTables = {
    "lsstsim": ["Source",
                "Object",
                "RefObject",
                "RefObjMatch",
                "RefSrcMatch",
                "Science_Ccd_Exposure",
                "Science_Ccd_Exposure_Metadata",
                "Science_Ccd_Exposure_To_Htm10",
                "Raw_Amp_Exposure",
                "Raw_Amp_Exposure_Metadata",
                "Raw_Amp_To_Science_Ccd_Exposure",
                "Raw_Amp_Exposure_To_Htm11",
                "Raw_Amp_To_Science_Ccd_Exposure",
                ],
    "sdss": ["Source",
             "Object",
             "RefObject",
             "RefObjMatch",
             "RefSrcMatch",
             "Science_Ccd_Exposure",
             "Science_Ccd_Exposure_Metadata",
             "Science_Ccd_Exposure_To_Htm10"
             ],
}


def checkDb(sql, camera):
    for table in loadTables[camera]:
        try:
            result = sql.runQuery("SELECT COUNT(*) FROM " + table)
            if result[0][0] != 0:
                print "WARNING: non-empty table " + table
        except Exception, e:
            if hasattr(e, "__getitem__") and e[0] == 1049:
                return False
            else:
                raise e
    return True


def main():
    parser = argparse.ArgumentParser(description=
                                     "Program which creates an LSST run database and instantiates the LSST "
                                     "schema therein. Indexes on tables which will be loaded by the various "
                                     "datarel ingest scripts are disabled. Once loading has finished, the "
                                     "finishDb.py script should be run to re-enable them.")
    addDbOptions(parser)
    parser.add_argument("--camera", dest="camera", default="lsstSim",
                        help="Name of desired camera (defaults to %(default)s)")
    parser.add_argument("database", help="Name of database to create and "
                        "instantiate the LSST schema in.")
    ns = parser.parse_args()
    sql = MysqlExecutor(ns.host, ns.database, ns.user, ns.port)
    camera = ns.camera.lower()
    if camera not in loadTables:
        parser.error("Unknown camera: {}. Choices (not case sensitive): {}".format(
            camera, loadTables.keys()))
    if not checkDb(sql, camera):
        if 'CAT_DIR' not in os.environ or len(os.environ['CAT_DIR']) == 0:
            parser.error("$CAT_DIR is undefined or empty - "
                         "please setup the cat package and try again.")
        catDir = os.environ['CAT_DIR']
        sql.createDb(ns.database)
        sql.execScript(os.path.join(
            catDir, 'sql', 'lsstSchema4mysqlS12_{}.sql'.format(camera)))
        sql.execScript(os.path.join(catDir, 'sql', 'setup_perRunTablesS12_{}.sql'.format(camera)))
        sql.execScript(os.path.join(catDir, 'sql', 'setup_storedFunctions.sql'))
    # Disable indexes on tables for faster loading
    for table in loadTables[camera]:
        sql.execStmt("ALTER TABLE {} DISABLE KEYS;".format(table))

if __name__ == "__main__":
    main()

