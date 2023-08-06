import logging
import os
import pysam
import os
import numpy as np
import pandas as pd
import subprocess

from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor
from scipy.io import mmwrite
from scipy.sparse import coo_matrix


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger()


def read_CID(CID_file):
    df_index = pd.read_csv(CID_file, sep='\t', index_col=0, dtype=object)
    df_valid = df_index[df_index['valid'] == 'True']
    return df_index, df_valid


def read_one_col(file):
    df = pd.read_csv(file, header=None)
    col1 = list(df.iloc[:, 0])
    num = len(col1)
    return col1, num


class Mutract():

    def __init__(self, outdir, sample, bam, fasta, barcodes_file, vcf=None, thread=1, gene_file=None):
        self.outdir = outdir
        self.sample = sample
        self.bam = bam
        self.fasta = fasta
        self.barcodes, _num = read_one_col(barcodes_file)
        self.barcodes.sort()
        self.vcf = vcf
        self.CID_file = f'{self.outdir}/{self.sample}_CID.tsv'
        self.VID_file = f'{self.outdir}/{self.sample}_VID.tsv'
        self.thread = thread
        self.gene_file = gene_file
        if self.gene_file:
            self.gene_list, _num = read_one_col(self.gene_file)

        if not os.path.exists(outdir):
            os.mkdir(outdir)


    def SplitNCigarReads(self):
        splitN_bam = f'{self.outdir}/{self.sample}_splitN.bam'
        cmd = (
            f'gatk '
            f'SplitNCigarReads '
            f'-R {self.fasta} '
            f'-I {self.bam} '
            f'-O {splitN_bam} '
        )
        logger.info(cmd)
        subprocess.check_call(cmd, shell=True)
        self.bam = splitN_bam
        return splitN_bam


    def split_bam(self):
        '''
        input:
            bam: bam from splitN
            barcodes: cell barcodes, list

        ouput:
            bam_dict: assign reads to cell barcodes and UMI
            count_dict: UMI counts per cell
            CID: assign ID(1-based) to cells
        '''

        # init
        count_dict = defaultdict(dict)
        bam_dict = defaultdict(list)
        CID_dict = defaultdict(dict)
        cells_dir = f'{self.outdir}/cells/'
    
        # read bam and split
        samfile = pysam.AlignmentFile(self.bam, "rb")
        header = samfile.header
        for read in samfile:
            attr = read.query_name.split('_')
            barcode = attr[0]
            umi = attr[1]
            if self.gene_file:
                if not read.has_tag('GN'):
                    continue
                gene_name = read.get_tag('GN')
                if not gene_name in self.gene_list:
                    continue
            if barcode in self.barcodes:
                CID = self.barcodes.index(barcode) + 1
                read.set_tag(tag='CL', value=f'CELL{CID}', value_type='Z')

                # assign read to barcode
                bam_dict[barcode].append(read)

                # count
                if self.gene_file:
                    if gene_name not in count_dict[barcode]:
                        count_dict[barcode][gene_name] = {}
                    if umi in count_dict[barcode][gene_name]:
                        count_dict[barcode][gene_name][umi] += 1
                    else:
                        count_dict[barcode][gene_name][umi] = 1

        logger.info('writing cell bam...')
        # write new bam
        CID = 0
        for barcode in self.barcodes:
            # init
            CID += 1
            CID_dict[CID]['barcode'] = barcode
            CID_dict[CID]['valid'] = False

            # out bam
            if barcode in bam_dict:
                cell_dir = f'{cells_dir}/cell{CID}'
                cell_bam_file = f'{cell_dir}/cell{CID}.bam'
                if not os.path.exists(cell_dir):
                    os.makedirs(cell_dir)
                CID_dict[CID]['valid'] = True
                cell_bam = pysam.AlignmentFile(
                    f'{cell_bam_file}', "wb", header=header)
                for read in bam_dict[barcode]:
                    cell_bam.write(read)
                cell_bam.close()

        # out CID
        df_CID = pd.DataFrame(CID_dict).T
        df_CID.index.name = 'CID'
        df_CID.to_csv(self.CID_file, sep='\t')

        # out count_dict
        if self.gene_file:
            df_count = pd.DataFrame(columns=['barcode', 'gene', 'UMI_count'])
            for barcode in count_dict:
                for gene in count_dict[barcode]:
                    umi_count = len(count_dict[barcode][gene])
                    df_count = df_count.append({
                        'barcode': barcode,
                        'gene': gene,
                        'UMI_count': umi_count,
                    }, ignore_index=True)
            count_file = f'{self.outdir}/{self.sample}_count.tsv'
            df_count.to_csv(count_file, sep='\t', index=False)


    def call_snp(self, CID):

        logging.info(f'Processing Cell {CID}')
        bam = f'{self.outdir}/cells/cell{CID}/cell{CID}.bam'
        # sort
        sorted_bam = f'{self.outdir}/cells/cell{CID}/cell{CID}_sorted.bam'
        cmd_sort = (
            f'samtools sort {bam} -o {sorted_bam}'
        )
        subprocess.check_call(cmd_sort, shell=True)
    
        # mpileup
        bcf = f'{self.outdir}/cells/cell{CID}/cell{CID}.bcf'
        cmd_mpileup = (
            f'bcftools mpileup -Ou '
            f'-f {self.fasta} '
            f'{sorted_bam} -o {bcf} '
        )
        subprocess.check_call(cmd_mpileup, shell=True)

        # call
        out_vcf = f'{self.outdir}/cells/cell{CID}/cell{CID}.vcf'
        cmd_call = (
            f'bcftools call -mv -Ov '
            f'-o {out_vcf} '
            f'{bcf}'
            f'>/dev/null 2>&1 '
        )
        subprocess.check_call(cmd_call, shell=True)

        # norm
        norm_vcf = f'{self.outdir}/cells/cell{CID}/cell{CID}_norm.vcf'
        cmd_norm = (
            f'bcftools norm -d none '
            f'-f {self.fasta} '
            f'{out_vcf} '
            f'-o {norm_vcf} '
        )
        subprocess.check_call(cmd_norm, shell=True)

        # call all position
        out_all_vcf = f'{self.outdir}/cells/cell{CID}/cell{CID}_all.vcf'
        cmd_all_call = (
            f'bcftools call -m -Ov '
            f'-o {out_all_vcf} '
            f'{bcf}'
            f'>/dev/null 2>&1 '
        )
        subprocess.check_call(cmd_all_call, shell=True)

        # norm all
        norm_all_vcf = f'{self.outdir}/cells/cell{CID}/cell{CID}_all_norm.vcf'
        cmd_all_norm = (
            f'bcftools norm -d none '
            f'-f {self.fasta} '
            f'{out_all_vcf} '
            f'-o {norm_all_vcf} '
        )
        subprocess.check_call(cmd_all_norm, shell=True)


    def call_all_snp(self):
        all_res = []
        _df_index, df_valid = read_CID(self.CID_file)
        CID_arg = df_valid.index
        with ProcessPoolExecutor(self.thread) as pool:
            for res in pool.map(self.call_snp, CID_arg):
                all_res.append(res)


    @staticmethod
    def parse_vcf(vcf_file, cols=['chrom', 'pos', 'alleles'], infos=['VID']):
        '''
        parse_ vcf into df
        '''
        vcf = pysam.VariantFile(vcf_file)
        df = pd.DataFrame(columns=[col for col in cols] + infos)
        rec_dict = {}
        for rec in vcf.fetch():

            for col in cols:
                rec_dict[col] = getattr(rec, col)
                if col == 'alleles':
                    rec_dict['ref'] = rec_dict['alleles'][0]
                    rec_dict['alt'] = '.'
                    if len(rec_dict['alleles']) == 2:
                        rec_dict['alt'] = rec_dict['alleles'][1]
                    
            for info in infos:
                rec_dict[info] = rec.info[info]

            df = df.append(pd.Series(rec_dict),ignore_index=True)
        return df


    def merge_vcf(self):
        '''
        merge cell vcf into one non-duplicated vcf
        add VID(variant ID) and CID(cell ID)
        '''
        _df_index, df_valid = read_CID(self.CID_file)
        CIDs = df_valid.index

        # variant dict
        v_cols = ['chrom', 'pos', 'alleles']
        v_dict = {}

        for CID in CIDs:
            CID = str(CID)
            vcf_file = f'{self.outdir}/cells/cell{CID}/cell{CID}_norm.vcf'
            vcf = pysam.VariantFile(vcf_file,'r')
            for rec in vcf.fetch():
                v = ','.join([str(getattr(rec, col)) for col in v_cols])
                if not v in v_dict:
                    v_dict[v] = dict()
                    v_dict[v]['CID'] = [CID]
                    v_dict[v]['record'] = rec
                else:
                    v_dict[v]['CID'].append(CID)

        # output
        def get_vcf_header(CIDs):
            CID = CIDs[0]
            vcf_file = f'{self.outdir}/cells/cell{CID}/cell{CID}_norm.vcf'
            vcf = pysam.VariantFile(vcf_file,'r')
            return vcf.header
        vcf_header = get_vcf_header(CIDs)
        merged_vcf_file = f'{self.outdir}/{self.sample}_merged.vcf'
        vcf_header.info.add('VID', number=1, type='String', description='Variant ID')
        vcf_header.info.add('CID', number=1, type='String', description='Cell ID')
        merged_vcf = pysam.VariantFile(merged_vcf_file,'w', header=vcf_header)

        VID = 0
        for v in sorted(v_dict.keys()):
            VID += 1
            rec = v_dict[v]['record']
            CID = ','.join(v_dict[v]['CID'])
            record = merged_vcf.new_record()
            cols = ['chrom', 'pos', 'alleles']
            for col in cols:
                setattr(record,col, getattr(rec,col))
            record.info['VID'] = str(VID)
            record.info['CID'] = CID
            merged_vcf.write(record)

        merged_vcf.close()
        self.vcf = merged_vcf_file


    def get_VID_file(self):
        self.df_vcf = Mutract.parse_vcf(self.vcf)
        # out VID file
        df_VID = self.df_vcf.loc[:,['VID', 'chrom', 'pos', 'ref', 'alt']]
        df_VID.to_csv(self.VID_file, sep='\t', index=False)


    def add_VID(self):
        vcf = pysam.VariantFile(self.vcf,'r')
        vcf_header = vcf.header
        if 'VID' in vcf_header.info:
            logging.info('VID is already in vcf file!')
            return
        vcf_header.info.add('VID', number=1, type='String', description='Variant ID')
        self.VID_vcf_file = f'{self.outdir}/{self.sample}_VID.vcf'
        VID_vcf = pysam.VariantFile(self.VID_vcf_file, 'w', header=vcf_header)
        VID = 0
        for rec in vcf.fetch():
            VID += 1
            rec.info['VID'] = str(VID) 
            VID_vcf.write(rec)
        VID_vcf.close()
        self.vcf = self.VID_vcf_file


    def cell_UMI(self, CID):
        logger.info(f'Processing cell {CID}')
        df_UMI = pd.DataFrame(columns=['VID', 'CID', 'ref_count', 'alt_count'])
        norm_all_vcf = f'{self.outdir}/cells/cell{CID}/cell{CID}_all_norm.vcf'
        df_cell_vcf = Mutract.parse_vcf(norm_all_vcf, infos=['DP4'])

        def get_DP4(row, alt):
            DP4 = row['DP4'].iloc[0]
            if alt == 'ref':
                indexs = [0,1]
            elif alt == 'alt':
                indexs = [2,3]
            umi = sum([DP4[index] for index in indexs])
            return umi

        def map_vcf_row(row, df_cell_vcf):
            pos = row['pos']
            chrom = row['chrom']
            alt = row['alt']
            df_pos = df_cell_vcf[(df_cell_vcf['pos']==pos) & (df_cell_vcf['chrom']==chrom)]
            df_ref = df_pos[df_pos['alt']=='.']
            df_alt = df_pos[df_pos['alt']==alt]
            ref_UMI = 0
            alt_UMI = 0
            if df_ref.shape[0] != 0:
                ref_UMI = get_DP4(df_ref, 'ref')
            if df_alt.shape[0] != 0:
                alt_UMI = get_DP4(df_alt, 'alt')
            return ref_UMI, alt_UMI, pos, chrom, alt

        for index in self.df_vcf.index:
            row = self.df_vcf.loc[index,]
            ref_UMI, alt_UMI, pos, chrom, alt = map_vcf_row(row, df_cell_vcf)
            if (ref_UMI + alt_UMI) != 0:
                ref = row['ref']
                VID = row['VID']
                dic = {
                    'VID':VID,
                    'CID':CID,
                    'ref_count':ref_UMI, 
                    'alt_count':alt_UMI,
                }
                df_UMI = df_UMI.append(dic, ignore_index=True)
        return df_UMI

    def get_UMI(self):
        '''
        get variant and ref UMI supporting an allele
        '''
        logger.info('get_UMI start...')
        _df_index, df_valid =  read_CID(self.CID_file)

        df_UMI_list = []
        with ProcessPoolExecutor(self.thread) as pool:
            for res in pool.map(self.cell_UMI, list(df_valid.index)):
                df_UMI_list.append(res)
        
        df_UMI = pd.concat(df_UMI_list)
        df_UMI_file = f'{self.outdir}/{self.sample}_variant_count.tsv'
        df_UMI['VID'] = df_UMI['VID'].astype('int')
        df_UMI.sort_values(by=['VID','CID'], inplace=True)
        df_UMI.to_csv(df_UMI_file, sep='\t', index=False)
        self.df_UMI_file = df_UMI_file

    def get_matrix(self):
        ref_mtx_file = f'{self.outdir}/{self.sample}_ref.mtx'
        alt_mtx_file = f'{self.outdir}/{self.sample}_alt.mtx'
        df_ref = self.df_UMI[self.df_UMI.ref_count!=0]
        df_alt = self.df_UMI[self.df_UMI.alt_count!=0]
        ref_mtx= coo_matrix((df_ref.ref_count, 
            (df_ref.VID - 1, df_ref.CID - 1)))
        alt_mtx= coo_matrix((df_alt.alt_count, 
            (df_alt.VID - 1, df_alt.CID - 1)))
        mmwrite(ref_mtx_file, ref_mtx)
        mmwrite(alt_mtx_file, alt_mtx)
    
    def get_support_matrix(self):
        support_mtx_file = f'{self.outdir}/{self.sample}_support.mtx'
        def set_support(row):
            ref_bit = 1 if row['ref_count'] > 0 else 0
            alt_bit = 2 if row['alt_count'] > 0 else 0
            support_bit = ref_bit + alt_bit
            return support_bit

        self.df_UMI = pd.read_csv(self.df_UMI_file, sep='\t')
        self.df_UMI['support'] = self.df_UMI.apply(set_support, axis=1)
        support_mtx = coo_matrix((self.df_UMI.support, 
            (self.df_UMI.VID - 1, self.df_UMI.CID - 1)))       
        mmwrite(support_mtx_file, support_mtx)
                    

    def run(self):
        self.SplitNCigarReads()
        self.split_bam()
        self.call_all_snp()
        if self.vcf:
            self.add_VID()
        else:
            self.merge_vcf()
        self.get_VID_file()
        self.get_UMI()
        self.get_support_matrix()

