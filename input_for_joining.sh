# This is a shell script file that needs to be downloaded along with the python code
Files1=*genes.results
Files2=*isoforms.results

#For Genes
for f in $Files1
do
 temp=$(echo $f|perl -pe "s/\.quant\.genes\.results//;")
 echo $temp
 perl -pe "s/TPM/$temp"_TPM"/;" $f|perl -pe "s/expected_count/$temp"_expected_count"/;"|perl -pe "s/FPKM/$temp"_FPKM"/;"|cut -f1,5 > genes/$temp".genes.results_expected_count"
perl -pe "s/TPM/$temp"_TPM"/;" $f|perl -pe "s/expected_count/$temp"_expected_count"/;"|perl -pe "s/FPKM/$temp"_FPKM"/;"|cut -f1,6 > genes/$temp".genes.results_TPM"
perl -pe "s/TPM/$temp"_TPM"/;" $f|perl -pe "s/expected_count/$temp"_expected_count"/;"|perl -pe "s/FPKM/$temp"_FPKM"/;"|cut -f1,7 > genes/$temp".genes.results_FPKM"
done

# For isoforms
for f in $Files2
do
 temp=$(echo $f|perl -pe "s/\.quant\.isoforms\.results//;")
 echo $temp
 perl -pe "s/TPM/$temp"_TPM"/;" $f|perl -pe "s/expected_count/$temp"_expected_count"/;"|perl -pe "s/FPKM/$temp"_FPKM"/;"|cut -f1,5  > isoforms/$temp".isoforms.results_expected_count"
perl -pe "s/TPM/$temp"_TPM"/;" $f|perl -pe "s/expected_count/$temp"_expected_count"/;"|perl -pe "s/FPKM/$temp"_FPKM"/;"|cut -f1,6  > isoforms/$temp".isoforms.results_TPM"
perl -pe "s/TPM/$temp"_TPM"/;" $f|perl -pe "s/expected_count/$temp"_expected_count"/;"|perl -pe "s/FPKM/$temp"_FPKM"/;"|cut -f1,7  > isoforms/$temp".isoforms.results_FPKM"
done
