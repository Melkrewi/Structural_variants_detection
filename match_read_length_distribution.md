# Match the read length distribution of the two samples 
Get the read lengths of both samples:
```
module load seqkit
seqkit fx2tab -nl PAW50853_1_202409050.fastq.gz > PAW50853_1_202409050.len
seqkit fx2tab -nl PAW46587_1_202409050.fastq.gz > PAW46587_1_202409050.len
```
Use the following python script to get bin the read lengths of the control sample, count the number of reads in each bin in the two samples, and sample the minimum number of reads from each bin:
```
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy
import seaborn as sns
import matplotlib.patches as mpatches
import os
#os.chdir("C:/Users/melkrewi/Desktop/shrimp/Nauplii_project/TRINITY/")
#load the read lengths for the two libraries
library_1_read_lengths=pd.read_csv("/nfs/scistore18/vicosgrp/melkrewi/C_elegands_project/16.random_subread_mytool/PAW50853_1_202409050.len",sep="\t",header=None)#
library_2_read_lengths=pd.read_csv("/nfs/scistore18/vicosgrp/melkrewi/C_elegands_project/16.random_subread_mytool/PAW46587_1_202409050.len",sep="\t",header=None)#
#get the read length bins from the first library
x,y,_=plt.hist(np.log2(library_1_read_lengths[1]),bins=100)
plt.close()
#count the number of reads in each bin for both libraries
library_1_counts=[]
library_2_counts=[]
for i in np.arange(0,100,1):
    library_1_counts.append(len(library_1_read_lengths[(np.log2(library_1_read_lengths[1])>=y[i])&(np.log2(library_1_read_lengths[1])<y[i+1])]))
    library_2_counts.append(len(library_2_read_lengths[(np.log2(library_2_read_lengths[1])>=y[i])&(np.log2(library_2_read_lengths[1])<y[i+1])]))
#merge the counts into one dataframe
bin_counts=pd.concat([pd.DataFrame(library_1_counts,columns=['train']),pd.DataFrame(library_2_counts,columns=['test'])],axis=1)
#identify which sample has less reads in each bin
bin_counts['min']=bin_counts[['train','test']].min(axis=1)
#randomly sample reads within each bin using the numbers identifies in the last step 
library_1_subsample=pd.DataFrame(columns=[0,1])
library_2_subsample=pd.DataFrame(columns=[0,1])
for i in np.arange(0,100,1):
    library_1_subsample=pd.concat([library_1_subsample,library_1_read_lengths[(np.log2(library_1_read_lengths[1])>=y[i])&(np.log2(library_1_read_lengths[1])<y[i+1])].sample(n=bin_counts['min'].iloc[i], replace=False,random_state=0)],axis=0)
    library_2_subsample=pd.concat([library_2_subsample,library_2_read_lengths[(np.log2(library_2_read_lengths[1])>=y[i])&(np.log2(library_2_read_lengths[1])<y[i+1])].sample(n=bin_counts['min'].iloc[i], replace=False,random_state=0)],axis=0)
library_1_subsample[0].to_csv("/nfs/scistore18/vicosgrp/melkrewi/C_elegands_project/17.random_subread_mytool_random_state/control_sample_adjusted_distribution_reads.txt",sep="\t",index=False,header=None)
library_2_subsample[0].to_csv("/nfs/scistore18/vicosgrp/melkrewi/C_elegands_project/17.random_subread_mytool_random_state/mutant_sample_adjusted_distribution_reads.txt",sep="\t",index=False,header=None)
```
subsample the fastq file with seqtk using the identified readnames:
```
module load seqtk
seqtk subseq PAW46587_1_202409050.fastq.gz mutant_sample_adjusted_distribution_reads.txt > 315850_adjusted.fastq
seqtk subseq PAW50853_1_202409050.fastq.gz control_sample_adjusted_distribution_reads.txt > 315848_adjusted.fastq
```
