#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 21 13:32:31 2014
@author: Chelly
"""

from __future__ import print_function
"""
import glob
import csv
import re
"""
import sys, os
import numpy as np
import time 
import argparse
from pyemd import emd
from sklearn.metrics import euclidean_distances
import Utilities

from matplotlib import rc
rc('text', usetex=True)
rc('font',**{'family':'serif','serif':['Palatino']})
import matplotlib as mpl
mpl.use('Agg') # Don't use Xserver
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.backends.backend_pdf import PdfPages


class EMDpairs:

    def __init__(self):
        self.n = 0
        self.u = Utilities.Utilities()
        self.saveAsPDF = True

    def setup(self,filenames, normalizeByShuffled, virtualOnly):
        

        self.data = []
        for f in range(len(filenames)):
            d = np.load(filenames[f],'r')
            if normalizeByShuffled:
                tsel_r, tsel_v = self.u.get_tsel_both(d)
                tsel_r_norm = (tsel_r - np.mean(tsel_r, axis=0))/np.std(tsel_r, axis=0)
                tsel_v_norm = (tsel_v - np.mean(tsel_v, axis=0))/np.std(tsel_v, axis=0)
                self.data.append(tsel_r_norm - tsel_v_norm)
            else:
                if virtualOnly:
                    self.data.append(d['tsel_v'])
                else:
                    self.data.append(d['tsel_r'])
            print(self.data[-1].shape)

    def run(self):


        if self.saveAsPDF:
            timelabel = time.strftime("%m_%d_%Y_-_%H_%M_%S")
            pdffn = os.path.join(os.getcwd(), os.path.splitext(os.path.basename(__file__))[0] + "_run_" + timelabel + ".results.pdf")
            pp = PdfPages(pdffn)
            print("Saving plots to PDF: " + pdffn)

        mpl.rcParams['figure.figsize'] = (40.0, 60.0)
        fig, axes = plt.subplots(len(self.data))

        f = 0
        for tumor_set in self.data:
            histog = np.apply_along_axis(lambda x: np.histogram(x,256)[0], 1, tumor_set)
            em = self.emd_allrows(histog)

            """
            Next, should sort rows of em by their sums, to look nice
            """


            cax = axes[f].imshow(em,aspect='equal');
            cbar = plt.colorbar(cax, ticks=np.round(np.arange(np.min(em),np.max(em),100)*2)/2)
            cbar.ax.set_yticklabels(map(str, np.round(np.arange(np.min(em),np.max(em),100)*2)/2))# vertically oriented colorbar
            cbar.set_label('EMD over gene expression distribution')

            f=f+1

        if self.saveAsPDF:
            pp.savefig()
        pp.close()
        return 0

    

    def emd_allrows(self,M):
        M = M.astype('float')
        EMDout = np.empty([M.shape[0],M.shape[0]])
        d = np.ones([M.shape[1],M.shape[1]])
        rr = 0
        for r in M:
            a = np.apply_along_axis(emd, 1, M, r, d)
            EMDout[rr,:] = a.T; rr=rr+1
        return EMDout
        

        
if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--loadfile",  help="Load a previous output *.npz file")
    parser.add_argument("--normalize", help="Normalize the real dataset by the shuffled dataset", default = False)
    parser.add_argument("--virtual",   help="Plot the virtual cells", default = False)
    parser.add_argument("--filelist",  help="Load previous output *.npz files from list passed on command line", nargs='+')
    args = parser.parse_args()


    if args.filelist:
        e = EMDpairs()
#        t = time.strftime("%m_%d_%Y_-_%H_%M_%S")
        e.setup(args.filelist, bool(int(args.normalize)), bool(int(args.virtual)))
        print(e.run())


        
    else:
        print("If calling this file directly, you must specify the \"--loadfile\" <path> or \"--filelist\" <files> argument with a path to the *.npz file containing the processed data.")
    
