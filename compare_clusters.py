#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Compare clusters generated with two different methods."""

from __future__ import print_function
import argparse
import os
from collections import defaultdict

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
	parser = argparse.ArgumentParser(description=__doc__)

	parser.add_argument('-r', '--ref', dest='reference', type=is_file, required=True, help='')

	parser.add_argument('-q', '--query', dest='query', type=is_file, required=True, help='')

	parser.add_argument('-o', '--output-file', dest='output_file', required=True, help='')

	parser.add_argument('--query-min-cluster-size', dest='query_min_cluster_size', type=int, default=1, help='')

	return parser.parse_args()

def index_reference(reference):
	""" Read the reference and creates a dict which map each gene to the list of its clusters.
	"""

	gene_to_clusters = defaultdict(list)

	with open(reference, 'r') as istream:
		for line in istream:
			cluster_name, gene_name = line.split()
			gene_to_clusters[gene_name].append(cluster_name)
	
	return gene_to_clusters

def index_query(query, min_cluster_size):
	""" Read the query and creates a dict which map each cluster to the list of its genes.
	"""
	cluster_to_genes = defaultdict(list)

	with open(query, 'r') as istream:
		for line in istream:
			cluster_name, gene_name = line.split()
			cluster_to_genes[cluster_name].append(gene_name)

	cluster_to_genes = dict((cluster,genes) for cluster,genes in cluster_to_genes.iteritems() if len(genes) >= min_cluster_size)

	return cluster_to_genes

def compare_clusters(gene_to_cluster_ref, cluster_to_genes_query):
	clusters_query_to_clusters_ref = dict()
	for cluster_query in cluster_to_genes_query.keys():
		clusters_query_to_clusters_ref[cluster_query] = defaultdict(int)
		for gene_query in cluster_to_genes_query[cluster_query]:
			if gene_query in gene_to_cluster_ref :
				for cluster_ref in gene_to_cluster_ref[gene_query]:
					clusters_query_to_clusters_ref[cluster_query][cluster_ref] += 1
			else:
				clusters_query_to_clusters_ref[cluster_query]['unknown'] += 1

	return clusters_query_to_clusters_ref

def write_results(clusters_query_to_clusters_ref, cluster_to_genes_query, output_file):
	with open(output_file, 'w') as ostream:
		for cluster_query in clusters_query_to_clusters_ref.keys():
			print("{0}: {1} genes".format(cluster_query, len(cluster_to_genes_query[cluster_query])), file=ostream)
			for cluster_ref in clusters_query_to_clusters_ref[cluster_query].keys():
				print("\t{0}\t{1}".format(cluster_ref, clusters_query_to_clusters_ref[cluster_query][cluster_ref]), file=ostream)
			print("", file=ostream)
def main():
	parameters = get_parameters()
	print('STEP 1/4: Indexing reference...')
	gene_to_cluster_ref = index_reference(parameters.reference)
	print('STEP 2/4: Indexing query...')
	cluster_to_genes_query = index_query(parameters.query, parameters.query_min_cluster_size)
	print('STEP 3/4: Comparing the query to the reference...')
	clusters_query_to_clusters_ref = compare_clusters(gene_to_cluster_ref, cluster_to_genes_query)
	print('STEP 4/4: Writing results...')
	write_results(clusters_query_to_clusters_ref, cluster_to_genes_query, parameters.output_file)

if __name__ == '__main__':
	main()

