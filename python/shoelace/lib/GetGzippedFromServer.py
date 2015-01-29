"""
Created on Thurs, 9/04/2014

@author: mdistasio
"""
import os
import urllib
import gzip

class GetGZippedFromServer:

    def getunzipped(self, theurl, dest):
        destdir = os.path.dirname(dest)
        name = os.path.join(destdir, 'temp.gz')
        print "Retrieving %r to %r" % (theurl, dest)
        try:
            name, hdrs = urllib.urlretrieve(theurl, name)
        except IOError, e:
            print "Can't retrieve %r to %r: %s" % (theurl, dest, e)
            return
        try:
            z = gzip.GzipFile(name)
        except gzip.error, e:
            print "Bad zipfile (from %r): %s" % (theurl, e)
            return
        if not os.path.isdir(destdir):
            os.makedirs(destdir)
        data = z.read()
        f = open(dest, 'w')
        f.write(data)
        f.close()
        z.close()
        os.unlink(name)
        print "Done!"


