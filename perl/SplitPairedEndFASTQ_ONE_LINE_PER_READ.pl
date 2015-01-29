#!/usr/bin/perl

use File::Basename;

$filename = $ARGV[0];
($name,$dir,$ext) = fileparse($filename,'\..*');
$filenameOut1 = $name . "_1" . $ext;
$filenameOut2 = $name . "_2" . $ext;

print "Writing $filenameOut1 and $filenameOut2 \n";

open $INFILE, "< $filename";
open $OUTFILE1, "> $filenameOut1";
open $OUTFILE2, "> $filenameOut2";

$delim = "__newline__";
while(<$INFILE>) {
    @these8lines = split(/$delim/, $_);

    print $OUTFILE1 "$these8lines[0]\n";
    print $OUTFILE1 "$these8lines[1]\n"; 
    print $OUTFILE1 "$these8lines[2]\n"; 
    print $OUTFILE1 "$these8lines[3]\n"; 

    print $OUTFILE2 "$these8lines[4]\n"; 
    print $OUTFILE2 "$these8lines[5]\n";
    print $OUTFILE2 "$these8lines[6]\n";
    print $OUTFILE2 "$these8lines[7]";
}
