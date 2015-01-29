#!/usr/bin/perl -w


use DB_File;
use Fcntl;
 
my $filename = $ARGV[0];
my $indexfilename = $ARGV[1];
my $filenameOut = $ARGV[2];


open(my $fh_index, $indexfilename)
  or die "Could not open file '$indexfilename' $!";
open $OUTFILE, "> $filenameOut";

$cnt=1;
while (my $rowi = <$fh_index>) {
  chomp $rowi;
  $line_number = $rowi;
  $tie = tie(@lines, "DB_File", $filename, O_RDWR, 0666, $DB_RECNO)
      or die "Cannot open file $filename: $!\n";
  unless ($line_number < $tie->length) {
      print  "Didn't find line $line_number in $filename\n"
  }
  print $OUTFILE "$lines[$line_number-1]\n";     
#  print "$cnt\n";
#  untie
  $cnt=$cnt+1;
}
print "ReorderLines.pl: Reordered $cnt lines\n\n";


