#Tips:
#download this program and store in a folder. 
#For example in this example I downloaded and stored in the folder scripts 
#Make sure you create the star index and rsem index files
#input the index and genome fasta location files

#Program starts
import glob
from multiprocessing import Pool
from subprocess import call
import os
import pandas as pd


def star_call(ff):
 print("star_running")
 temp=ff.replace("_R1.fq","") #For pair-end fastq files  we read in the R1 file
 temp=temp.replace("../","")
 echo_call_1=(f"echo aligning {temp}.fastq")
 call(echo_call_1,shell=True)
 #prepare your star command with all needed parameters
 #insert the directory where you stored your star indexed files
 star_run=(f"STAR --genomeDir "directory where your star indices are stored" --readFilesIn ../{temp}_R1.fq  ../{temp}_R2.fq --outSAMtype BAM SortedByCoordinate --outSAMunmapped Within --twopassMode Basic --outFilterMultimapNmax 20 --quantMode TranscriptomeSAM --outFilterMismatchNoverReadLmax 0.06  --runThreadN 20 --outFileNamePrefix ../star_output/{temp}_star_")      
 #execute the star alignment command
 call(star_run, shell=True)
 echo_call=(f"echo aligning {temp}.fastq completed")
 call(echo_call,shell=True) 

def rsem_call(ff):
 print("rsem_running")
 #star aligned files after being sorted produces file with the suffix "_star_Aligned.toTranscriptome.out.bam"
 temp=ff.replace("_star_Aligned.toTranscriptome.out.bam","")
 echo_call_1=(f"echo rsem quantification {temp}_star_aligned_Aligned.toTranscriptome.out.bam")
 call(echo_call_1,shell=True)
#prepare your rsem command in the line below 
#insert the rsem index file prefix
 rsem_run=(f"rsem-calculate-expression --alignments --paired-end --bam --no-bam-output -p 20 {temp}_star_Aligned.toTranscriptome.out.bam "Rsem_index files"  rsem_output/{temp}.quant")      
 call(rsem_run, shell=True)
 echo_call=(f"echo rsem quantification {temp}_star_aligned_Aligned.toTranscriptome.out.bam completed")
 call(echo_call,shell=True)

#this function merges all the TPM, EXPECTED COUNT, FPKM files together with sample names as column names
def merging_files(ff,output,typeof_column):
 print("merging files")
 counter=0
 while counter<len(ff):
#merging first two files then creating temp df
  if counter==0:
   left=pd.read_csv(ff[counter],sep="\t")
   right=pd.read_csv(ff[counter+1],sep="\t")
   fin=left.merge(right, on=typeof_column, how='left')
   counter=counter+2
#merging one by one
  else:
   right=pd.read_csv(files[counter],sep="\t")
   fin=fin.merge(right, on=typeof_column, how='left')
   #print(counter)
   counter=counter+1
#writing the output file
 fin.to_csv(output,sep="\t",index=False)




if __name__ == '__main__':
    files_ls=glob.glob("../*_R1.fq") 
#creating a star alignment output director
    makedir=(f"mkdir ../star_output")
    call(makedir, shell=True)
#set number of processors you want to use 
    p = Pool(processes=3)
#calling the function star call
    data = p.map(star_call, [i for i in files_ls])
    p.close()
    os.chdir("../star_output")
    print("changing dir")
    makedir=(f"mkdir rsem_output")
    call(makedir, shell=True)
    files_ls0=glob.glob("*.toTranscriptome.out.bam")
    p1 = Pool(processes=2)
#calling rsem function
    data1 = p1.map(rsem_call, [i for i in files_ls0])
    p1.close()
#entering the rsem quant folder
    os.chdir("rsem_output")
    makedir=(f"mkdir genes")
    call(makedir, shell=True)
    makedir=(f"mkdir isoforms")
    call(makedir, shell=True)
    print(f"present working directory is: {os.getcwd()}")
    #the program input_for_joining utilizes a script to prepare input for next steps
    run_shell=(f"sh ../../scripts/input_for_joining.sh")
    call(run_shell, shell=True)
    os.chdir("genes")
    print("changing dir to genes")
    files=glob.glob("*genes.results_expected_count")
#calling python merging files
    merging_files(files,"all_merged_expected_count.tsv","gene_id")
    files=glob.glob("*genes.results_TPM")
#calling python merging files
    merging_files(files,"all_merged_TPM.tsv","gene_id")
    files=glob.glob("*genes.results_FPKM")
#calling python merging files
    merging_files(files,"all_merged_FPKM.tsv","gene_id")
    os.chdir("../isoforms")
    print("changing dir to isoforms")
    files=glob.glob("*isoforms.results_expected_count")
#calling python merging files
    merging_files(files,"all_isoforms_merged_expected_count.tsv","transcript_id")
    files=glob.glob("*isoforms.results_TPM")
#calling python merging files
    merging_files(files,"all_isoforms_merged_TPM.tsv","transcript_id")
    files=glob.glob("*isoforms.results_FPKM")
#calling python merging files
    merging_files(files,"all_isoforms_merged_FPKM.tsv","transcript_id")
