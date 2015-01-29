"""
Created on Thurs, 9/04/2014

@author: mdistasio

Uses BioPython
"""

import os
import glob
import math
import random
import re
import numpy as np
import itertools
import subprocess

class Shuffler:

    def __init__(self, p):
        #p = Paths object (from mmdSetPaths.py)
        np.set_printoptions(suppress=True)
        np.random.seed(10081981)
        self.p = p  

    def setup(self):
        self.ReadFileLens()
        
    def run(self):
        inputFilenames = glob.glob(os.path.join(self.p.fastq_dir,'*_1.fastq'))
        print "%d line counts found." % len(self.linecounts)
        print "%d input files found." % len(inputFilenames)

        self.OpenOutputFiles(len(self.linecounts))
        for f in inputFilenames:
            f1 = f
            f2 = re.sub('_1\.fastq','_2.fastq', f1)
            if1 = open(f1,'r')
            if2 = open(f2,'r')
            while 1:
                read1 = []
                for i in range(0,4):
                    line1 = if1.readline()
                    read1.append(line1)
                read2 = []
                for i in range(0,4):
                    line2 = if2.readline()
                    read2.append(line2)
                if not line1 or not line2:
                    break
                else:
                    fn = self.ChooseOutputFile()
                    for i in range(0,4):
                        self.outfileHandles_1[fn].write(read1[i])
                        self.outfileHandles_2[fn].write(read2[i])

            print "Done reading file %s."  % f


        
        self.CloseOutputFiles()
        
    def file_len(self, fname):
        with open(fname) as f:
            i = -1
            for i, l in enumerate(f):
                pass
            return i + 1

    def ReadFileLens(self, fname=0):
        # This function takes a file of line counts.
        # Generate it with:
        #   'wc -l *.fastq > FASTQ_linecounts.txt'
        if fname == 0:
            fname = os.path.join(self.p.fastq_dir, "FASTQ_linecounts.txt")
        if not os.path.exists(fname):
            try:
                os.system("wc -l " + os.path.join(self.p.fastq_dir,"*.fastq") + " > " + fname)
            except OSError:
                print "Counting lines in fastq files with wc failed."
                return -1
        print "Reading line counts for FASTQ files from " + fname
        self.linecounts = np.genfromtxt(fname, delimiter=" ")[:-1:2,0]
        self.fileChooserIndex = np.cumsum(self.linecounts/(max(1,np.std(self.linecounts))))
        
    def ChooseOutputFile(self):
        roll = np.random.rand()*np.max(self.fileChooserIndex)
        return np.min(np.nonzero(self.fileChooserIndex>roll))
        
    def OpenOutputFiles(self, n=4):
        self.outfileHandles_1 = []
        self.outfileHandles_2 = []
        for i in range(1,n+1):
            self.outfileHandles_1.append(open(os.path.join(self.p.virtual_fastq_dir,"mmdVirtualCell_%03d_1.fastq" % i),'w+'))
            self.outfileHandles_2.append(open(os.path.join(self.p.virtual_fastq_dir,"mmdVirtualCell_%03d_2.fastq" % i),'w+'))
        

    def CloseOutputFiles(self):
        for i in self.outfileHandles_1:
            i.close()
        for i in self.outfileHandles_2:
            i.close()
    


    def CreateVirtualCellsFromAllReadsMerged(self, n=430):
        print "Writing virtual cells."
        INFILE1 = os.path.join(self.virtual_fastq_dir, "AllReads_Merged_1.fastq")
        INFILE2 = os.path.join(self.virtual_fastq_dir, "AllReads_Merged_2.fastq")
        print "Total number of reads: " + str(TotalReads)

        return 0

















    
