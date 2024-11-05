# Analysis of repeat content and duplications
Download the hard-masked genome from wormbase:
```
wget https://ftp.ebi.ac.uk/pub/databases/wormbase/parasite/releases/WBPS19/species/caenorhabditis_elegans/PRJNA13758/caenorhabditis_elegans.PRJNA13758.WBPS19.genomic_masked.fa.gz
gunzip caenorhabditis_elegans.PRJNA13758.WBPS19.genomic_masked.fa.gz
```
Generate a bed file of the masked regions using the script [generate_masked_ranges.py](https://github.com/Melkrewi/Structural_variants_detection/blob/main/generate_masked_ranges.py) downloaded from (https://www.danielecook.com/generate-a-bedfile-of-masked-ranges-a-fasta-file/):
```
python generate_masked_ranges.py caenorhabditis_elegans.PRJNA13758.WBPS19.genomic_masked.fa  > output_ranges.txt
```
Extract the duplications from the vcf files:
```
grep DUP /nfs/scistore18/vicosgrp/melkrewi/C_elegands_project/17.random_subread_mytool_random_state/alignment_315850_cuteSV.vcf > DUPs_mutant.vcf
grep DUP /nfs/scistore18/vicosgrp/melkrewi/C_elegands_project/17.random_subread_mytool_random_state/control/alignment_315848_cuteSV.vcf > DUPs_control.vcf
```
Get Chromosome lengths using seqkit:
```
seqkit fx2tab -nl caenorhabditis_elegans.PRJNA13758.WBPS19.genomic_masked.fa > caenorhabditis_elegans.PRJNA13758.WBPS19.genomic_masked.fa.len
```
Generate a bed file with 100,000 bp chromosomal windows in python:
```
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
chr_len=pd.read_csv("/nfs/scistore18/vicosgrp/melkrewi/C_elegands_project/12.repeat_masker/caenorhabditis_elegans.PRJNA13758.WBPS19.genomic_masked.fa.len",sep="\s+",header=None)
I_chr=pd.DataFrame([['I']*len(np.arange(0,chr_len[chr_len[0]=='I'][2].iloc[0],100000)),np.arange(0,chr_len[chr_len[0]=='I'][2].iloc[0],100000),np.arange(100000,chr_len[chr_len[0]=='I'][2].iloc[0]+100000,100000)]).T
II_chr=pd.DataFrame([['II']*len(np.arange(0,chr_len[chr_len[0]=='II'][2].iloc[0],100000)),np.arange(0,chr_len[chr_len[0]=='II'][2].iloc[0],100000),np.arange(100000,chr_len[chr_len[0]=='II'][2].iloc[0]+100000,100000)]).T
III_chr=pd.DataFrame([['III']*len(np.arange(0,chr_len[chr_len[0]=='III'][2].iloc[0],100000)),np.arange(0,chr_len[chr_len[0]=='III'][2].iloc[0],100000),np.arange(100000,chr_len[chr_len[0]=='III'][2].iloc[0]+100000,100000)]).T
V_chr=pd.DataFrame([['V']*len(np.arange(0,chr_len[chr_len[0]=='V'][2].iloc[0],100000)),np.arange(0,chr_len[chr_len[0]=='V'][2].iloc[0],100000),np.arange(100000,chr_len[chr_len[0]=='V'][2].iloc[0]+100000,100000)]).T
IV_chr=pd.DataFrame([['IV']*len(np.arange(0,chr_len[chr_len[0]=='IV'][2].iloc[0],100000)),np.arange(0,chr_len[chr_len[0]=='IV'][2].iloc[0],100000),np.arange(100000,chr_len[chr_len[0]=='IV'][2].iloc[0]+100000,100000)]).T
X_chr=pd.DataFrame([['X']*len(np.arange(0,chr_len[chr_len[0]=='X'][2].iloc[0],100000)),np.arange(0,chr_len[chr_len[0]=='X'][2].iloc[0],100000),np.arange(100000,chr_len[chr_len[0]=='X'][2].iloc[0]+100000,100000)]).T
pd.concat([I_chr,II_chr,III_chr,IV_chr,V_chr,X_chr],axis=0).to_csv("/nfs/scistore18/vicosgrp/melkrewi/C_elegands_project/20.mask_genome/chromosomal_bins.bed",sep="\t",header=True,index=False)
```
