#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Extract genes of clusters from a gene catalog."""

from __future__ import print_function
import argparse
import os

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

	parser.add_argument('--clusters-file', dest='clusters_file', type=is_file, required=True, default=argparse.SUPPRESS,
			help='File which contains line by line, tab separated pairs of values <cluster name> <gene name>.')

	parser.add_argument('--annotation-file', dest='annotation_file', type=is_file, required=True, default=argparse.SUPPRESS,
			help='File which contains the annotation of all the genes.')

	parser.add_argument('--output-dir', dest='output_dir', type=is_dir, required=True, default='.',
			help='Directory in which clusters profile will be written.')

	parser.add_argument('--min-cluster-size', dest='min_cluster_size', type=int, default=1,
			help='Discard all clusters which have a size below this value.')

	return parser.parse_args()

def parse_clusters(clusters_file):
	""" Read the clusters file and creates a dict which map a gene to the list of its clusters.
	"""

	gene_to_clusters = dict()

	with open(clusters_file, 'r') as istream:
		for line in istream:
			cluster_name, gene_name = line.split()
			gene_name = int(gene_name)

			if gene_name in gene_to_clusters:
				gene_to_clusters[gene_name].append(cluster_name)
			else:
				gene_to_clusters[gene_name] = [cluster_name]
	
	return gene_to_clusters

def extract_clusters_annotation(annotation_file, gene_to_clusters):
	""" Read the annotation file and dispatch each gene annotation to its clusters.
	"""

	clusters_annotation = dict()
	with open(annotation_file, 'r') as istream:
		for line in istream:
			gene_num = int(line.split(None,1)[0])

			if gene_num in gene_to_clusters:
				for cluster_name in gene_to_clusters[gene_num]:
					if cluster_name in clusters_annotation:
						clusters_annotation[cluster_name].append(line)
					else:
						clusters_annotation[cluster_name] = [line]

	return clusters_annotation


def write_clusters_annotation(output_dir, clusters_annotation, min_cluster_size):
	for cluster_name in clusters_annotation:

		if len(clusters_annotation[cluster_name]) < min_cluster_size :
			continue

		output_file = os.path.join(output_dir, cluster_name + '.annotation.txt')

		with open(output_file, 'w') as ostream:
			for line in clusters_annotation[cluster_name]:
				print(line, file=ostream)

def main():
	parameters = get_parameters()
	print('STEP 1/3: Reading clusters file...')
	gene_to_clusters = parse_clusters(parameters.clusters_file)
	print('STEP 2/3: Extracting clusters annotation from annotation file...')
	clusters_annotation = extract_clusters_annotation(parameters.annotation_file, gene_to_clusters)
	print('STEP 3/3: Writing clusters annotation...')
	write_clusters_annotation(parameters.output_dir, clusters_annotation, parameters.min_cluster_size)

if __name__ == '__main__':
	main()

