# Mutract
Mutract is a tool for extracting single cell variants from bam file. If vcf file is not provided, it will perform variant calling at single cell level.

## Requirements
- python > 3.6
- GATK
- samtools

## Installation
`pip install mutract`

GATK and samtools can be installed via conda.

## Usage
```
mutract \
--bam bam_file \
--barcodes cell_barcodes_file \
--fasta reference_fasta_file \
--vcf vcf_file \
--sample sample_name \
--outdir output_directory \
--thread 8 \
--gene_file gene_file \
```

- Required Arguments

`bam` Input CeleScope BAM file. If gene_file is specified, the BAM must have the 'GN' tag.

`barcodes` Cell barcodes file, one barcode per line.

`fasta` Reference genome fasta, must be indexed.

`sample` Sample name.

- Optional Arguments

`vcf` VCF file. If vcf file is not provided, mutract will perform variant calling at single cell level and use these variants as input vcf.

`outdir` output directory, default='./'.

`thread` The number of threads to use,  default=1.

`gene_file` Gene list file, one gene symbol per line. Only variants of these genes are reported.

## Output

`{sample}_VID.tsv` A unique numeric ID is assigned for each variant.

`{sample}_CID.tsv` A unique numeric ID is assigned for each cell.

`{sample}_variant_count.tsv`  Reference and variant supporting reads/UMIs count.

`{sample}_support.mtx` Support matrix, only high quality bases are considered.   
0 : no reads/UMIs covered the position. 
1 : all reads/UMIs at the position support the ref allele.  
2 : all reads/UMIs at the position support the alt allele.  
3 : one or more reads/UMIs support both the alt and the ref allele.  

## Usage
```
mutract \
--bam bam_file \
--barcodes cell_barcodes_file \
--fasta reference_fasta_file \
--vcf vcf_file \
--sample sample_name \
--outdir output_directory \
```
