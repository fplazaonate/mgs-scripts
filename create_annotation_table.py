#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Creates the annotation table of a genes catalog"""

from __future__ import print_function
import argparse
import os

__author__ = "Florian Plaza Oñate"
__copyright__ = "Copyright 2015, Enterome"
__version__ = "1.0.0"
__maintainer__ = "Florian Plaza Oñate"
__email__ = "fplaza-onate@enterome.com"
__status__ = "Development"

def is_file(path):
    """Check if path is an existing file.
    """

    if not os.path.isfile(path):
        if os.path.isdir(path):
            msg = "{0} is a directory".format(path)
        else:
            msg = "{0} does not exist.".format(path)
            raise argparse.ArgumentTypeError(msg)
    return path

def get_parameters():
    """Parse command line parameters.
    """
    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument('-g','--genes-catalog', dest='genes_catalog', type=is_file, required=True,
        help='Multi-FASTA file which contains all the genes of the catalog')

    parser.add_argument('-t', '--taxonomic-annotation', dest='taxonomic_annotation', type=is_file, required=True,
        help='Taxonomic annotation of the genes catalog.')

    parser.add_argument('-f', '--functional-annotation' , dest='functional_annotation', type=is_file, required=True,
        help='Functional annotation of the genes catalog.')

    parser.add_argument('-a', '--annotation-table' , dest='annotation_table', required=True,
        help='Final annotation table.')

    return parser.parse_args()

def index_genes(genes_catalog):
    with open(genes_catalog, 'r') as genes_catalog_is:
        genes_list = [line.split()[0][1:] for line in genes_catalog_is if line.startswith('>')]
    return genes_list

def index_taxonomic_annotation(taxonomic_annotation):
    gene_to_tax_annot = dict()
    with open(taxonomic_annotation,'r') as taxonomic_annotation_is: 
        for tax_annot in taxonomic_annotation_is:
            tax_annot_items = tax_annot.split('\t')
            gene_name = tax_annot_items[0]
            gene_to_tax_annot[gene_name] = '\t'.join(tax_annot_items[1:-1])
    return gene_to_tax_annot


def index_functional_annotation(functional_annotation):
    gene_to_func_annot = dict()

    with open(functional_annotation, 'r') as functional_annotation_is:
        for func_annot in functional_annotation_is:
            func_annot_items = func_annot.split()
            gene_name = func_annot_items[1]
            gene_annot = func_annot_items[2]
            gene_to_func_annot[gene_name] = gene_annot
    return gene_to_func_annot

def write_annotation_table(genes_list, gene_to_tax_annot, gene_to_func_annot, annotation_table):
    with open(annotation_table, 'w') as annotation_table_is:
        for gene_name in genes_list:
            print('{0}\t{1}\t{2}'.format(gene_name, gene_to_tax_annot[gene_name], gene_to_func_annot.get(gene_name, 'NA')), sep='', file=annotation_table_is)


def main():
    parameters = get_parameters()

    print('STEP 1/4: Indexing genes catalog...')
    genes_list = index_genes(parameters.genes_catalog)
    print('STEP 2/4: Indexing taxonomic annotation file...')
    gene_to_tax_annot = index_taxonomic_annotation(parameters.taxonomic_annotation)
    print('STEP 3/4: Indexing functional annotation file...')
    gene_to_func_annot = index_functional_annotation(parameters.functional_annotation)
    print('STEP 4/4: Writing final annotation table...')
    write_annotation_table(genes_list, gene_to_tax_annot, gene_to_func_annot, parameters.annotation_table)

if __name__ == '__main__':
    main()

