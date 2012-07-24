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

import math
import argparse
import os
import subprocess
import sys
import time

from textwrap import dedent
import glob
import re


def _line_to_args(self, line):
    for arg in shlex.split(line, comments=True, posix=True):
        if not arg.strip():
            continue
        yield arg


def makeArgumentParser(description, inRootsRequired=True, addRegistryOption=True):

    parser = argparse.ArgumentParser(
        description=description,
        fromfile_prefix_chars="@",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=" \n"
               "ly.")
    parser.convert_arg_line_to_args = _line_to_args


    parser.add_argument(
        "-s", "--source", dest="source",
        help="Source site for file transfer.")

    parser.add_argument(
        "-w", "--workerdir", dest="workerdir",
        help="workers directory")

    parser.add_argument(
        "-t", "--template", dest="template",
        help="template file")

    parser.add_argument(
        "-p", "--prescript", dest="prescript",
        help="pre shell script")

    parser.add_argument(
        "-r", "--runid", dest="runid",
        help="runid of production")

    return parser
 


def writeDagFile(pipeline, templateFile, infile, workerdir, prescriptFile, runid):
    """
    Write Condor Dag Submission files. 
    """

    print "Writing DAG file "


    outname = pipeline + ".diamond.dag"
    mapname = pipeline + ".mapping"

    print outname

    mapObj = open(mapname,"w")
    outObj = open(outname,"w")

    outObj.write("JOB A "+workerdir+"/" + pipeline + ".pre\n"); 
    outObj.write("JOB B "+workerdir+"/" +  pipeline + ".post\n"); 
    outObj.write(" \n"); 

    outObj.write("PARENT A CHILD B \n"); 

    outObj.close()
    mapObj.close()


def main():
    print 'Starting generateDag.py'
    parser = makeArgumentParser(description=
        "generateDag.py write a Condor DAG for job submission"
        "by reading input list and writing the attribute as an argument.")
    print 'Created parser'
    ns = parser.parse_args()
    print 'Parsed Arguments'
    print ns

    # SA 
    # templateFile = "SourceAssoc-template.condor"
    # pipeline = "SourceAssoc"
    # infile   = "sky-tiles"

    # Pipeqa  
    # templateFile = "pipeqa-template.template"
    # pipeline = "pipeqa"
    # infile   = "visits-449"

    #   processCcdLsstSim
    pipeline = "S2012Pipe"
    #templateFile = "W2012Pipe-template.condor"
    #infile   = "9429-CCDs.input"

    writeDagFile(pipeline, ns.template, ns.source, ns.workerdir, ns.prescript, ns.runid )


    sys.exit(0)







if __name__ == '__main__':
    main()

