# Structural_variants_detection
## Preliminary steps
Downloading the reads and decompressing the files (command for only one of the files is shown):
```
wget -c --no-check-certificate --auth-no-challenge --user 'XXXXXXXX' --password 'XXXXXXXX' https://ngs.vbcf.ac.at/filemanager/byurl/134a311_20240902_1315_1C_PAW46587_3e9ba0bd.tar
tar -xvf 134a311_20240902_1315_1C_PAW46587_3e9ba0bd.tar

```
Install NGMLR and sniffles:
```
module load anaconda3/2024.03_deb12 ## This line and the next depend on what version of anaconda are installed on your cluster
source ~/activate_anaconda3_2024.03_deb12.txt
conda create -n sniffles_and_NGMLR
conda activate sniffles_and_NGMLR
conda install sniffles=2.4
conda install bioconda::ngmlr
conda deactivate
```
Install samtools/1.9 (Newer samtools versions did not work directly with the output of NGMLR):
```
module load anaconda3/2024.03_deb12 ## This line and the next depend on what version of anaconda are installed on your cluster
source ~/activate_anaconda3_2024.03_deb12.txt
conda create -n samtools_1.9
conda activate samtools_1.9
conda install samtools=1.9
conda deactivate
```
Install cuteSV:
```
module load anaconda3/2024.03_deb12 ## This line and the next depend on what version of anaconda are installed on your cluster
source ~/activate_anaconda3_2024.03_deb12.txt
conda create -n cuteSV
conda install -c bioconda cutesv
conda deactivate
```
Download the c. elegans genome:
```
wget https://ftp.ensembl.org/pub/release-112/fasta/caenorhabditis_elegans/dna/Caenorhabditis_elegans.WBcel235.dna.toplevel.fa.gz
```
## Read alignment

Align the reads using NGMLR:
```
module load anaconda3/2024.03_deb12 ## This line and the next depend on what version of anaconda are installed on your cluster
source ~/activate_anaconda3_2024.03_deb12.txt
conda activate sniffles_and_NGMLR

ngmlr -x ont -t 100 -r Caenorhabditis_elegans.WBcel235.dna.toplevel.fa -q PAW46587_1_202409050.fastq.gz -o alignment_315850.sam
ngmlr -t 100 -x ont -r Caenorhabditis_elegans.WBcel235.dna.toplevel.fa -q PAW50853_1_202409050.fastq.gz -o alignment_315848.sam
```
Convert the alignment files to bam, then sort and index:
```
module load anaconda3/2024.03_deb12 ## This line and the next depend on what version of anaconda are installed on your cluster
source ~/activate_anaconda3_2024.03_deb12.txt
conda activate samtools_1.9

samtools view -@20 -bS alignment_315848.sam > alignment_315848.bam
samtools sort -@20 -o alignment_315848.sorted.bam alignment_315848.bam
samtools view -@20 -bS alignment_315850.sam > alignment_315850.bam
samtools sort -@20 -o alignment_315850.sorted.bam alignment_315850.bam
samtools index alignment_315848.sorted.bam
samtools index alignment_315850.sorted.bam
conda deactivate
```
## Estimating the coverage per sample
```
module load samtools

samtools coverage --histogram alignment_315850.sorted.bam > alignment_315850.coverage
samtools coverage --histogram alignment_315848.sorted.bam > alignment_315848.coverage

```
### Subsampling the alignments
We randomly sampled the alignments from the sample with the higher coverage to match the coverage of the other sample.
```
samtools view -bs 0.816 alignment_315850.sorted.bam > alignment_315850.sorted.subsampled.bam
samtools sort alignment_315850.sorted.subsampled.bam > temp
mv temp alignment_315850.sorted.subsampled.bam
samtools index alignment_315850.sorted.subsampled.bam
```

### Calling SVs using sniffles
Generating tandem repeats bed file (script can be found [here](https://github.com/PacificBiosciences/pbsv/tree/master/annotations)):
```
findTandemRepeats --merge Caenorhabditis_elegans.WBcel235.dna.toplevel.fa celegans.trf.bed
```
Call structural variants using sniffles (for more than one sample):
```
module load anaconda3/2024.03_deb12 ## This line and the next depend on what version of anaconda are installed on your cluster
source ~/activate_anaconda3_2024.03_deb12.txt
conda activate sniffles_and_NGMLR

sniffles --input alignment_315848.sorted.bam --vcf alignment_315848.vcf --qc-output-all --mosaic --tandem-repeats celegans.trf.bed --threads 60 --output-rnames
sniffles --input alignment_315850.sorted.subsampled.bam --vcf alignment_315850_subsampled.vcf --qc-output-all --mosaic --tandem-repeats celegans.trf.bed --threads 60 --output-rnames
conda deactivate
```
### Calling SVs using cuteSV
```
module load anaconda3/2024.03_deb12
source ~/2024.03_deb12/activate_anaconda3_2024.03_deb12.txt
conda activate cuteSV
cuteSV alignment_315848.sorted.bam /nfs/scistore18/vicosgrp/melkrewi/C_elegands_project/2.analysis/Caenorhabditis_elegans.WBcel235.dna.toplevel.fa alignment_315848_cuteSV.vcf . --min_support 1 --max_cluster_bias_INS	100 --diff_ratio_merging_INS 0.3 --max_cluster_bias_DEL 100 --diff_ratio_merging_DEL 0.3 --report_readid 
cuteSV alignment_315850.sorted.subsampled.bam /nfs/scistore18/vicosgrp/melkrewi/C_elegands_project/2.analysis/Caenorhabditis_elegans.WBcel235.dna.toplevel.fa alignment_315850_subsampled_cuteSV.vcf . --min_support 1 --max_cluster_bias_INS	100 --diff_ratio_merging_INS 0.3 --max_cluster_bias_DEL 100 --diff_ratio_merging_DEL 0.3 --report_readid
conda deactivate
```



