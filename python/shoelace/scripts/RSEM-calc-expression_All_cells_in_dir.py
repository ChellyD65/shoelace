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
rsemargstring = ''
for i in unknown:
    rsemargstring = rsemargstring + ' ' + str(i)
rsemargstring = rsemargstring + ' '



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


convert_command = os.path.join(p.rsem_dir,'convert-sam-for-rsem')
rsem_command = os.path.join(p.rsem_dir,'rsem-calculate-expression')

for idir in inputDir:
    inputFilenames_1 = glob.glob(os.path.join(idir,'*_1.fastq'))
    if (len(inputFilenames_1) < 1):
        inputFilenames_1 = glob.glob(os.path.join(idir,'*.fastq'))
        if (len(inputFilenames_1) > 0):
            singleEnd = True
        else:
            print("No FASTQ files found in directory: " + idir + ". Assuming single-end reads")
            singleEnd = True
    else:
        singleEnd = False
    inputSAMfilenames = glob.glob(os.path.join(idir,'*.sam'))
    for i in range(len(inputSAMfilenames)):
        out_rsem = re.sub('\.sam','_rsem',inputSAMfilenames[i])
        out_bam  = re.sub('\.sam','.bam',inputSAMfilenames[i])
        out_expression = re.sub('\.sam','_expression',inputSAMfilenames[i])
        print inputSAMfilenames[i]
        if singleEnd:
            command_string = "bsub -q short -n 6 -W 12:00 -e ~/.lsbatch_errors_rsem -o lsf_output.txt \"{0} {1} {2}; {3} {4} --bam {5} {6} {7}\"".format(convert_command, inputSAMfilenames[i], out_rsem, rsem_command, rsemargstring, out_bam, referenceFile, out_expression)
        else:
            command_string = "bsub -q short -n 6 -W 12:00 -e ~/.lsbatch_errors_rsem -o lsf_output.txt \"{0} {1} {2}; {3} {4} --bam --paired-end {5} {6} {7}\"".format(convert_command, inputSAMfilenames[i], out_rsem, rsem_command, rsemargstring, out_bam, referenceFile, out_expression)

        try:
            os.system(command_string)
        except OSError:
            sys.exit("Command failed: " + command_string)
        print "Job {0}/{1} submitted for dir {2}".format(i+1,len(inputFilenames_1),idir)
        







