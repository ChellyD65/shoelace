# README #

Some simple utilities for manipulating FASTQ files

### Main tools ###
* Shuffletown -- randomly distributes (paired end) FASTQ reads in multiple files into a number of new files
* Split and Merge -- perl scripts that merge paired end read files from *_1.fastq and *_2.fastq into a single file, and split them back apart if needed
* Job management tools -- submits multiple bowtie and RSEM jobs to and LSF cluster in an organized way
* Analyze_RSEM_results.py -- Analysis of RSEM *.genes.results output files; sorts genes based on hg38 annotations from BioMart, does PCA, cross-correlation, etc.