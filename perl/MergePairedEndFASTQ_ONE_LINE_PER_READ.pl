#!/usr/bin/perl

$filenameA = $ARGV[0];
$filenameB = $ARGV[1];
$filenameOut = $ARGV[2];

open $FILEA, "< $filenameA";
open $FILEB, "< $filenameB";

open $OUTFILE, "> $filenameOut";

$delim = "__newline__";
while(<$FILEA>) {
    chomp($_);
    print $OUTFILE $_ . $delim;
    $_ = <$FILEA>; 
    chomp($_);
    print $OUTFILE $_ . $delim;
    $_ = <$FILEA>; 
    chomp($_);
    print $OUTFILE $_ . $delim;
    $_ = <$FILEA>; 
    chomp($_);
    print $OUTFILE $_ . $delim;

    $_ = <$FILEB>;
    chomp($_);
    print $OUTFILE $_ . $delim;
    $_ = <$FILEB>;
    chomp($_);
    print $OUTFILE $_ . $delim;
    $_ = <$FILEB>;
    chomp($_);
    print $OUTFILE $_ . $delim;
    $_ = <$FILEB>;
    print $OUTFILE $_;
}

