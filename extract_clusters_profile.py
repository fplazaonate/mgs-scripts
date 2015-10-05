#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Extract clusters profile from profiles table."""

from __future__ import print_function
import argparse
import os
import sys
from collections import defaultdict

__author__ = "Florian Plaza Oñate"
__copyright__ = "Copyright 2014, Enterome"
__version__ = "1.0.0"
__maintainer__ = "Florian Plaza Oñate"
__email__ = "fplaza-onate@enterome.com"
__status__ = "Development"

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
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('--clusters-file', dest='clusters_file', type=argparse.FileType('r'), required=True, default=argparse.SUPPRESS,
        help='File which contains line by line, tab separated pairs of values <cluster name> <gene name>.')

    parser.add_argument('--profiles-file', dest='profiles_file', type=argparse.FileType('r'), required=True, default=argparse.SUPPRESS,
        help='File which contains a list of genes and their profile.')

    parser.add_argument('--output-dir', dest='output_dir', type=is_dir, required=True, default='.',
        help='Directory in which clusters profile will be written.')

    parser.add_argument('--with-header', dest='with_header', action='store_true', default=False,
    help='Indicates whether the profiles file has an header with the names of samples.')

    parser.add_argument('--min-cluster-size', dest='min_cluster_size', type=int, default=1,
        help='Discard all clusters which have a size below this value.')

    parser.add_argument('--max-cluster-size', dest='max_cluster_size', type=int, default=sys.maxint,
        help='Discard all clusters which have a size above this value.')


    return parser.parse_args()

def parse_clusters(clusters_file):
    """ Read the clusters file and creates a dict which map a gene to the list of its clusters.
    """

    gene_to_clusters = defaultdict(list)

    with clusters_file as clusters_file:
        for line in clusters_file:
            line_items = line.split()
            cluster_name, gene_name = line_items[0], line_items[1]
            gene_to_clusters[gene_name].append(cluster_name)

    return gene_to_clusters

def extract_clusters_profile(profiles_file, with_header, gene_to_clusters):
    """ Read the profiles table and dispatch each gene profile to its clusters.
    """

    clusters_profile = defaultdict(list)

    with profiles_file as profiles_file:
        if with_header:
            profiles_file.next()

        for line in profiles_file:
            gene_name = line.split(None,1)[0]

            if gene_name in gene_to_clusters:
                for cluster_name in gene_to_clusters[gene_name]:
                    clusters_profile[cluster_name].append(line)

    return clusters_profile

def write_clusters_profile(output_dir, clusters_profile, min_cluster_size, max_cluster_size):
    for cluster_name in clusters_profile:

        cluster_size = len(clusters_profile[cluster_name])
        if (cluster_size < min_cluster_size) or (cluster_size > max_cluster_size)  :
            continue

        output_file = os.path.join(output_dir, cluster_name + '_profile.txt')

        with open(output_file, 'w') as ostream:
            for line in clusters_profile[cluster_name]:
                ostream.write(line)

def main():
    parameters = get_parameters()
    print('STEP 1/3: Reading clusters file...')
    gene_to_clusters = parse_clusters(parameters.clusters_file)
    print('STEP 2/3: Extracting clusters profile from profiles file...')
    clusters_profile = extract_clusters_profile(parameters.profiles_file, parameters.with_header, gene_to_clusters)
    print('STEP 3/3: Writing clusters profile...')
    write_clusters_profile(parameters.output_dir, clusters_profile, parameters.min_cluster_size, parameters.max_cluster_size)

if __name__ == '__main__':
    main()

