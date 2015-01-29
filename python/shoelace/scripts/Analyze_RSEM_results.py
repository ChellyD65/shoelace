#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 09 22:22:35 2014

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
import scipy.cluster.hierarchy as sch





def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [ atoi(c) for c in re.split('(\d+)', text )]

def loadDataSet(directory):
    print(directory)
    nfl = len(glob.glob(os.path.join(directory,'*.genes.results')))
    if nfl > 0:
        a = np.zeros((nfl,28516));
        filenum = 0
        zz=1
        for filename in glob.glob(os.path.join(directory,'*.genes.results')):
            print(filename)
            dset = np.genfromtxt(filename)[1:,6]
            a[filenum,:] = dset
            if zz==1:
                genenames = np.genfromtxt(filename, usecols=0, dtype=str)[1:];
                zz=0
                print("Loaded gene names from file: " + filename + ": ")
            print(filenum); filenum=filenum+1;
        return a, genenames
    else:
        print("No filenames found matching \'*.genes.results\' in directory: " + directory)




def sortGenes(genenames):
    """
    Sorting based on chromosome and position, using BioMart hg38 index
    """
    GeneName=[]
    Chromosome=[]
    Start=[]
    Stop=[]
    with open('BioMart_HumanGenome38.txt','r') as f:
        next(f) # skip headings
        reader=csv.reader(f,delimiter='\t')
        for a,b,c,d in reader:
            GeneName.append(a)
            Chromosome.append(atoi(b))
            Start.append(c)
            Stop.append(d)

    sortedBioMartList = sorted(zip(GeneName,Chromosome,Start,Stop), key=lambda element: (element[1], element[2]))
    G = zip(*sortedBioMartList)[0]
    print("Sorted " + str(len(G)) + " genes by (Chromosome, Start Position) in BioMart Dataset.")

    # Get the index list to sort the genes in the dataset based on G (the BioMart list)
    # BioMartI = map(lambda x: (G.index(x) if x in G else None), genenames)
    BioMartI = []
    sri = []
    i = 0 
    for x in genenames:
        if (x in G):
            BioMartI.append(G.index(x))
            sri.append(i)
        i=i+1
    inds = np.argsort(BioMartI)
    sortedIndex = np.array(sri)[inds]
    #sortedIndex = np.array(sorted(sri, key = lambda x: BioMartI[x]))
            
    # Now the sorted index into the list of genenames
    #    sortedIndex = sorted(range(0,len(genenames)), key=lambda x: BioMartI[x])
    return (sortedBioMartList,BioMartI,sortedIndex)



def generatePlots(dd,timelabel):
    # dd is the dictionary containing the variables to be plotted (e.g. locals(), loadedfile, etc.)
    print("Generating plots.")
    saveAsPDF = 1
    if saveAsPDF:
#        pdffn = os.path.join(basedir,"Results" + "_run_" + timelabel + ".pdf")
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
    if saveAsPDF:
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
    if saveAsPDF:
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
    if saveAsPDF:
        pp.savefig()
    else:
        plt.savefig(os.path.join(basedir,"corrcoef_real_sel" + "_run_" + timelabel + ".eps"), bbox_inches='tight')



    fig4 = plt.figure(4)
    fig4, ax = plt.subplots()
    cax = ax.imshow(dd['corrcoeff_virt'],interpolation='nearest',aspect='auto',cmap=cm.coolwarm); ax.set_title('Correlation Coeffcient, n$_{PCA}=5$, Virtual Cells')
    cax.get_axes().set_xlabel('Genes'); cax.get_axes().set_ylabel('Genes');
    cbar = fig4.colorbar(cax, ticks=[-1, 0, 1])
    cbar.ax.set_yticklabels(['-1', '0', '1'])# vertically oriented colorbar
    if saveAsPDF:
        pp.savefig()
    else:
        plt.savefig(os.path.join(basedir,"corrcoef_virt_sel" + "_run_" + timelabel + ".eps"), bbox_inches='tight')


    fig5 = plt.figure(5)
    fig5, ax = plt.subplots()
    sch.dendrogram(d['real_dendro'])
    ax.set_title("Real Cells, hierarchical clustering (Ward linkage distance metric)")
    plt.xlabel('Cell number')
    if saveAsPDF:
        pp.savefig()
    else:
        plt.savefig(os.path.join(basedir,"real_dendrogram" + "_run_" + timelabel + ".eps"), bbox_inches='tight')

    fig6 = plt.figure(5)
    fig6, ax = plt.subplots()
    sch.dendrogram(d['virt_dendro'])
    ax.set_title("Virtual Cells, hierarchical clustering (Ward linkage distance metric)")
    plt.xlabel('Cell number')
    if saveAsPDF:
        pp.savefig()
    else:
        plt.savefig(os.path.join(basedir,"virt_dendrogram" + "_run_" + timelabel + ".eps"), bbox_inches='tight')



    if saveAsPDF:
        pp.close()
    #End of generatePlots



