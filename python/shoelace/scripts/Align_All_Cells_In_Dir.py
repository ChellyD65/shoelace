#!/opt/python-2.7.1/bin/python
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
import glob
import pickle
import argparse
import re

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
parser.add_argument("-d", "--directory", help="Directory containing *.fastq files to align")
parser.add_argument("-r", "--reference", help="Path to reference to align to")

args, unknown = parser.parse_known_args()
bowtieargstring = ''
for i in unknown:
    bowtieargstring = bowtieargstring + ' ' + str(i)
bowtieargstring = bowtieargstring + ' ' 

"""
Setup directories, files
"""
inputDir = None; referenceFile = None
if args.directory:
    inputDir = args.directory
if args.reference:
    referenceFile = args.reference

if args.configfile:
    p = mmdConfig.Paths(args.configfile)
else:
    p = mmdConfig.Paths()
if not inputDir:
    print "No input directory argument specified.  Using fastq and virtual_fastq directories from configuration file."
    inputDir = [p.fastq_dir, p.virtual_fastq_dir]
if not referenceFile:
    print "No reference file directory argument specified.  Using reference file specified in configuration file."
    referenceFile = p.RefGenomeDir

"""
Find files, generate commands and submit jobs
"""
for idir in inputDir:
    inputFilenames_1 = glob.glob(os.path.join(idir,'*_1.fastq'))
    if (len(inputFilenames_1) < 1):
        inputFilenames_1 = glob.glob(os.path.join(idir,'*.fastq'))
        if (len(inputFilenames_1) > 0):
            singleEnd = True
        else:
            sys.exit("No FASTQ files found in directory: " + idir)
    else:
        inputFilenames_2 = []
        singleEnd = False
    outputFilenames = []
    for f1 in inputFilenames_1:
        if singleEnd:
            outputFilenames.append(re.sub('\.fastq','.sam', f1))
        else:
            outputFilenames.append(re.sub('_1\.fastq','.sam', f1))
            inputFilenames_2.append(re.sub('_1\.fastq','_2.fastq', f1))

    for i in range(len(inputFilenames_1)):
        print inputFilenames_1[i]
        print outputFilenames[i]
        if singleEnd:
            command_string = "bsub -q short -n 4 -W 12:00 -R \"rusage[mem=12000]\" -e ~/.lsbatch_errors -o lsf_output.txt \"{0} {1} {2} -n 0 -e 99999999 -l 25 -I 1 -X 2000 -a -m 15 {3} -S {4};\"".format(p.bowtie, p.RefGenomeDir, bowtieargstring, inputFilenames_1[i], outputFilenames[i])
        else:
            command_string = "bsub -q short -n 4 -W 12:00 -R \"rusage[mem=12000]\" -e ~/.lsbatch_errors -o lsf_output.txt \"{0} {1} {2} -n 0 -e 99999999 -l 25 -I 1 -X 2000 -a -m 15 -1 {3} -2 {4}, -S {5};\"".format(p.bowtie, p.RefGenomeDir, bowtieargstring, inputFilenames_1[i], inputFilenames_2[i], outputFilenames[i])
        try:
            os.system(command_string)
        except OSError:
            sys.exit("Command failed: " + command_string)
        print "Job {0}/{1} submitted for dir {2}".format(i+1,len(inputFilenames_1),idir)
        

