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

	parser.add_argument('-r', '--ref-file', dest='reference_file', type=is_file, required=True, help='')

	parser.add_argument('-q', '--query-file', dest='query_file', type=is_file, required=True, help='')

	parser.add_argument('-o', '--output-file', dest='output_file', required=True, help='')

	parser.add_argument('--query-min-cluster-size', dest='query_min_cluster_size', type=int, default=1, help='')

	return parser.parse_args()

def parse_clusters_file(istream):
	cluster_name, gene_name = None, None

	for line in istream:
		if cluster_name:
			yield cluster_name, gene_name
		cluster_name, gene_name = line.split()
	
	if cluster_name:
		yield cluster_name, gene_name

def index_clusters(clusters_file, min_cluster_size=None):
	gene_to_clusters = defaultdict(list)
	cluster_to_genes = defaultdict(list)

	with open(clusters_file, 'r') as istream:
		for cluster_name, gene_name in parse_clusters_file(istream):
			gene_to_clusters[gene_name].append(cluster_name)
			cluster_to_genes[cluster_name].append(gene_name)

	if min_cluster_size:
		cluster_to_genes = dict((cluster,genes) for cluster,genes in cluster_to_genes.iteritems() if len(genes) >= min_cluster_size)

	return gene_to_clusters, cluster_to_genes

def compare_clusters(gene_to_clusters_ref, cluster_to_genes_query):
	clusters_query_to_clusters_ref = dict()

	for cluster_query in cluster_to_genes_query.iterkeys():
		clusters_query_to_clusters_ref[cluster_query] = defaultdict(int)
		for gene_query in cluster_to_genes_query[cluster_query]:
			if gene_query in gene_to_clusters_ref :
				for cluster_ref in gene_to_clusters_ref[gene_query]:
					clusters_query_to_clusters_ref[cluster_query][cluster_ref] += 1
			else:
				clusters_query_to_clusters_ref[cluster_query][None] += 1

	return clusters_query_to_clusters_ref

def write_results(clusters_query_to_clusters_ref, clusters_size_ref, clusters_size_query, output_file):
	with open(output_file, 'w') as ostream:
		for cluster_query, cluster_query_to_clusters_ref in sorted(clusters_query_to_clusters_ref.items(),
				key=lambda (cluster_query,_): clusters_size_query[cluster_query], reverse=True):
			print("{0} ({1} genes):".format(cluster_query, clusters_size_query[cluster_query]), file=ostream)
			for cluster_ref in sorted(cluster_query_to_clusters_ref.keys(),
					key = lambda cluster_ref: cluster_query_to_clusters_ref[cluster_ref], reverse=True):
				if cluster_ref:
					print("\t{0} ({1} genes)\t{2}".format(cluster_ref, clusters_size_ref[cluster_ref], cluster_query_to_clusters_ref[cluster_ref]), file=ostream)
				else:
					print("\tunknown\t{0}".format(cluster_query_to_clusters_ref[cluster_ref]), file=ostream)
			print("", file=ostream)
def main():
	parameters = get_parameters()
	print('STEP 1/4: Indexing reference...')
	gene_to_clusters_ref, cluster_to_genes_ref = index_clusters(parameters.reference_file)
	print('STEP 2/4: Indexing query...')
	gene_to_clusters_query, cluster_to_genes_query = index_clusters(parameters.query_file, parameters.query_min_cluster_size)
	print('STEP 3/4: Comparing the query to the reference...')
	clusters_query_to_clusters_ref = compare_clusters(gene_to_clusters_ref, cluster_to_genes_query)

	clusters_size_ref = dict((cluster, len(cluster_genes)) for (cluster, cluster_genes) in cluster_to_genes_ref.iteritems())
	clusters_size_query = dict((cluster, len(cluster_genes)) for (cluster, cluster_genes) in cluster_to_genes_query.iteritems())
	print('STEP 4/4: Writing results...')
	write_results(clusters_query_to_clusters_ref, clusters_size_ref, clusters_size_query, parameters.output_file)

if __name__ == '__main__':
	main()

