import argparse
from mutract.utils import Mutract
from mutract.__init__ import __version__
   
def main():
    readme = f'Mutract'
    parser = argparse.ArgumentParser(readme)
    parser.add_argument('--bam', help='bam', required=True)
    parser.add_argument('--barcodes', help='barcodes', required=True)
    parser.add_argument('--fasta', help='fasta', required=True)
    parser.add_argument('--sample', help='sample', required=True)
    parser.add_argument('--outdir', help='outdir', default='./')
    parser.add_argument('--thread', help='thread', default=1)
    parser.add_argument('--vcf', help='vcf', default=None)
    parser.add_argument('--gene_file', help='gene file', default=None)
    parser.add_argument('-v','--version',action='version', version=__version__)
    args = parser.parse_args()

    obj = Mutract(
        args.outdir, args.sample, args.bam, args.fasta, 
        args.barcodes, args.vcf, int(args.thread),
        args.gene_file,
    )
    obj.run()

if __name__ == '__main__':
    main()

