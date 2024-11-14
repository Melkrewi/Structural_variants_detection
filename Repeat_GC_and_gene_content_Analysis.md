# Analysis of repeat content and duplications
Download the genome annotation from wormbase:
```
wget https://ftp.ebi.ac.uk/pub/databases/wormbase/parasite/releases/WBPS19/species/caenorhabditis_elegans/PRJNA13758/caenorhabditis_elegans.PRJNA13758.WBPS19.annotations.gff3.gz
gunzip caenorhabditis_elegans.PRJNA13758.WBPS19.annotations.gff3.gz
```
Extract the duplications from the vcf files:
```
grep DUP /nfs/scistore18/vicosgrp/melkrewi/C_elegands_project/17.random_subread_mytool_random_state/alignment_315850_cuteSV.vcf > DUPs_mutant.vcf
grep DUP /nfs/scistore18/vicosgrp/melkrewi/C_elegands_project/17.random_subread_mytool_random_state/control/alignment_315848_cuteSV.vcf > DUPs_control.vcf
```
Get Chromosome lengths using seqkit:
```
module load seqkit
seqkit fx2tab -nl Caenorhabditis_elegans.WBcel235.dna.toplevel.fa > Caenorhabditis_elegans.WBcel235.dna.toplevel.fa.len
```
Generate a bed file with 100,000 bp chromosomal windows in python:
```
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
chr_len=pd.read_csv("/nfs/scistore18/vicosgrp/melkrewi/C_elegands_project/21.repeat_analysis/GC_content/Caenorhabditis_elegans.WBcel235.dna.toplevel.fa.len",sep="\s+",header=None)[[0,4]]
I_chr=pd.DataFrame([['I']*len(np.arange(0,chr_len[chr_len[0]=='I'][4].iloc[0],100000)),np.arange(0,chr_len[chr_len[0]=='I'][4].iloc[0],100000),np.arange(100000,chr_len[chr_len[0]=='I'][4].iloc[0]+100000,100000)]).T
II_chr=pd.DataFrame([['II']*len(np.arange(0,chr_len[chr_len[0]=='II'][4].iloc[0],100000)),np.arange(0,chr_len[chr_len[0]=='II'][4].iloc[0],100000),np.arange(100000,chr_len[chr_len[0]=='II'][4].iloc[0]+100000,100000)]).T
III_chr=pd.DataFrame([['III']*len(np.arange(0,chr_len[chr_len[0]=='III'][4].iloc[0],100000)),np.arange(0,chr_len[chr_len[0]=='III'][4].iloc[0],100000),np.arange(100000,chr_len[chr_len[0]=='III'][4].iloc[0]+100000,100000)]).T
V_chr=pd.DataFrame([['V']*len(np.arange(0,chr_len[chr_len[0]=='V'][4].iloc[0],100000)),np.arange(0,chr_len[chr_len[0]=='V'][4].iloc[0],100000),np.arange(100000,chr_len[chr_len[0]=='V'][4].iloc[0]+100000,100000)]).T
IV_chr=pd.DataFrame([['IV']*len(np.arange(0,chr_len[chr_len[0]=='IV'][4].iloc[0],100000)),np.arange(0,chr_len[chr_len[0]=='IV'][4].iloc[0],100000),np.arange(100000,chr_len[chr_len[0]=='IV'][4].iloc[0]+100000,100000)]).T
X_chr=pd.DataFrame([['X']*len(np.arange(0,chr_len[chr_len[0]=='X'][4].iloc[0],100000)),np.arange(0,chr_len[chr_len[0]=='X'][4].iloc[0],100000),np.arange(100000,chr_len[chr_len[0]=='X'][4].iloc[0]+100000,100000)]).T
chromosomal_bins=pd.concat([I_chr,II_chr,III_chr,IV_chr,V_chr,X_chr],axis=0)
chromosomal_bins.to_csv("/nfs/scistore18/vicosgrp/melkrewi/C_elegands_project/20.mask_genome/chromosomal_bins.bed",sep="\t",header=True,index=False)
chromosomal_bins['index']=(chromosomal_bins[0]).astype('str')+'-'+(chromosomal_bins[1]).astype('str')+'-'+(chromosomal_bins[2]).astype('str')
```
Get non-overlapping repetitive windows and find the intersection with the chromosomal windows: 
```
module load bedops
module load bedtools
grep repeat caenorhabditis_elegans.PRJNA13758.WBPS19.annotations.gff3 | cut -f1,2,3,4,5 > repeats.txt
cat repeats.txt | cut -f1,4,5 > repeats.bed
grep '\<II\>' repeats.bed > II.bed
grep '\<I\>' repeats.bed > I.bed
grep '\<III\>' repeats.bed > III.bed
grep '\<IV\>' repeats.bed > IV.bed
grep '\<V\>' repeats.bed > V.bed
grep '\<X\>' repeats.bed > X.bed
bedmap --count --echo --bp-ovr 1 --delim '\t' I.bed | awk '($1>1)' | cut -f2- | bedops --merge - > I_clean.bed
bedmap --count --echo --bp-ovr 1 --delim '\t' II.bed | awk '($1>1)' | cut -f2- | bedops --merge - > II_clean.bed
bedmap --count --echo --bp-ovr 1 --delim '\t' III.bed | awk '($1>1)' | cut -f2- | bedops --merge - > III_clean.bed
bedmap --count --echo --bp-ovr 1 --delim '\t' V.bed | awk '($1>1)' | cut -f2- | bedops --merge - > V_clean.bed
bedmap --count --echo --bp-ovr 1 --delim '\t' IV.bed | awk '($1>1)' | cut -f2- | bedops --merge - > IV_clean.bed
bedmap --count --echo --bp-ovr 1 --delim '\t' X.bed | awk '($1>1)' | cut -f2- | bedops --merge - > X_clean.bed
cat *_clean.bed > all_clean.bed
bedtools intersect -a chromosomal_bins.bed -b all_clean.bed -wo > repeats_in_chromosomal_bins
```
Get non-overlapping genic windows and find the intersection with the chromosomal windows: 
```
module load bedops
module load bedtools
grep 'biotype=protein_coding' caenorhabditis_elegans.PRJNA13758.WBPS19.annotations.gff3 | cut -f1,2,3,4,5 > genes.txt
cat genes.txt | cut -f1,4,5 > genes.bed
grep '\<II\>' genes.bed > II_genes.bed
grep '\<I\>' genes.bed > I_genes.bed
grep '\<III\>' genes.bed > III_genes.bed
grep '\<IV\>' genes.bed > IV_genes.bed
grep '\<V\>' genes.bed > V_genes.bed
grep '\<X\>' genes.bed > X_genes.bed
bedmap --count --echo --bp-ovr 1 --delim '\t' I_genes.bed | awk '($1>1)' | cut -f2- | bedops --merge - > I_genes_clean.bed
bedmap --count --echo --bp-ovr 1 --delim '\t' II_genes.bed | awk '($1>1)' | cut -f2- | bedops --merge - > II_genes_clean.bed
bedmap --count --echo --bp-ovr 1 --delim '\t' III_genes.bed | awk '($1>1)' | cut -f2- | bedops --merge - > III_genes_clean.bed
bedmap --count --echo --bp-ovr 1 --delim '\t' V_genes.bed | awk '($1>1)' | cut -f2- | bedops --merge - > V_genes_clean.bed
bedmap --count --echo --bp-ovr 1 --delim '\t' IV_genes.bed | awk '($1>1)' | cut -f2- | bedops --merge - > IV_genes_clean.bed
bedmap --count --echo --bp-ovr 1 --delim '\t' X_genes.bed | awk '($1>1)' | cut -f2- | bedops --merge - > X_genes_clean.bed
cat *_genes_clean.bed > all_genes_clean.bed
bedtools intersect -a chromosomal_bins.bed -b all_genes_clean.bed -wo > genes_in_chromosomal_bins
```
Get the intersection between the duplications and the chromosomal bins:
```
bedtools intersect -a chromosomal_bins.bed -b /nfs/scistore18/vicosgrp/melkrewi/C_elegands_project/20.mask_genome/DUPs_control.vcf -wo > DUPs_control_in_chromosomal_bins.txt
bedtools intersect -a chromosomal_bins.bed -b /nfs/scistore18/vicosgrp/melkrewi/C_elegands_project/20.mask_genome/DUPs.vcf -wo > DUPs_mutant_in_chromosomal_bins.txt
```
Use the [jupyter notebook] for the analysis.
