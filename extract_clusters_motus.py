#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Extract mOTUs of each cluster"""

from __future__ import print_function
import argparse
import os
from collections import defaultdict

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


def is_dir(path):
    """Check if path is an existing file.
    """

    if not os.path.isdir(path):
        if os.path.isfile(path):
            msg = "{0} is a file.".format(path)
        else:
            msg = "{0} does not exist.".format(path)
        raise argparse.ArgumentTypeError(msg)

    return path

def get_parameters():
    """Parse command line parameters.
    """
    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument('--clusters-file', dest='clusters_file', type=is_file, required=True,
            help='File which contains line by line, tab separated pairs of values <cluster name> <gene name>.')

    parser.add_argument('--motus-file', dest='motus_file', type=is_file, required=True,
            help='Multi-FASTA file which contains all the genes.')

    parser.add_argument('--output-dir', dest='output_dir', type=is_dir, required=True, default='.',
            help='Directory in which mOTUs of each cluster will be written.')

    parser.add_argument('--min-cluster-size', dest='min_cluster_size', type=int, default=1,
            help='Discard clusters which have a size below this value.')

    return parser.parse_args()

def parse_clusters_file(clusters_file, min_cluster_size):
    """ Read the clusters file and creates a dict which maps a cluster to the list of its genes
    """

    cluster_to_genes = defaultdict(list)

    with open(clusters_file, 'r') as istream:
        for line in istream:
            cluster_name, gene_name = line.split()
            cluster_to_genes[cluster_name].append(gene_name)

    return dict((cluster,cluster_genes)
            for cluster,cluster_genes in cluster_to_genes.items() if len(cluster_genes) >= min_cluster_size)

def parse_motus_file(motus_file):
    """ Read the mOTUs file 
    """

    all_motus = set()
    gene_to_motu = dict()

    with open(motus_file, 'r') as istream:
        for line in istream:
            line_items = line.split()
            gene_name, motu_name = line_items[0], line_items[-1]
            all_motus.add(motu_name)
            gene_to_motu[gene_name] = motu_name
    
    return sorted(all_motus), gene_to_motu

def extract_clusters_motus(cluster_to_genes, all_motus, gene_to_motu):
    cluster_motus = dict()
    for cluster, cluster_genes in cluster_to_genes.items():

        cluster_motus[cluster] = dict((motu_name,[]) for motu_name in all_motus)

        for gene_name in cluster_genes:
            if gene_name in gene_to_motu:
                cluster_motus[cluster][gene_to_motu[gene_name]].append(gene_name)

    return cluster_motus

def write_clusters_motus(output_dir, cluster_to_genes, cluster_motus, all_motus):
    for cluster_name, cluster_genes in cluster_to_genes.items():

        output_file = os.path.join(output_dir, cluster_name + '.mOTUs.txt')

        with open(output_file, 'w') as ostream:
            for motu in all_motus:
                print("{0}={1}".format(motu,','.join(cluster_motus[cluster_name][motu])), file=ostream)

def main():
    parameters = get_parameters()
    print('STEP 1/3: Reading clusters file...')
    cluster_to_genes = parse_clusters_file(parameters.clusters_file, parameters.min_cluster_size)
    print('STEP 2/4: Reading mOTUs file...')
    all_motus, gene_to_motu = parse_motus_file(parameters.motus_file)
    print('STEP 3/4: Extracting clusters mOTUs...')
    cluster_motus = extract_clusters_motus(cluster_to_genes, all_motus, gene_to_motu)
    print('STEP 4/4: Writing clusters mOTUs...')
    write_clusters_motus(parameters.output_dir, cluster_to_genes, cluster_motus, all_motus)

if __name__ == '__main__':
    main()

