"""
Created on Thurs, 9/04/2014

@author: mdistasio
"""

import os
import re
from Bio import Entrez 
from Bio import Geo
import xml.dom.minidom
import subprocess
import columnize
from shoelace.references.EntrezDBs import EntrezDBs


class FileLoader:

    def __init__(self, p):
        self.p = p

        
        Entrez.email="mdistasi@bidmc.harvard.edu"
        self.currentEntrezDB = None

    def selectDB(self):
        self.console_height, self.console_width = map(int, os.popen('stty size', 'r').read().split())
        print "\n\nSelect Entrez databases to query for SRA accession numbers. Enter the corresponding integer:"
        screenoutput = list()
        screenoutput.append(('[0] All Entrez Databases'))
        for key in enumerate(EntrezDBs):
            screenoutput.append(('[%s] %s' % (key[0]+1, key[1][0])))
        print columnize.columnize(screenoutput, displaywidth=self.console_width)
        print "(Default [32] sra):",
        s = raw_input()
        if s == '':
            self.currentEntrezDB = 'sra'
        else:
            try:
                number = map(int, s)
                if not (number in range(0,len(EntrezDBs)+1)):
                    print "\nERROR: Invalid input value. Please enter an  integer in the range [0-" + str(len(EntrezDBs)) + "].\n\n"
                    number = None
            except ValueError:
                print "\nERROR: Invalid input type. Please enter an integer in the range [0-" + str(len(EntrezDBs)) + "].\n\n"
            number = number-1
            if number == -1:
                self.currentEntrezDB = 'mmdAllEntrezDBs'
            else:
                self.currentEntrezDB = EntrezDBs[number][2]
        
    def parse_series_matrix(self, filename):
        print "Parsing series matrix file " + os.path.split(filename)[1]
        with open(filename,'r') as f:
            SeriesData = {}
            skip = False
            for x in f:
                S = x.split('\t',1)
                if re.compile('.*\!series_matrix_table_begin.*').match(S[0]):
                    skip = True
                if re.compile('.*\!series_matrix_table_end.*').match(S[0]):
                    skip = False
                if (len(S) > 1):
                    S[0] = S[0].lstrip('!')
                    if not skip:
                        while (S[0] in SeriesData.keys()):
                            S[0] = S[0]+'_'
                        SeriesData[S[0]] = S[1].replace("\"","").split('\t')

                        
        return SeriesData

    def choose_cell_records(self, SM, choice=None, exclude=None):
        # SM = SeriesData returned by parse_series_matrix

        # mmdhere: need to update
        #If the list already exists, just load it
        SRR_list_file = os.path.join(self.p.SeriesMetadataDir, 'GSE57872_AccessionNumbersForCellsOfInterest.txt')
        if os.path.exists(SRR_list_file):
            print "SRR Accession numbers for cells of interest found (" + os.path.split(SRR_list_file)[1] + ") -- loading..."
            with open(SRR_list_file) as f:
                content = f.readlines()
            aSRR = [a.split(':')[2].strip(' \n') for a in content]
            return aSRR


        hits = []
        for kc in choice.keys():
            records=SM[kc]
            for pattern in choice[kc]:
                #regex=re.compile(pattern)
                #inds = [i for i,x in enumerate(records) if regex.search(x)]
                inds = [i for i,x in enumerate(records) if (x==pattern)]
                hits.append(inds)
                #finalinds.extend(inds)
        if len(hits) > 0:
            finalinds = list(set.intersection(*map(set, hits)))
        else:
            records = SM[SM.keys()[0]]
            finalinds = [i for i,x in enumerate(records)]



        for ke in exclude.keys():
            records=SM[ke]
            for pattern in exclude[ke]:
                #regex=re.compile(pattern)
                #inds = [i for i,x in enumerate(records) if regex.search(x)]
                inds = [i for i,x in enumerate(records) if (x==pattern)]
                finalinds = [aa for aa in finalinds if aa not in inds]
        

        print "\n" + str(len(finalinds)) + " cells found that match criteria."

        SAccNumber = SM['Sample_geo_accession']
        aGEO = [SAccNumber[i] for i in finalinds]
        aSRR = map(lambda x: self.GetSRR(x), aGEO)

        return aSRR, finalinds

        










    def GetSRR(self, GEO_Accession_Number):
        if not self.currentEntrezDB:
            self.selectDB()
        if self.currentEntrezDB == 'mmdAllEntrezDBs':
            print "Looking up GEO accession number " + GEO_Accession_Number + " in ALL Entrez databases."
            handle = Entrez.egquery(retmax=10, term=GEO_Accession_Number)
        else:
            print "Looking up GEO accession number " + GEO_Accession_Number + " in Entrez database: " + self.currentEntrezDB
            handle = Entrez.esearch(db=self.currentEntrezDB, retmax=10, term=GEO_Accession_Number)
        record = Entrez.read(handle); handle.close()
        if int(record['Count']) < 1:
            print "No results in selected database."
            return -1

        handle = Entrez.efetch(db="sra", id=record['IdList'][0])
        GEOrecord = handle.read(); handle.close()
        xmlRecord = xml.dom.minidom.parseString(GEOrecord)
        itemlist = xmlRecord.getElementsByTagName('RUN') 

        SRR_Accession_Number =  itemlist[0].attributes['accession'].value

        print GEO_Accession_Number + " : " + record['IdList'][0] + " : " + SRR_Accession_Number
        return SRR_Accession_Number



    def fastq_dump(self, SRR_Accession_Number, numberOfReads=0):
        a = SRR_Accession_Number
        d = self.p.fastq_dir 
        if not os.path.isdir(d):
            os.makedirs(d)
        FASTQ_file_single = os.path.join(d,a+".fastq")
        FASTQ_file_1 = os.path.join(d,a+"_1.fastq")
        FASTQ_file_2 = os.path.join(d,a+"_2.fastq")
        if (os.path.exists(FASTQ_file_1) & os.path.exists(FASTQ_file_2)) or (os.path.exists(FASTQ_file_1+".gz") & os.path.exists(FASTQ_file_2+".gz")):
            print "Paired-end read fastq files found: " + FASTQ_file_1 + " , " + os.path.split(FASTQ_file_2)[1]
            return 0
        if (os.path.exists(FASTQ_file_single) or os.path.exists(FASTQ_file_single+".gz")):
            print "Single-end read fastq file found: " + FASTQ_file_single
            return 0
         
        else:
            print "Retrieving FASTQ file for accession number: " + a + "..."
            if numberOfReads == 0:
                try:
                    subprocess.check_call([self.p.fastq_dump, "-F", "--split-3", "-O", d, a])
                except subprocess.CalledProcessError:
                    print "fastq-dump returned an error: " + str(subprocess.CalledProcessError.returncode)
            else:
                try:
                    subprocess.check_call([self.p.fastq_dump, "-F", "--split-3", "-X", numberOfReads, "-O", d, a])
                except subprocess.CalledProcessError:
                    print "fastq-dump returned an error: " + str(subprocess.CalledProcessError.returncode)

        if (os.path.exists(FASTQ_file_1) & os.path.exists(FASTQ_file_2)) or (os.path.exists(FASTQ_file_1+".gz") & os.path.exists(FASTQ_file_2+".gz")):
            print "Paired-end read fastq files found: " + FASTQ_file_1 + " , " + os.path.split(FASTQ_file_2)[1]
            return 0
        if (os.path.exists(FASTQ_file_single) or os.path.exists(FASTQ_file_single+".gz")):
            print "Single-end read fastq file found: " + FASTQ_file_single
            return 0





    def choosefromdict(self, sm):
        """
        Query the user about which records to retrieve
        """
        self.console_height, self.console_width = map(int, os.popen('stty size', 'r').read().split())
        restart = True
        while restart:
            restart = False
            choice = dict(); exclude = dict();
            numbers = None
            while numbers is None:
                print("\nSelect data fields to choose from. Enter corresponding integer(s), separated by commas.\n")
                screenoutput = list()
                for key in enumerate(sorted(sm.keys())):
                    screenoutput.append(('[%s] %s' % (key[0]+1, key[1])))
                print columnize.columnize(screenoutput, displaywidth=self.console_width)
                print ":",
                s = raw_input()
                try:
                    numbers = map(int, s.split(','))
                    for n in numbers:
                        if not (n in range(1,len(sm)+1)):
                            print "\nERROR: Invalid input value. Please enter a comma separated list of integers in the range [1-" + str(len(sm)) + "].\n\n"
                            numbers = None
                except ValueError:
                    print "\nERROR: Invalid input type. Please enter a comma separated list of integers in the range [1-" + str(len(sm)) + "].\n\n"
            numbers = [n-1 for n in numbers]    
            for number in numbers:
                thiskey = sorted(sm.keys())[number]
                choice[thiskey] = list(); exclude[thiskey] = list();
                fieldvalues = sorted(set(sm[thiskey]))
                allowablevalues = range(-len(fieldvalues), len(fieldvalues)+1); allowablevalues.remove(0)
                numbers_fv = None
                while numbers_fv is None:
                    print("\nSelect values to retrieve from " + thiskey + ". Enter corresponding integer(s), separated by commas.  You can specify values to EXCLUDE by entering a negative valued integer. (Numbers in parentheses are the number of records that match that value).\n")
                    screenoutput = list()
                    for key in enumerate(fieldvalues):
                        screenoutput.append(('[%s] %s (%s)' % (key[0]+1, key[1], sm[thiskey].count(key[1]))))
                    print columnize.columnize(screenoutput, displaywidth=self.console_width)
                    print ":",
                    s = raw_input()
                    try:
                        numbers_fv = map(int, s.split(','))
                        for n in numbers_fv:
                            if not (n in allowablevalues):
                                print "\n ERROR: Invalid input value. Please enter a comma separated list of integers in the range ["+str(-len(fieldvalues))+"-" + str(len(fieldvalues)) + "], excluding 0.\n\n"
                                numbers_fv = None
                    except ValueError:
                        print "\n ERROR: Invalid input type. Please enter a comma separated list of integers in the range ["+str(-len(fieldvalues))+"-" + str(len(fieldvalues)) + "], excluding 0.\n\n"
                for nfv in numbers_fv:
                    if nfv > 0: 
                        choice[thiskey].append(fieldvalues[nfv-1])
                    if nfv < 0:
                        exclude[thiskey].append(fieldvalues[abs(nfv)-1])

            # get rid of keys with empty lists for values
            choice = dict((k, v) for k, v in choice.iteritems() if len(v)>0)
            exclude = dict((k, v) for k, v in exclude.iteritems() if len(v)>0)



            
            for k in set(choice.keys()) & set(exclude.keys()):
                if choice[k] == exclude[k]:
                    print "\nERROR: Same value present in both choice and exclude:"
                    print str(k) + " : " + str(choice[k])
                    print "Repeat selection?  [y]/n: ",
                    if raw_input() == ('y' or 'Y' or ''):
                        restart = True
                
        return choice, exclude



















