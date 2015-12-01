#!/usr/bin/env python
"""
Created on Thurs, 9/04/2014
@author: mdistasio
"""

"""
import modules
"""
# Python modules
import sys
import os
import subprocess
import numpy as np
import matplotlib.pyplot as plt
import glob
import pickle
import argparse

# mmd Library of functions
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))
from shoelace.lib import mmdConfig
from shoelace.lib import FileLoader #as FileLoader
from shoelace.lib import Shuffler #as Shuffler
from shoelace.lib import GetGzippedFromServer as GZFS
from shoelace.lib import columnize

print "Running Python version {0}.{1}".format(sys.version_info[0],sys.version_info[1])
console_height, console_width = map(int, os.popen('stty size', 'r').read().split())

"""
Parse command line options
"""
parser = argparse.ArgumentParser()
parser.add_argument("--configfile", help="Path to configuration file")
args = parser.parse_args()

"""
Set up data directories
"""
if args.configfile:
    p = mmdConfig.Paths(args.configfile)
else:
    p = mmdConfig.Paths()
SeriesMetadataDir = p.SeriesMetadataDir 
if not os.path.isdir(SeriesMetadataDir):
    os.makedirs(SeriesMetadataDir)

"""
Load the series matrix 
This gives the GEO accession numbers for all samples, and their descriptions
"""
SM_file = os.path.join(SeriesMetadataDir,os.path.split(p.GEO_SeriesMatrixURL)[1])
if not(os.path.exists(SM_file)):
    if not os.path.exists(SeriesMetadataDir):
        os.makedirs(SeriesMetadataDir)
    G =  GZFS.GetGZippedFromServer()
    G.getunzipped(p.GEO_SeriesMatrixURL, SM_file)
else:
    print os.path.split(SM_file)[1] + " found."

"""
Parse the series matrix, to get the accession numbers of the cells of interest
"""
FL = FileLoader.FileLoader(p) # pass FileLoader the Paths object so it knows where to put stuff
sm = FL.parse_series_matrix(SM_file)
choice, exclude = FL.choosefromdict(sm)

print "\n\n\nRecords will be downloaded that INCLUDE"
print "---------------------------------------"
for key in choice.keys():
    print "\n" + key + "  :"
    for val in choice[key]:
        print "\t" + val

print "\n\n\nbut EXCLUDE"
print "------------"
for key in exclude.keys():
    print "\n" + key + "  :"
    for val in exclude[key]:
        print "\t" + val

"""
Determine the GEO accession numbers from the Series Matrix
"""
GEOAccNums, icoi = FL.choose_cell_records(sm,choice,exclude)
f1 = os.path.splitext(SM_file)[0] + ".p"
fff = open(os.path.join(SeriesMetadataDir, f1), "wb")
pickle.dump([sm, GEOAccNums, icoi], fff)
fff.close()
print("Saved pickled object file: " + os.path.join(SeriesMetadataDir, f1))

"""
Retrieve the FASTQ files from the server
"""
print("Dumping FASTQ files to local dir: " + FL.p.fastq_dir )
for a in GEOAccNums:
    FL.fastq_dump(a)


