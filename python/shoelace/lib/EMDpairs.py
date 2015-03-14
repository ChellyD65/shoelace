#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 21 13:32:31 2014
@author: Chelly
"""

from __future__ import print_function
"""
import sys, os
import argparse
import glob
import numpy as np
import time 
import csv
import re
"""
import pyemd
from shoelace.lib import Utilities

class EMDpairs:

    def __init__(self):
        self.n = 0
        self.u = Utilities()

    def setup(self,filenames):
        
        """
        if self.saveAsPDF:
            pdffn = os.path.join(os.getcwd(), os.path.splitext(os.path.basename(__file__))[0] + "_run_" + timelabel + ".results.pdf")
            pp = PdfPages(pdffn)
            print("Saving plots to PDF: " + pdffn)

        mpl.rcParams['figure.figsize'] = (40.0, 60.0)
        fig, axes22 = plt.subplots(5, 3)
        """

        self.data = []
        for f in range(len(filenames)):
            d = np.load(filenames[f],'r')
            if normalizeByShuffled:
                tsel_r, tsel_v = self.u.get_tsel_both(d)
                tsel_r_norm = (tsel_r - np.mean(tsel_r, axis=0))/np.std(tsel_r, axis=0)
                tsel_v_norm = (tsel_v - np.mean(tsel_v, axis=0))/np.std(tsel_v, axis=0)
                self.data.append(tsel_r_norm - tsel_v_norm)
            else:
                if plot_virtual:
                    self.data.append(d['tsel_v'])
                else:
                    self.data.append(d['tsel_r'])

    def run(self):
        return 0

        
if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--loadfile",  help="Load a previous output *.npz file")
    parser.add_argument("--normalize", help="Normalize the real dataset by the shuffled dataset", default = False)
    parser.add_argument("--virtual",   help="Plot the virtual cells", default = False)
    parser.add_argument("--filelist",  help="Load previous output *.npz files from list passed on command line", nargs='+')
    args = parser.parse_args()


    if args.filelist:
        e = EMDpairs()
        t = time.strftime("%m_%d_%Y_-_%H_%M_%S")
        e.setup(args.filelist, t, bool(int(args.normalize)), bool(int(args.virtual)))
        print e.run()
        
    else:
        print("If calling this file directly, you must specify the \"--loadfile\" <path> or \"--filelist\" <files> argument with a path to the *.npz file containing the processed data.")
    
