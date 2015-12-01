#!/usr/bin/env python
"""
Created on Thurs, 9/04/2014

@author: mdistasio
"""

# Python modules
import sys
import os
import subprocess
import numpy as np
import matplotlib.pyplot as plt
import glob
import argparse

# mmd Library of functions
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))
from shoelace.lib import mmdConfig # as mmdConfig
from shoelace.lib import FileLoader #as FileLoader
from shoelace.lib import Shuffler #as Shuffler


"""
Main Function
"""
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

print "Running Python version {0}.{1}".format(sys.version_info[0],sys.version_info[1])


## ----------------------------------------------------------------------------------------------------
# Evry dey 'm shuffle-in

SH = Shuffler.Shuffler(p)
SH.setup()
SH.run()

print "Shuffling completed! New files are in: " + p.virtual_fastq_dir