"""
--------------------------------------------------------------------------------------------------------------------------------
Main Function ------------------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------------------------------
"""
timelabel = time.strftime("%m_%d_%Y_-_%H_%M_%S")

"""
Parse command line arguments
"""

parser = argparse.ArgumentParser()
parser.add_argument("-l", "--log", help="Log messages to a file", default=0)
parser.add_argument("-o", "--out", help="Save output to file(s) (default 1)", default=True)
parser.add_argument("--loadfile", help="Load a previous output *.npz file")
parser.add_argument("--basedir", help="Directory containing two subdirs \'fastq\' and \'fastq_virtual\', which contain *.genes.results output from RSEM", default=os.path.dirname(os.path.realpath(__file__)))
parser.add_argument("-t", "--threshold", help="Threshold for log2(TPMs), averaged over all cells. (default 3)", default=3)
parser.add_argument("--threshold_r", help="Threshold for log2(TPMs), averaged over all REAL cells. (default None)", default=None)
parser.add_argument("--threshold_v", help="Threshold for log2(TPMs), averaged over all VIRTUAL cells. (default None)", default=None)
args = parser.parse_args()
lg = 0 # Logging on/off
if args.log == 1:
    lg = 1
    logFilename = os.path.join(os.getcwd(), os.path.splitext(os.path.basename(__file__))[0] + "_run_" + timelabel + ".log")
    print("Logging to file: " + logFilename)
    logFile = open(logFilename,'w')

if os.path.isdir(args.basedir):
    basedir=args.basedir
else:
    print("Data directory not found: " + args.basedir)
    sys.exit()
    

d = dict()
if args.loadfile:
    if os.path.isfile(args.loadfile):
        d_load = np.load(args.loadfile)
        print("Loading previous results from file: " + args.loadfile)
        for dk in d_load.keys():
            d[dk] = d_load[dk]
        d_load.close()

args.out = bool(args.out)
if (args.out==True):
    outFileName = os.path.join(os.getcwd(), os.path.splitext(os.path.basename(__file__))[0] + "_run_" + timelabel + ".out")
    print("Saving output to: " + outFileName)





"""
Loading Data
"""
if not (all (k in d.keys() for k in ('genenames_real', 'tpm_real_s','tpm_virt_s'))):
    # Real cells
    if os.path.isfile(os.path.join(basedir, 'real_TPMs.npz')):
        print("Found file " + os.path.join(basedir, 'real_TPMs.npz') + ". Loading...")
        loadedfile = np.load(os.path.join(basedir, 'real_TPMs.npz'))
        tpm_real = loadedfile['tpm_real']
        genenames_real = loadedfile['genenames_real']
    else:
        tpm_real, genenames_real = loadDataSet(os.path.join(basedir,'fastq'))
        np.savez(os.path.join(basedir, 'real_TPMs'),tpm_real=tpm_real, genenames_real=genenames_real)
    d['genenames_real'] = genenames_real

    # Virtual cells
    if os.path.isfile(os.path.join(basedir, 'virt_TPMs.npz')):
        print("Found file " + os.path.join(basedir, 'virt_TPMs.npz') + ". Loading...")
        loadedfile = np.load(os.path.join(basedir, 'virt_TPMs.npz'))
        tpm_virt = loadedfile['tpm_virt']
        genenames_virt = loadedfile['genenames_virt']
    else:
        tpm_virt, genenames_virt = loadDataSet(os.path.join(basedir,'fastq_virtual'))
        np.savez(os.path.join(basedir, 'virt_TPMs'),tpm_virt=tpm_virt, genenames_virt=genenames_virt)


if lg:
    print(str(len(genenames_real)) + " gene names found in real.", file=logFile)
    print(str(len(genenames_virt)) + " gene names found in virtual.\n\n", file=logFile)



"""
Get sorting indices based on hg38 as annotated in BioMart
"""
if  not (all (k in d.keys() for k in ('sortedBioMartList', 'BioMartI', 'sortedIndex'))):
    d['sortedBioMartList'], d['BioMartI'], d['sortedIndex'] = sortGenes(genenames_real)
