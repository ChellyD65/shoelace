E_BADARGS=5;
if [ ! -n "$1" ]
then
  echo "Usage: `basename $0` InputDir"
  exit $E_BADARGS
fi  
inputDir=$1
echo
echo "Input directory: $inputDir"
echo 

reference_file=/path/to/reference_file

find $inputDir -maxdepth 1 -name '*.sam' | while read filename; do
    name_base=`echo $filename | sed -r 's/\.[[:alnum:]]+\$//'`
    name1=$name_base"_rsem"
    name2=$name_base"_expression"
    if [ ! -f $name2".genes.results" ]; then
	echo $name_base ": Submitting to queue.";
	bsub -q short -n 6 -W 12:00 -e ~/.lsbatch_errors_rsem -o lsf_output.txt "convert-sam-for-rsem $filename $name1; rsem-calculate-expression --bam --paired-end $name1.bam $reference_file $name2"
    else
	echo $name2".genes.results found!";
    fi
    echo ""
done









