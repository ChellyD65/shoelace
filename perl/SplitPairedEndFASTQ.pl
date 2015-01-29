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

while(<$INFILE>) {
    print $OUTFILE1 $_;
    $_ = <$INFILE>;  
    print $OUTFILE1 $_; 
    $_ = <$INFILE>;  
    print $OUTFILE1 $_; 
    $_ = <$INFILE>;  
    print $OUTFILE1 $_; 

    $_ = <$INFILE>;  
    print $OUTFILE2 $_; 
    $_ = <$INFILE>;  
    print $OUTFILE2 $_;
    $_ = <$INFILE>;  
    print $OUTFILE2 $_;
    $_ = <$INFILE>;  
    print $OUTFILE2 $_;
}


