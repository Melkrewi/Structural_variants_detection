# Analysis of repeat content and duplications
Download the hard-masked genome from wormbase:
```
wget https://ftp.ebi.ac.uk/pub/databases/wormbase/parasite/releases/WBPS19/species/caenorhabditis_elegans/PRJNA13758/caenorhabditis_elegans.PRJNA13758.WBPS19.genomic_masked.fa.gz
gunzip caenorhabditis_elegans.PRJNA13758.WBPS19.genomic_masked.fa.gz
```
Generate a bed file of the masked regions using the script [generate_masked_ranges.py](https://github.com/Melkrewi/Structural_variants_detection/blob/main/generate_masked_ranges.py) downloaded from (https://www.danielecook.com/generate-a-bedfile-of-masked-ranges-a-fasta-file/):
