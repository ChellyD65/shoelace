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
        self.inputFilenames = glob.glob(os.path.join(self.p.fastq_dir,'*_1.fastq'))
        if (len(self.inputFilenames) < 1):
            self.inputFilenames = glob.glob(os.path.join(self.p.fastq_dir,'*.fastq'))
            self.singleEnd = True
        else:
            self.singleEnd = False
        self.ReadFileLens()
        
    def run(self):
        print "%d line counts found in file." % len(self.linecounts)
        print "%d input files found." % len(self.inputFilenames)
        self.OpenOutputFiles(len(self.linecounts))
        c = 0
        for f in self.inputFilenames:
            f1 = f
            if1 = open(f1,'r')
            if not self.singleEnd:
                f2 = re.sub('_1\.fastq','_2.fastq', f1)
                if2 = open(f2,'r')
            while 1:
                read1 = []
                for i in range(0,4):
                    line1 = if1.readline()
                    read1.append(line1)
                if not self.singleEnd:
                    read2 = []
                    for i in range(0,4):
                        line2 = if2.readline()
                        read2.append(line2)
                else:
                    line2 = True
                if not line1 or not line2:
                    break
                else:
                    fn = self.ChooseOutputFile()
                    for i in range(0,4):
                        self.outfileHandles_1[fn].write(read1[i])
                        if not self.singleEnd:
                            self.outfileHandles_2[fn].write(read2[i])
            c = c + 1
            print "Done reading file %s. [%d/%d]"  % f, c, len(self.inputFilenames)
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
            print "Counting lines in FASTQ files, using system call to wc -l"
            try:
                os.system("wc -l " + os.path.join(self.p.fastq_dir,"*.fastq") + " > " + fname)
            except OSError:
                print "Counting lines in fastq files with wc failed."
                return -1
        print "Reading line counts for FASTQ files from " + fname
        if self.singleEnd:
            self.linecounts = np.genfromtxt(fname, delimiter=" ")[:-1:1,0]
        else:
            self.linecounts = np.genfromtxt(fname, delimiter=" ")[:-1:2,0]
        self.fileChooserIndex = np.cumsum(self.linecounts/(max(1,np.std(self.linecounts))))
        
    def ChooseOutputFile(self):
        roll = np.random.rand()*np.max(self.fileChooserIndex)
        return np.min(np.nonzero(self.fileChooserIndex>roll))
        
    def OpenOutputFiles(self, n=4, pairedEndFiles=True):
        self.outfileHandles_1 = []
        if not self.singleEnd:
            self.outfileHandles_2 = []
        for i in range(1,n+1):
            if not self.singleEnd:
                self.outfileHandles_1.append(open(os.path.join(self.p.virtual_fastq_dir,"mmdVirtualCell_%03d_1.fastq" % i),'w+'))
                self.outfileHandles_2.append(open(os.path.join(self.p.virtual_fastq_dir,"mmdVirtualCell_%03d_2.fastq" % i),'w+'))
            else:
                self.outfileHandles_1.append(open(os.path.join(self.p.virtual_fastq_dir,"mmdVirtualCell_%03d.fastq" % i),'w+'))

    def CloseOutputFiles(self, pairedEndFiles=True):
        for i in self.outfileHandles_1:
            i.close()
        if pairedEndFiles:
            for i in self.outfileHandles_2:
                i.close()
    
    def CreateVirtualCellsFromAllReadsMerged(self, n=430, pairedEndFiles=True):
        print "Writing virtual cells."
        INFILE1 = os.path.join(self.virtual_fastq_dir, "AllReads_Merged_1.fastq")
        if pairedEndFiles:
            INFILE2 = os.path.join(self.virtual_fastq_dir, "AllReads_Merged_2.fastq")
        print "Total number of reads: " + str(TotalReads)
        return 0

















    
