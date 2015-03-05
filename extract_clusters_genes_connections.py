#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Extract genes connections of each cluster"""

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
	parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)

	parser.add_argument('--clusters', dest='clusters_file', type=is_file, required=True, default=argparse.SUPPRESS,
			help='File which contains line by line, tab separated pairs of values <cluster name> <gene name>.')

	parser.add_argument('--genes-connections', dest='genes_connections_file', type=is_file, required=True, default=argparse.SUPPRESS,
			help='')

	parser.add_argument('--min-cluster-size', dest='min_cluster_size', type=int, default=1,
			help='Discard all clusters which have a size below this value.')

	parser.add_argument('--output-dir', dest='output_dir', type=is_dir, default='.',
			help='Directory in which genes connections of each cluster will be written')


	return parser.parse_args()

def parse_clusters(clusters_file):
	""" Read the clusters file and creates a dict which map a gene to the list of its clusters.
	"""

	cluster_to_genes = defaultdict(list)
	gene_to_cluster = dict()

	with open(clusters_file, 'r') as istream:
		for line in istream:
			cluster_name, gene_name = line.split()
			gene_name = int(gene_name)
			gene_to_cluster[gene_name] = cluster_name
			cluster_to_genes[cluster_name].append(gene_name)
	
	return gene_to_cluster, cluster_to_genes

def parse_connections(genes_connections_file):
	genes_connections = list()
	with open(genes_connections_file, 'r') as istream:
		for line in istream:
			gene1, gene2, num_connections = map(int, line.split())
			genes_connections.append((gene1, gene2, num_connections))
	return genes_connections

def dispatch_connections(gene_to_cluster, genes_connections):
	cluster_to_genes_connections = defaultdict(list)
	for gene1, gene2, num_connections in genes_connections:
		gene1_cluster = gene_to_cluster.get(gene1)
		gene2_cluster = gene_to_cluster.get(gene2)

		if gene1_cluster is not None and gene1_cluster == gene2_cluster:
			cluster_to_genes_connections[gene1_cluster].append((gene1,gene2, num_connections))
	
	return cluster_to_genes_connections

def write_clusters_genes_connections(cluster_to_genes_connections, output_dir):
	for cluster_name, genes_connections in cluster_to_genes_connections.items():
		output_file = os.path.join(output_dir, cluster_name + '_connections.txt')

		with open(output_file, 'w') as ostream:
			for gene1, gene2, num_connections in genes_connections:
				print("{0}\t{1}\t{2}".format(gene1,gene2, num_connections), file=ostream)


def main():
	parameters = get_parameters()
	print('STEP 1/4: Reading clusters file...')
	gene_to_cluster, cluster_to_genes = parse_clusters(parameters.clusters_file)
	print('STEP 2/4: Reading genes connections file...')
	genes_connections = parse_connections(parameters.genes_connections_file)
	print('STEP 3/4: Dispatching genes connections...')
	cluster_to_genes_connections = dispatch_connections(gene_to_cluster, genes_connections)
	print('STEP 3/4: Writing results...')
	write_clusters_genes_connections(cluster_to_genes_connections, parameters.output_dir)

if __name__ == '__main__':
	main()

