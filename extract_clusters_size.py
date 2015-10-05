#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Extract clusters size"""

from __future__ import print_function
import argparse
import sys
import operator
from collections import defaultdict

__author__ = "Florian Plaza Oñate"
__copyright__ = "Copyright 2014, Enterome"
__version__ = "1.0.0"
__maintainer__ = "Florian Plaza Oñate"
__email__ = "fplaza-onate@enterome.com"
__status__ = "Development"


def get_parameters():
    """Parse command line parameters.
    """
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('--clusters-file', dest='clusters_file', type=argparse.FileType('r'), required=True, default=argparse.SUPPRESS,
        help='File which contains line by line, tab separated pairs of values <cluster name> <gene name>.')

    parser.add_argument('--output-file', dest='output_file', type=argparse.FileType('w'),default='clusters_size.txt',
        help='File in which clusters size will be written.')

    parser.add_argument('--min-cluster-size', dest='min_cluster_size', type=int, default=1,
        help='Discard all clusters which have a size below this value.')

    parser.add_argument('--max-cluster-size', dest='max_cluster_size', type=int, default=sys.maxint,
        help='Discard all clusters which have a size above this value.')

    return parser.parse_args()

def get_clusters_size(clusters_file):
    """ Read the clusters file and creates a dict which map each cluster to its size
    """

    clusters_size = defaultdict(int) 

    with clusters_file as clusters_file:
        for line in clusters_file:
            cluster_name = line.split(None, 1)[0]
            clusters_size[cluster_name] += 1

    return clusters_size


def write_clusters_size(clusters_size, min_cluster_size, max_cluster_size, output_file):
    clusters_size = sorted(clusters_size.iteritems(), key=operator.itemgetter(1), reverse=True)

    with output_file as output_file:
        for cluster_name, cluster_size in clusters_size:
            if (cluster_size >= min_cluster_size) and (cluster_size <= max_cluster_size):
                print('{0}\t{1}'.format(cluster_name, cluster_size), file=output_file)


def main():
    parameters = get_parameters()
    print('STEP 1/2: Computing clusters size')
    clusters_size = get_clusters_size(parameters.clusters_file)
    print('STEP 2/2: Writing clusters size')
    write_clusters_size(clusters_size, parameters.min_cluster_size, parameters.max_cluster_size, parameters.output_file)
    print('Done!')

if __name__ == '__main__':
    main()

