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

	parser.add_argument('--genes-catalog', dest='genes_catalog', type=is_file, required=True, default=argparse.SUPPRESS,
			help='Multi-FASTA file which contains all the genes.')

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

def parse_fasta(istream):
	header, seq = None, []
	for line in istream:
		line = line.rstrip()
		if line.startswith(">"):
			if header: yield (header, ''.join(seq))
			header, seq = line, []
		else:
			seq.append(line)
	if header: yield (header, ''.join(seq))


def extract_clusters_genes(genes_catalog, gene_to_clusters):
	""" Read the genes catalog and dispatch each gene profile to its clusters.
	"""

	clusters_genes = dict()
	with open(genes_catalog, 'r') as istream:
		for i, fasta_entry in enumerate(parse_fasta(istream),start=1):
			if i in gene_to_clusters:
				for cluster_name in gene_to_clusters[i]:
					if cluster_name in clusters_genes:
						clusters_genes[cluster_name].append(fasta_entry)
					else:
						clusters_genes[cluster_name] = [fasta_entry]

	return clusters_genes


def write_clusters_genes(output_dir, clusters_genes, min_cluster_size):
	for cluster_name in clusters_genes:

		if len(clusters_genes[cluster_name]) < min_cluster_size :
			continue

		output_file = os.path.join(output_dir, cluster_name + '.fna')

		with open(output_file, 'w') as ostream:
			for header,seq in clusters_genes[cluster_name]:
				print("{0}\n{1}".format(header,seq), file=ostream)

def main():
	parameters = get_parameters()
	print('STEP 1/3: Reading clusters file...')
	gene_to_clusters = parse_clusters(parameters.clusters_file)
	print('STEP 2/3: Extracting clusters genes from genes catalog...')
	clusters_genes = extract_clusters_genes(parameters.genes_catalog, gene_to_clusters)
	print('STEP 3/3: Writing clusters genes...')
	write_clusters_genes(parameters.output_dir, clusters_genes, parameters.min_cluster_size)

if __name__ == '__main__':
	main()

