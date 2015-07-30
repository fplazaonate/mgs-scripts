#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Extract annotation of each cluster"""

from __future__ import print_function
import argparse
import os
from collections import defaultdict

__author__ = "Florian Plaza Oñate"
__copyright__ = "Copyright 2014-2015, Enterome"
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
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('--clusters-file', dest='clusters_file', type=is_file, required=True, default=argparse.SUPPRESS,
            help='File which contains line by line, tab separated pairs of values <cluster name> <gene name>.')

    parser.add_argument('--annotation-file', dest='annotation_file', type=is_file, required=True, default=argparse.SUPPRESS,
            help='File which contains the annotation of all the genes.')

    parser.add_argument('--output-file', dest='output_file', required=True, default=argparse.SUPPRESS,
            help='Output file in which clusters annotation will be written.')

    parser.add_argument('--min-cluster-size', dest='min_cluster_size', type=int, default=1,
            help='Discard all clusters which have a size below this value.')

    return parser.parse_args()

def parse_clusters(clusters_file):
    """ Read the clusters file and creates a dict which map a gene to the list of its clusters.
    """

    gene_to_clusters = defaultdict(list)

    with open(clusters_file, 'r') as clusters_file_istream:
        for line in clusters_file_istream:
            cluster_name, gene_name = line.split()
            gene_name = int(gene_name)

            gene_to_clusters[gene_name].append(cluster_name)
    
    return gene_to_clusters

def extract_clusters_annotation(annotation_file, gene_to_clusters):
    """ Read the annotation file and dispatch each gene annotation to its clusters.
    """

    clusters_annotation = defaultdict(list)
    with open(annotation_file, 'r') as annotation_file_istream:
        for gene_num, annot in enumerate(annotation_file_istream, start=1):
            if gene_num in gene_to_clusters:
                for cluster_name in gene_to_clusters[gene_num]:
                    clusters_annotation[cluster_name].append(annot)

    return clusters_annotation


def write_clusters_annotation(output_file, clusters_annotation, min_cluster_size):

    with open(output_file, 'w') as output_file_ostream:
	for cluster_name in clusters_annotation:

	    if len(clusters_annotation[cluster_name]) < min_cluster_size :
		continue

	    for annot in clusters_annotation[cluster_name]:
		print('{0}\t{1}'.format(cluster_name, annot), file=output_file_ostream, end='')

def main():
    parameters = get_parameters()
    print('STEP 1/3: Reading clusters file...')
    gene_to_clusters = parse_clusters(parameters.clusters_file)
    print('STEP 2/3: Extracting clusters annotation from annotation file...')
    clusters_annotation = extract_clusters_annotation(parameters.annotation_file, gene_to_clusters)
    print('STEP 3/3: Writing clusters annotation...')
    write_clusters_annotation(parameters.output_file, clusters_annotation, parameters.min_cluster_size)

if __name__ == '__main__':
    main()

