import pandas as pd
import argparse
import sys
import argparse
import os
parser=argparse.ArgumentParser(description="parse sniffles vcf file")
parser.add_argument("vcf_file")
parser.add_argument("output_file_name")
args=parser.parse_args()
file_name=args.vcf_file
output_file_name=args.output_file_name
with open(file_name) as oldfile, open('vcf_temp.txt', 'w') as newfile:
	for line in oldfile:
		line = "" if "#" in line or not line else line
		newfile.write(line)
vcf=pd.read_csv('vcf_temp.txt',sep="\t",header=None)
vcf['QUAL']=vcf[5]
vcf['CHROM']=vcf[0]
vcf['POS']=vcf[1]
vcf['SVTYPE']=vcf[2].str.split('.',expand=True)[1].fillna('NA')
vcf['AF']=vcf[7].str.split('AF=',expand=True)[1].str.split(';',expand=True)[0].fillna('NA')
vcf['SVLEN']=vcf[7].str.split('SVLEN=',expand=True)[1].str.split(';',expand=True)[0].fillna('NA')
vcf['Number of reference reads']=vcf[9].str.split(':',expand=True)[2].fillna('NA')
vcf['Number of variant reads']=vcf[9].str.split(':',expand=True)[3].fillna('NA')
vcf=vcf[['CHROM','QUAL','POS','SVTYPE','SVLEN','AF','Number of reference reads','Number of variant reads']]
vcf.to_csv(output_file_name,index=False,sep='\t')
os.remove("vcf_temp.txt")
