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

reference_file=/path/to/rsem_reference

find $inputDir -maxdepth 1 -name '*_1.fastq' | while read filename; do
    name_base=`echo $filename | sed -r 's/_1\.[[:alnum:]]+\$//'`
    echo $name_base
    name1=$name_base"_1.fastq"
    name2=$name_base"_2.fastq"
    name_out=$name_base".sam"
    if [ ! -f $name_out ]; then
	echo $name_base ": Submitting to queue.";
	bsub -q short -n 4 -W 12:00 -R "rusage[mem=12000]" -e ~/.lsbatch_errors -o lsf_output.txt "$reference_file -n 0 -e 99999999 -l 25 -I 1 -X 2000 -a -m 15 -1 $name1 -2 $name2 -S $name_out;"
    else
	echo $name_out " found!";
    fi
done






