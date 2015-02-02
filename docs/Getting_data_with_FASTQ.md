## Retrieving Data from NCBI Databases
---------------------------------------------
You can use any data in FASTQ format with shoelace.  The FASTQ_dumper.py utility is included to help you query and retrieve the files you need from the SRA database, based on GEO accession numbers.

Once you have the configuration file set up for your project, execute the FASTQ_dumper.py script located in <installdir>/python/shoelace/scripts/.  You can include the path to your config file as a command line argument:

    <installdir>/python/shoelace/scripts/FASTQ_dumper.py --configfile <ProjectDir>/Project.config

If you don't specify it on the command line, the program will prompt you to enter the filename of the configuration file:

    Please enter the configuration filename:  <ProjectDir>/Project.config 

It will then download the Series matrix *.tar.gz file, unzip and read it, and parse the data fields, presenting you with a menu of options with which you can choose which data records will be downloaded.

###### Choosing GEO data records
-------------------
* The first menu contains all the field <b>names</b> present in the Series Matrix file.  Enter the numbers corresponding to field names that you want to select from.  For each number entered here, a submenu will be created (and presented sequentially) with the unique data values found for the corresponding field name.

* The files downloaded will be the INTERSECTION of matching records.  Thus, a record must contain ALL values selected from the various fields in order to be included.

* You may specify values to EXCLUDE by entering a corresponding negative number.  Records matching the corresponding value will be ignored.

* If you do not enter any positive numbers in a submenu, all values for that submenu's field will be downloaded (unless they are excluded by entering a negative value).

* The final menu is for database selection. The program will query the SRA database (or another of your choosing) to find the SRA database accession numbers for the raw fastq data that correspond to GEO database numbers you have just selected.  Generally, the default (sra) database is yuor best bet.

* FASTQ data will be downloaded (using sratools) and placed in the directory specified by fastq_dir in your *.config file