if lg:
    print("Index of genes in BioMart (BioMartI)\n", file=logFile)
    print(d['BioMartI'], file=logFile)
    print("\n\n\n", file=logFile)
    print("Sorting index of genes in dataset (sortedIndex)\n", file=logFile)
    print(d['sortedIndex'], file=logFile)
    print("\n\n\n", file=logFile)

# Sort the records by chromosome order
if  not (all (k in d.keys() for k in ('tpm_real_s','tpm_virt_s'))):
    d['tpm_real_s'] = tpm_real[:,d['sortedIndex']]
    d['tpm_virt_s'] = tpm_virt[:,d['sortedIndex']]


# Log2 transform and select only the genes with average expression (across all cells) > threshold
if  not (all (k in d.keys() for k in ('tsel_r', 'tsel_v', 'i_grThresh_r', 'i_grThresh_v'))):
    if args.threshold_r:
        threshold = float(args.threshold_r)
    else:
        threshold = float(args.threshold)
    print("thresholding real cells: log2(TPM) > " + str(threshold) + "...",)
    tpm_r  = np.log2(d['tpm_real_s']+1)
    avg_tpm_r = np.mean(tpm_r, axis=0)
    d['i_grThresh_r'] = np.where(avg_tpm_r > threshold)[0]
    d['tsel_r'] = tpm_r[:,d['i_grThresh_r']] 

    if args.threshold_v:
        threshold = float(args.threshold_v)
    else:
        threshold = float(args.threshold)
    print("thresholding virtual cells: log2(TPM) > " + str(threshold) + "...",)
    tpm_v  = np.log2(d['tpm_virt_s']+1)
    avg_tpm_v = np.mean(tpm_v, axis=0)
    d['i_grThresh_v'] = np.where(avg_tpm_v > threshold)[0]
    d['tsel_v'] = tpm_v[:, d['i_grThresh_v']] 

    d['i_grThresh_both'] = np.union1d(d['i_grThresh_r'],d['i_grThresh_v'])

print("Found " + str(d['tsel_r'].shape[1]) + " genes for real, " + str(d['tsel_v'].shape[1]) + " genes for virtual.")


"""
Principal Components Analysis and Correlation to define modules
"""
if  not (all (k in d.keys() for k in ('corrcoeff_real', 'corrcoeff_virt'))):
    print("Projecting onto first 5 Principal components...")
    sklearn_pca = PCA(n_components=5)
    sklearn_transf_r = sklearn_pca.fit_transform(d['tsel_r'])
    A_r = sklearn_pca.inverse_transform(sklearn_transf_r)
    sklearn_transf_v = sklearn_pca.fit_transform(d['tsel_v'])
    A_v = sklearn_pca.inverse_transform(sklearn_transf_v)

    # Cross correlation
    ### I,J = np.array(list(combinations(np.arange(A.shape[1]),2))).T
    print("Computing pairwise cross correlation matrices...")
    d['corrcoeff_real'] = np.zeros((A_r.shape[1],A_r.shape[1]))
    d['corrcoeff_virt'] = np.zeros((A_v.shape[1],A_v.shape[1]))

    pnc=0
    for I in np.arange(0,A_r.shape[1]):
        if (pnc==100):
            print("Gene " + str(I) + " of " + str(A_r.shape[1]) + " for real")
            pnc = 0
        pnc=pnc+1
        for J in np.arange(I,A_r.shape[1]):
            #            if J >= I:
            d['corrcoeff_real'][I,J] = np.corrcoef(A_r[:,I],A_r[:,J])[0,1]
    pnc=0
    for I in np.arange(0,A_v.shape[1]):
        if (pnc==100):
            print("Gene " + str(I) + " of " + str(A_v.shape[1]) + " for virtual")
            pnc = 0
        pnc=pnc+1
        for J in np.arange(I,A_v.shape[1]):
            #            if J >= I:
            d['corrcoeff_virt'][I,J] = np.corrcoef(A_v[:,I],A_v[:,J])[0,1]

# Find highest and Lowest correlated genes
if not (all (k in d.keys() for k in ('corr_sorted_real_i', 'corr_sorted_virt_i'))):
    print("Computing highest and lowest correlations among genes...")
    cr=d['corrcoeff_real']
    cv=d['corrcoeff_virt']
    #    l = np.unravel_index(np.array(sorted(range(0,cr.size), key=lambda x: cr.ravel()[x])),cr.shape)
    l = np.unravel_index(np.argsort(cr.ravel()),cr.shape)
    d['corr_sorted_real_i'] = np.array(l).T
    #    l = np.unravel_index(np.array(sorted(range(0,cv.size), key=lambda x: cv.ravel()[x])),cv.shape)
    l = np.unravel_index(np.argsort(cv.ravel()),cv.shape)
    d['corr_sorted_virt_i'] = np.array(l).T




