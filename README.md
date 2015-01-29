# shoelace #

A python package for RNA sequence data and expression level analysis and utilities for querying the <a href="http://www.ncbi.nlm.nih.gov/geo/">NCBI Gene Expression Omnibus (GEO)</a> database.  This package is written for Linux/*nix and uses <a href="https://github.com/ncbi/sra-tools/wiki/Downloads">sratools</a>, <a href="http://bowtie-bio.sourceforge.net/index.shtml">bowtie</a>, and <a href="http://deweylab.biostat.wisc.edu/rsem/">RSEM</a> to retrieve FASTQ data, manipulate it, align to reference genomes, and estimate expression levels.

### Requirements
-------------------
* Tested with Python 2.7.1
* <a href="http://www.numpy.org/">NumPy</a>, <a href="http://www.scipy.org/">SciPy</a>, <a href="http://matplotlib.org/">matplotlib</a>, <a href="http://scikit-learn.org/">scikit-learn</a>
* HPC cluster job manager (LSF) utilities tested on Platform LSF HPC 7 Update 6

### Installation
-------------------
Clone the repository.

    git clone https://github.com/ChellyD65/shoelace.git <installdir>

In your python script or code, add the path to the 'python/mmdgeneticstools' directory

    sys.path.append('<installdir>/python/mmdgeneticstools')
    from mmdgeneticstools.lib import *
    
#### Main tools
-------------------
Most of shoelace is in the form of a python package 'mmdgeneticstools' which can be imported into your own scripts.  Some example scripts are included in the shoelace/python/mmdgeneticstools/scripts/ directory:

* Analyze_RSEM_results.py -- Analysis of RSEM *.genes.results output files; sorts genes based on hg38 annotations from BioMart, does PCA, cross-correlation, etc.
* Shuffletown -- randomly distributes (paired end) FASTQ reads in multiple files into a number of new files

The shoelace/python/mmdgeneticstools/lib/ directory contains the modules that can be imported.  Some of these can be run as standalone scripts from the command line:

* Plotter.py -- Generates figures summarizing expression data, correlation, and cluster analysis.

##### Utility tools
-------------------
Perl and BASH shell scripts that may be helpful, especially in the HPC environment.

* Job management tools -- submits multiple bowtie and RSEM jobs to and LSF cluster in an organized way
* Split and Merge -- perl scripts that merge paired end read files from *_1.fastq and *_2.fastq into a single file, and split them back apart if needed

