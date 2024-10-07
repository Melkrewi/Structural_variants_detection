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
## Read alignment

Align the reads using NGMLR (you could also use minimap2):
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
## Subsampling the alignments




Call structural variants using sniffles (for more than one sample):
```
module load anaconda3/2024.03_deb12 ## This line and the next depend on what version of anaconda are installed on your cluster
source ~/activate_anaconda3_2024.03_deb12.txt
conda activate sniffles_and_NGMLR

module load samtools

sniffles --input alignment1.sorted.bam --threads 60 --snf alignment1.snf #--output-rnames 
sniffles --input alignment2.sorted.bam --threads 60 --snf alignment2.snf #--output-rnames 
#sniffles --input alignment1.snf alignment2.snf --vcf multisample.vcf --threads 60 
conda deactivate

```
