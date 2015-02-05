## Redistribution of FASTQ sequence reads into 'virtual' cells
--------------------------------------------------------------

Once your files are downloaded and the configuration file specifies their locations, simply run

    <shoelace_install_dir>/python/shoelace/scripts/ShuffleTown.py --configfile <Project.config>
  
The reads in your FASTQ files will be randomly distributed among a set of new files.  The number of new files will be the same as the number of files in the original dataset (i.e. the number of files in the fastq_dir).  The distribution of number of reads per file will match the distribution of number of reads per file in the original.

The lib/Shuffle.py script will automatically detect whether the files are single-end or paired-end by looking for *_1.fastq and *_2.fastq files (in which case the data is assumed to be paired-end), and write output files to match.
