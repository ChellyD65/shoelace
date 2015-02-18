#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 21 13:32:31 2014
@author: Chelly
"""

from __future__ import print_function
import sys, os
import argparse
import glob
import numpy as np
import time 
import csv
import re

from matplotlib import rc
rc('text', usetex=True)
rc('font',**{'family':'serif','serif':['Palatino']})
import matplotlib as mpl
mpl.use('Agg') # Don't use Xserver
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.backends.backend_pdf import PdfPages

from sklearn.decomposition import PCA
from sklearn import manifold
from sklearn.metrics import euclidean_distances
import scipy.cluster.hierarchy as sch
from scipy.spatial.distance import squareform,pdist    


class Plotter:

    def __init__(self):
        self.saveAsPDF = True

    def generateClusterPlots(self, filenames, timelabel='', normalizeByShuffled=False, plot_virtual=False):

        if self.saveAsPDF:
            pdffn = os.path.join(os.getcwd(), os.path.splitext(os.path.basename(__file__))[0] + "_run_" + timelabel + ".results.pdf")
            pp = PdfPages(pdffn)
            print("Saving plots to PDF: " + pdffn)

        mpl.rcParams['figure.figsize'] = (40.0, 60.0)
        fig, axes22 = plt.subplots(5, 3)

        for f in range(len(filenames)):
            d = np.load(filenames[f],'r')
            if normalizeByShuffled:
                tsel_r, tsel_v = self.get_tsel_both(d)
                tsel_r_norm = (tsel_r - np.mean(tsel_r, axis=0))/np.std(tsel_r, axis=0)
                tsel_v_norm = (tsel_v - np.mean(tsel_v, axis=0))/np.std(tsel_v, axis=0)
                a = tsel_r_norm - tsel_v_norm
            else:
                if plot_virtual:
                    a = d['tsel_v']
                else:
                    a = d['tsel_r']
            z = sch.linkage(a, method='ward')
            knee = np.diff(z[::-1, 2], 2)
            num_clust1 = knee.argmax() + 2
            part1 = sch.fcluster(z, num_clust1, 'maxclust')
#            similarities = euclidean_distances(a)
            similarities = squareform(pdist(a, metric='euclidean'))

            seed = np.random.RandomState(seed=3)
            mds = manifold.MDS(n_components=2, max_iter=3000, eps=1e-9, 
                  random_state=seed, dissimilarity="precomputed", n_jobs=1)
            pos = mds.fit(similarities).embedding_

            axes22[f][0].plot(range(1, len(z)+1), z[::-1, 2])
            axes22[f][0].plot(range(2, len(z)), knee)
            axes22[f][0].text(num_clust1, z[::-1, 2][num_clust1-1], '<- knee point')
            clr = ['#2200CC' ,'#D9007E' ,'#FF6600' ,'#FFCC00' ,'#ACE600' ,'#0099CC' ,
            '#8900CC' ,'#FF0000' ,'#FF9900' ,'#FFFF00' ,'#00CC01' ,'#0055CC']
            print("\n" + str(f) + ":" + str(len(set(part1))) + " clusters.")
            for cluster in set(part1):
                axes22[f][1].scatter(pos[part1 == cluster, 0], pos[part1 == cluster, 1], 
                               color=clr[cluster])
            plt.sca(axes22[f][2])
            sch.dendrogram(sch.linkage(a, method='ward'))
                
            axes22[f][2].set_title("Real Cells, hierarchical clustering (Ward linkage distance metric)")
            plt.xlabel('Cell number')
        if self.saveAsPDF:
            pp.savefig()
        else:
            plt.savefig(os.path.join(basedir,"real_sel" + "_run_" + timelabel + ".eps"), bbox_inches='tight')
        if self.saveAsPDF:
            pp.close()





    def generatePlots(self,dd,timelabel=''):
        # dd is the dictionary containing the variables to be plotted (e.g. locals(), loadedfile, etc.)
        if self.saveAsPDF:
            pdffn = os.path.join(os.getcwd(), os.path.splitext(os.path.basename(__file__))[0] + "_run_" + timelabel + ".results.pdf")
            pp = PdfPages(pdffn)
            print("Saving plots to PDF: " + pdffn)

        """
        genelabels = dd['sortedBioMartList'][dd['BioMartI']][dd['sortedIndex']] # The selected and sorted list of genes
        """

        # Fig 1 and 2 are normalized (Z-score) expression of genes x cells
        fig1 = plt.figure(1)
        a = dd['tsel_r']
        b = ((a.T-np.mean(a,1))/np.std(a,1)).T
        cax = plt.imshow(b,aspect='auto'); plt.title('Normalized Expression Levels in Real Cells')
        cax.get_axes().set_xlabel('Genes');  cax.get_axes().set_ylabel('Cells'); 
        cbar = fig1.colorbar(cax, ticks=np.round(np.arange(np.min(b),np.max(b),1)*2)/2)
        cbar.ax.set_yticklabels(map(str, np.round(np.arange(np.min(b),np.max(b),1)*2)/2))# vertically oriented colorbar
        cbar.set_label('Within cell z-score')
        if self.saveAsPDF:
            pp.savefig()
        else:
            plt.savefig(os.path.join(basedir,"real_sel" + "_run_" + timelabel + ".eps"), bbox_inches='tight')


        fig2 = plt.figure(2)
        a = dd['tsel_v']
        b = ((a.T-np.mean(a,1))/np.std(a,1)).T
        cax = plt.imshow(b,aspect='auto'); plt.title('Normalized Expression Levels in Virtual Cells')
        cax.get_axes().set_xlabel('Genes');  cax.get_axes().set_ylabel('Cells'); 
        cbar = fig2.colorbar(cax, ticks=np.round(np.arange(np.min(b),np.max(b),1)*2)/2)
        cbar.ax.set_yticklabels(map(str, np.round(np.arange(np.min(b),np.max(b),1)*2)/2))# vertically oriented colorbar
        cbar.set_label('Within cell z-score')
        if self.saveAsPDF:
            pp.savefig()
        else:
            plt.savefig(os.path.join(basedir,"virt_sel" + "_run_" + timelabel + ".eps"), bbox_inches='tight')


        # Fig 3 and 4 are cross correlation coefficients between genes (after projection onto first 5 PCAs and back)
        fig3 = plt.figure(3)
        fig3, ax = plt.subplots()
        cax = ax.imshow(dd['corrcoeff_real'],interpolation='nearest',aspect='auto',cmap=cm.coolwarm); ax.set_title('Correlation Coeffcient, n$_{PCA}=5$, Real Cells')
        cax.get_axes().set_xlabel('Genes'); cax.get_axes().set_ylabel('Genes');
        cbar = fig3.colorbar(cax, ticks=[-1, 0, 1])
        cbar.ax.set_yticklabels(['-1', '0', '1'])# vertically oriented colorbar
        if self.saveAsPDF:
            pp.savefig()
        else:
            plt.savefig(os.path.join(basedir,"corrcoef_real_sel" + "_run_" + timelabel + ".eps"), bbox_inches='tight')


        fig4 = plt.figure(4)
        fig4, ax = plt.subplots()
        cax = ax.imshow(dd['corrcoeff_virt'],interpolation='nearest',aspect='auto',cmap=cm.coolwarm); ax.set_title('Correlation Coeffcient, n$_{PCA}=5$, Virtual Cells')
        cax.get_axes().set_xlabel('Genes'); cax.get_axes().set_ylabel('Genes');
        cbar = fig4.colorbar(cax, ticks=[-1, 0, 1])
        cbar.ax.set_yticklabels(['-1', '0', '1'])# vertically oriented colorbar
        if self.saveAsPDF:
            pp.savefig()
        else:
            plt.savefig(os.path.join(basedir,"corrcoef_virt_sel" + "_run_" + timelabel + ".eps"), bbox_inches='tight')


        
        # Dendrograms showing clusters of cells
        fig5 = plt.figure(5)
        fig5, ax = plt.subplots()
        sch.dendrogram(d['real_dendro'])
        ax.set_title("Real Cells, hierarchical clustering (Ward linkage distance metric)")
        ax.set_ylim([0,500])
        plt.xlabel('Cell number')
        if self.saveAsPDF:
            pp.savefig()
        else:
            plt.savefig(os.path.join(basedir,"real_dendrogram" + "_run_" + timelabel + ".eps"), bbox_inches='tight')

        fig6 = plt.figure(5)
        fig6, ax = plt.subplots()
        sch.dendrogram(d['virt_dendro'])
        ax.set_title("Virtual Cells, hierarchical clustering (Ward linkage distance metric)")
        ax.set_ylim([0,500])
        plt.xlabel('Cell number')
        if self.saveAsPDF:
            pp.savefig()
        else:
            plt.savefig(os.path.join(basedir,"virt_dendrogram" + "_run_" + timelabel + ".eps"), bbox_inches='tight')

        ############################################################################################################
        if self.saveAsPDF:
            pp.close()

    def get_tsel_both(self, d, threshold=None):
        tpm_r  = np.log2(d['tpm_real_s']+1)
        tpm_v  = np.log2(d['tpm_virt_s']+1)
        tsel_r = tpm_r[:,d['i_grThresh_both']] 
        tsel_v = tpm_v[:,d['i_grThresh_both']]
        return tsel_r, tsel_v

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--loadfile",  help="Load a previous output *.npz file")
    parser.add_argument("--normalize", help="Normalize the real dataset by the shuffled dataset", default = False)
    parser.add_argument("--virtual",   help="Plot the virtual cells", default = False)
    parser.add_argument("--filelist",  help="Load previous output *.npz files from list passed on command line", nargs='+')
    args = parser.parse_args()



    if args.loadfile:
        if os.path.isfile(args.loadfile):
            d_load = np.load(args.loadfile)
            print("Loading previous results from file: " + args.loadfile)
            d = dict()
            for dk in d_load.keys():
                d[dk] = d_load[dk]
            d_load.close()
            print("Generating plots")
            timelabel = time.strftime("%m_%d_%Y_-_%H_%M_%S")
            p = Plotter()
            p.saveAsPDF = True
            p.generatePlots(d, timelabel)



    if args.filelist:
        p = Plotter()
        p.saveAsPDF = True
        t = time.strftime("%m_%d_%Y_-_%H_%M_%S")
        p.generateClusterPlots(args.filelist, t, bool(int(args.normalize)), bool(int(args.virtual)))

    else:
        print("If calling this file directly, you must specify the \"--loadfile\" <path> or \"--filelist\" <files> argument with a path to the *.npz file containing the processed data.")
    
