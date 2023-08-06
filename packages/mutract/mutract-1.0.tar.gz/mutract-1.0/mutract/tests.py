import unittest
import os
from utils import *

class Tests(unittest.TestCase):

    def setUp(self):
        os.chdir('/SGRNJ01/RD_dir/pipeline_test/zhouyiqi/mutract/20210108/')
        self.outdir = 'sample1/05.snp'
        self.sample = 'sample1'
        self.bam = 'sample1/04.featureCounts/sample1_Aligned.sortedByCoord.out.bam.featureCounts.bam'
        self.barcodes_file = '/SGRNJ02/RandD4/RD20051303_Panel/20201218_2/\
S32_SUR0528_drug_S203_ZL/05.count/S32_SUR0528_drug_S203_ZL_matrix_10X/barcodes.tsv'
        self.index_file = 'sample1/05.snp/sample1_cell_index.tsv'
        self.thread = 2
        self.fasta = '/SGRNJ/Public/Database/genome/homo_sapiens/ensembl_92/Homo_sapiens.GRCh38.fa'
        self.splitN_bam = 'sample1/05.snp/sample1_splitN.bam'
        self.gene_file = '/SGRNJ01/RD_dir/pipeline_test/zhouyiqi/mutract/20210108/gene_list.txt'
        self.obj = Mutract(
            self.outdir, self.sample, self.bam, self.fasta, 
            self.barcodes_file, thread=2, gene_file=self.gene_file
        )
    '''

    def setUp(self):
        os.chdir('/SGRNJ01/RD_dir/pipeline_test/zhouyiqi/mutract/20210112')
        self.sample = 'S32_SUR0528_drug_S203_TS'
        self.outdir = f'{self.sample}/05.snp'
        self.bam = f'{self.sample}/04.featureCounts/{self.sample}_Aligned.sortedByCoord.out.bam.featureCounts.bam'
        self.barcodes_file = '/SGRNJ02/RandD4/RD20051303_Panel/20201218_2/\
S32_SUR0528_drug_S203_ZL/05.count/S32_SUR0528_drug_S203_ZL_matrix_10X/barcodes.tsv'
        self.index_file = '{self.sample}/05.snp/{self.sample}_cell_index.tsv'
        self.thread = 15
        self.fasta = '/SGRNJ/Public/Database/genome/homo_sapiens/ensembl_92/Homo_sapiens.GRCh38.fa'
        self.splitN_bam = '{self.sample}/05.snp/{self.sample}_splitN.bam'
        self.obj = Mutract(self.outdir, self.sample, self.bam, self.fasta, self.barcodes_file, thread=self.thread)
    '''
    
    @unittest.skip('tested')
    def test_split_bam(self):
        self.obj.split_bam()

    @unittest.skip('tested')
    def test_SplitNCigarReads(self):
        splitN_bam = self.obj.SplitNCigarReads()

    @unittest.skip('tested')
    def test_call_all_snp(self):
        self.obj.call_all_snp()

    @unittest.skip('tested')
    def test_merge_vcf(self):
        self.obj.merge_vcf()

    @unittest.skip('tested')
    def test_get_UMI(self):
        self.obj.vcf = f'{self.outdir}/{self.sample}_merged.vcf'
        self.obj.get_UMI()

    #@unittest.skip('tested')
    def test_run(self):
        self.obj.vcf = '/SGRNJ01/RD_dir/pipeline_test/zhouyiqi/mutract/20210108/sample1_merged.vcf'
        self.obj.run()

    @unittest.skip('tested')
    def test_get_matrix(self):
        df_UMI_file = f'{self.outdir}/{self.sample}_variant_count.tsv'
        self.obj.df_UMI = pd.read_csv(df_UMI_file, sep='\t')
        print(self.obj.df_UMI.head())
        self.obj.get_matrix()

    @unittest.skip('tested')
    def test_get_support_matrix(self):
        df_UMI_file = f'{self.outdir}/{self.sample}_variant_count.tsv'
        self.obj.df_UMI_file = df_UMI_file
        self.obj.get_support_matrix()
        print(self.obj.df_UMI.head())

    @unittest.skip('tested')
    def test_add_VID(self):
        self.obj.vcf = '/SGRNJ01/RD_dir/pipeline_test/zhouyiqi/mutract/20210108/sample1_merged.vcf'
        self.obj.add_VID()


    

if __name__ == '__main__':
    unittest.main()
