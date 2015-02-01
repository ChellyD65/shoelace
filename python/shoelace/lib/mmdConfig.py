"""
Created on Thurs, 9/04/2014
@author: mdistasio
"""
import os
import sys
import re




class Paths:
    def __init__(self, configFilename=None):
        if sys.platform == 'win32':
            self.ROOT = os.path.splitdrive(os.path.abspath('.'))[0]
        elif sys.platform == 'linux2':
            self.ROOT = os.sep
        basedir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

        if configFilename:
            self.configfile = configFilename
        else:
            self.configfile = os.path.abspath(str(raw_input('Please enter the configuration filename: ')))
        print("Loading configuration file: " + self.configfile)
        self.loadConfigFile(self.configfile)
        print "mmdConfig.Paths: Set up file paths for data and genomics tools. Data directory = " + self.SeriesMetadataDir

    def loadConfigFile(self,filename):
        self.configfile = filename
        validline = re.compile('^(?!#).+')
        with open(filename) as fp:
            for line in fp:
                if validline.match(line):
                    varname, varval = line.split("=")
                    exec('self.'+varname+' = '+varval)


    def displayConfig(self):
        print("\n\nCurrent configuration settings:")
        print("-----------------------------------")
        for key in  self.__dict__.keys():
            print(key + " : " + self.__dict__[key])
        print("\n")

                             
                            

        
