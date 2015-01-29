#!/usr/bin/env python
#####!/opt/python-2.7.1/bin/python
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

# mmd Library of functions
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))
from shoelace.lib import mmdConfig # as mmdConfig
from shoelace.lib import FileLoader #as FileLoader
from shoelace.lib import Shuffler #as Shuffler


"""
Main Function
"""
p = mmdConfig.Paths()
print "Running Python version {0}.{1}".format(sys.version_info[0],sys.version_info[1])


## ----------------------------------------------------------------------------------------------------
# Evry dey 'm shuffle-in

SH = Shuffler.Shuffler(p)
SH.setup()
SH.run()