"""
Get top and bottom most correlated genes
"""
ntopbot = 100
d['corr_real_top_i'] = d['corr_sorted_real_i'][(-d['corrcoeff_real'].shape[0]-ntopbot-1):(-d['corrcoeff_real'].shape[0]-1),:] #highest correlation
d['corr_virt_top_i'] = d['corr_sorted_virt_i'][(-d['corrcoeff_virt'].shape[0]-ntopbot-1):(-d['corrcoeff_virt'].shape[0]-1),:]
d['corr_real_bot_i'] = d['corr_sorted_real_i'][0:ntopbot] #lowest correlation
d['corr_virt_bot_i'] = d['corr_sorted_virt_i'][0:ntopbot]

kr=(d['genenames_real'][d['sortedIndex']])[d['i_grThresh_r']] # Just the gene names still in use
kv=(d['genenames_real'][d['sortedIndex']])[d['i_grThresh_v']]
topnames_r = kr[d['corr_real_top_i']]
topnames_v = kv[d['corr_virt_top_i']]
botnames_r = kr[d['corr_real_bot_i']]
botnames_v = kv[d['corr_virt_bot_i']]

# Count up instances, forming histograms
topnames_r_hist = dict((x, list(topnames_r.ravel()).count(x)) for x in list(topnames_r.ravel())) 
topnames_v_hist = dict((x, list(topnames_v.ravel()).count(x)) for x in list(topnames_v.ravel()))
botnames_r_hist = dict((x, list(botnames_r.ravel()).count(x)) for x in list(botnames_r.ravel()))
botnames_v_hist = dict((x, list(botnames_v.ravel()).count(x)) for x in list(botnames_v.ravel())) 
# Sort the histograms in descending order
d['topnames_r_hist'] = sorted(topnames_r_hist.items(),key=lambda x: x[1], reverse=True)
d['topnames_v_hist'] = sorted(topnames_v_hist.items(),key=lambda x: x[1], reverse=True)
d['botnames_r_hist'] = sorted(botnames_r_hist.items(),key=lambda x: x[1], reverse=True)
d['botnames_v_hist'] = sorted(botnames_v_hist.items(),key=lambda x: x[1], reverse=True)




"""
Hierarchical Clustering
"""
print("Ward Agglomerative clustering")
d['real_dendro'] = sch.linkage(d['tsel_r'], method='ward')
d['virt_dendro'] = sch.linkage(d['tsel_v'], method='ward')
print("Done")




"""
Output
"""
if (args.out==True):
    np.savez(outFileName,
             genenames_real=d['genenames_real'],
             tpm_real_s=d['tpm_real_s'],
             tpm_virt_s=d['tpm_virt_s'],
             tsel_r=d['tsel_r'],
             tsel_v=d['tsel_v'],
             sortedBioMartList=d['sortedBioMartList'],
             BioMartI=d['BioMartI'],
             sortedIndex=d['sortedIndex'],
             i_grThresh_r=d['i_grThresh_r'], 
             i_grThresh_v=d['i_grThresh_v'],
             i_grThresh_both=d['i_grThresh_both'],
             corrcoeff_real=d['corrcoeff_real'],
             corrcoeff_virt=d['corrcoeff_virt'],
             corr_sorted_real_i=d['corr_sorted_real_i'],
             corr_sorted_virt_i=d['corr_sorted_virt_i'],
             corr_real_top_i=d['corr_real_top_i'], 
             corr_virt_top_i=d['corr_virt_top_i'], 
             corr_real_bot_i=d['corr_real_bot_i'], 
             corr_virt_bot_i=d['corr_virt_bot_i'],
             real_dendro=d['real_dendro'],
             virt_dendro=d['virt_dendro'],
             topnames_r_hist=d['topnames_r_hist'],
             topnames_v_hist=d['topnames_v_hist'],
             botnames_r_hist=d['botnames_r_hist'],
             botnames_v_hist=d['botnames_v_hist'])

    
    print("Saved results to " + outFileName + "\n\n")
if lg:
    print("Saved results to " + outFileName + "\n\n", file=logFile)



# Plotting
generatePlots(d,timelabel)

if lg:
    logFile.close()



