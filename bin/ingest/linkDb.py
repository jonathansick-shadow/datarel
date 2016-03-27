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

import argparse

from lsst.datarel.mysqlExecutor import MysqlExecutor, addDbOptions


def main():
    parser = argparse.ArgumentParser(description=
                                     "Program which \"links\" an LSST per-run database into the well-known "
                                     "database name buildbot_weekly_latest by creating views for each table.")
    addDbOptions(parser)
    parser.add_argument(
        "-t", "--tag", dest="type", default="tags", choices=["trunk", "tags"],
        help="Type of stack which generated DB")
    parser.add_argument("database", help="Name of database to \"link\" from.")
    ns = parser.parse_args()
    print ns
    if ns.user == None:
        parser.error("No database user name specified and $USER is undefined or empty")
    viewName = "buildbot_weekly_latest_" + ns.type
    print viewName
    sql = MysqlExecutor(ns.host, viewName, ns.user, ns.port)
    for table in (
            "AmpMap", "CcdMap", "Filter", "LeapSeconds", "Logs",
            "Object", "ObjectType", "RaftMap",
            "Raw_Amp_Exposure", "Raw_Amp_Exposure_Metadata",
            "Raw_Amp_Exposure_To_Htm11", "Raw_Amp_To_Science_Ccd_Exposure",
            "RefObjMatch", "RefSrcMatch", "RunObject", "RunSource",
            "Science_Ccd_Exposure", "Science_Ccd_Exposure_Metadata",
            "Science_Ccd_Exposure_To_Htm10", "RefObject",
            "Source", "Visit",
            "ZZZ_Db_Description",):
        sql.execStmt(str.format(
            "CREATE OR REPLACE SQL SECURITY INVOKER VIEW {0} AS "
            "SELECT * FROM {1}.{0};", table, ns.database))
    sql.execStmt(str.format(
        "UPDATE ZZZ_View_Description SET src='{}';", ns.database))

if __name__ == "__main__":
    main()
