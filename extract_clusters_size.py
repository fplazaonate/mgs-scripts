#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Extract clusters size"""

from __future__ import print_function
import argparse
import os
import itertools
import string
import operator

__author__ = "Florian Plaza Oñate"
__copyright__ = "Copyright 2014, Enterome"
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

	parser.add_argument('--output-file', dest='output_file', default='clusters_size.txt',
			help='File in which clusters size will be written.')

	parser.add_argument('--min-cluster-size', dest='min_cluster_size', type=int, default=1,
			help='Discard all clusters which have a size below this value.')
	
	return parser.parse_args()

def get_clusters_size(clusters_file):
	""" Read the clusters file and creates a dict which map each cluster to its size
	"""

	clusters_size = dict()

	with open(clusters_file, 'r') as istream:
		for line in istream:
			cluster_name = line.split(None, 1)[0]
			if cluster_name in clusters_size:
				clusters_size[cluster_name] = clusters_size[cluster_name] + 1
			else:
				clusters_size[cluster_name] = 1
	
	return clusters_size


def write_clusters_size(clusters_size, output_file):
	clusters_size = sorted(clusters_size.iteritems(), key=operator.itemgetter(1), reverse=True)

	with open(output_file, 'w') as ostream:
		for cluster_name, clusters_size in clusters_size:
			print("{0}\t{1}".format(cluster_name, clusters_size), file=ostream)
			

def main():
	parameters = get_parameters()
	print('STEP 1/2: Computing clusters size')
	clusters_size = get_clusters_size(parameters.clusters_file)
	print('STEP 2/2: Writing clusters size to {0}'.format(parameters.output_file))
	write_clusters_size(clusters_size, parameters.output_file)
	print('Done!')

if __name__ == '__main__':
	main()

