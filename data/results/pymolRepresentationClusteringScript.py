#################################################
"""
- logging
    - use the function 'log' for each and every print!
        -> d(ebug) for debug messages
        -> i(nfo) for status and meta information
        -> w(arning), e(rror), c(ritical) for more severe messages
        -> without a level to print results and if required obligatory non-result prints
            -> command line option 'silent' should suppress those obligatory prints so that only results are printed
- pipelining
    - write the results with -o to an output file to use as next input or
    - use 'silent' mode (if obligatory prints exist) and pipe the output of stdout directly to next script
        -> all debug, info, warning etc. are printed to stderr
    - it is possibly to pipe input to this script via stdin
"""
########### information ###########

# Python template taken from Jan Niclas Wolf


########### settings ###########

version = "1.0.0"


########### built-in imports ###########

import sys
import os
import argparse
import logging
import traceback


########### functions ###########


def check_file_writable(fp):
    """Checks if the given filepath is writable"""
    if os.path.exists(fp):
        if os.path.isfile(fp):
            return os.access(fp, os.W_OK)
        else:
            return False
    # target does not exist, check perms on parent dir
    parent_dir = os.path.dirname(fp)
    if not parent_dir: parent_dir = '.'
    return os.access(parent_dir, os.W_OK)


def log(message, level=""):
    """Prints the message according to level of severity and output settings"""
    if (level == "c"):
        logger.critical(message)
    if (level == "e"):
        logger.error(message)
    elif (level == "w"):
        logger.warning(message)
    elif (level == "i"):
        logger.info(message)
    elif (level == "d"):
        logger.debug(message)
    else:
        args.output.write(message + "\n")


########### simple classes ###########

class PTGLComplexGraphClusterDictionary:
	"""
	A class to prepare a dictionary, which holds the information about a PTGL complex graph and the corresponding clustering.
	Structure:
		key -> numbers of the nodes (here nodes represent chains of the structure):
		[chain ID: str, cluster membership: int, [chain ID contacts (edges): str], [edge weights corresponding to edges: str]]

	Attributes
	----------
	cluster_dictionary : dict, dictionary containing the PTGL graph information and the corresponding clustering

	Methods
	-------
	prepareDictionary():
		Parses the graph file input and the graph partitioning and prepares a dictionary for further usage.
	"""
	
	def __init__(self, input_structure: str, graph_file_input: str, cluster_membership: [int], edge_weight_type: str = "absoluteWeight"):
		"""
		
		Initialization of PTGLComplexGraphClusterDictionary
		
		:param input_structure: str, the coordinate file of the structure (mmCIF or PDB)
		:param graph_file_input: str, the graph input file (only GML input supported)
		:param cluster_membership: [int], vector, which assigns the number of the community to a chain. 
                                        It is sorted in the order of the chains.
                                        (If iGraph is used for cluster membership calculations 
                                        'community-detection-object.membership' can be used)
		:param edge_weight_type: str, the edge weight, which should be read
			default: "absoluteWeight"
		
		"""
		
		self.cluster_dictionary: dict[str: str,int,[str],[str]] = {}
		self.graph_file: str = graph_file_input
		self.cluster_membership: [int] = cluster_membership
		self.edge_weight_type: str = edge_weight_type
		
		
	def prepareDictionary(self):
		"""
		
		Prepares a dictionary, which stores PTGL complex graph information and the corresponding partitioning.
		
		"""
		
		hit_node: bool = False
		hit_edge: bool = False
		in_block: bool = False
		node_id: int
		label: str
		edge_source: str 
		edge_target: str
		edge_weight: str
		add_to_dictionary = True
		
		with open(self.graph_file) as f:
			for line in f.read().split("\n"):
				if not in_block:
					# in graph header
					if "node [" in line:
						hit_node = True
						in_block = True
					elif "edge [" in line:
						hit_edge = True
						in_block = True
						# once all the nodes are read, we go through the edges and have to add two lists to the dictionary first
						if add_to_dictionary:
							for item in self.cluster_dictionary:
								self.cluster_dictionary[item].append([])
								self.cluster_dictionary[item].append([])
							add_to_dictionary = False
					else:
						pass
				else:
					# first go through all nodes
					if hit_node:
						if line.split()[0] == "id":
							node_id = str(line.split()[-1])
						elif line.split()[0] == "label":
							label = str(line.split()[-1])[1:-1]
						elif line.split()[0] == "]":
							in_block = False
							hit_node = False
							self.cluster_dictionary[node_id] = [label, self.cluster_membership[int(node_id)]]
							pass
						else: pass

					# then go through all edges            
					elif hit_edge:
						if line.split()[0] == "source":
							edge_source = str(line.split()[-1])
						elif line.split()[0] == "target":
							edge_target = str(line.split()[-1])
						elif line.split()[0] == f({self.edge_weight_type}):
							edge_weight = str(line.split()[-1])
						elif line.split()[0] == "]":
							in_block = False
							hite_edge = False
							self.cluster_dictionary[edge_source][2].append(self.cluster_dictionary[edge_target][0])
							self.cluster_dictionary[edge_source][3].append(edge_weight)
							self.cluster_dictionary[edge_target][2].append(self.cluster_dictionary[edge_source][0])
							self.cluster_dictionary[edge_target][3].append(edge_weight)
							pass
						else: pass

					else:
				    		pass

########### configure logger ###########


logger = logging.getLogger('pymolRepresentationClustering.py')
logging.basicConfig(format = "[%(levelname)s] %(message)s")          

            
########### command line parser ###########
def create_parser():
	## create the parser
	cl_parser = argparse.ArgumentParser(description="Prepares a .pml-input script for PyMOL, which shows the detected communities \
	    						with connections and edge weights from a graph analysis in the real protein structure.",
		                            fromfile_prefix_chars="@")

	## add arguments

	# positional arguments
	cl_parser.add_argument('protein_structure',
		               metavar = '<path to PDB/mmCIF>',
		               help = 'name of the PDB or mmCIF structure')

	cl_parser.add_argument('graph_file_path',
		               metavar = '<path to graph file (GML)>',
		               help = 'read the graph file (only GML input tested so far)')          

	cl_parser.add_argument('graph_partition',
		               metavar = '<graph partitioning information>',
		               help = 'read the partitioning information from graph clustering (vector with cluster number for nodes)\
		               		(If iGraph is used for cluster membership calculations \'community-detection-object.membership\' can be used)')

	# add mutually exclusive group for silent / verbose
	loudness = cl_parser.add_mutually_exclusive_group()
	loudness.add_argument('-s',
		               '--silent',
		               action='store_true',
		               help='only print results to stdout, e.g., no status messages and meta information')

	loudness.add_argument('-v',
		               '--verbose',
		               action='store_true',
		               help='print more to stdout, e.g., status messages and meta information')

	loudness.add_argument('-d',
		              '--debug',
		              action='store_true',
		              help='print everything including debug information')

	# add command line arguments
	cl_parser.add_argument('--version',
		               action='version',
		               version='%(prog)s ' + version)

	cl_parser.add_argument('-o',
		               '--outputfile',
		               metavar = 'path',
		               dest = 'output',
		               type = argparse.FileType('w'),
		               default = sys.stdout,
		               help = 'PML file for PyMOL to file')

	cl_parser.add_argument('-w',
		               '--weighttype',
		               metavar = 'edge weight type',
		               default = "absoluteWeight",
		               help = 'the edge weight type to use')

	return cl_parser.parse_args()


########### check arguments ###########

# assign log level
log_level = logging.WARNING
#if (args.debug):
#	log_level = logging.DEBUG
#elif (args.verbose):
#	log_level = logging.INFO
logger.setLevel(log_level)


########### vamos ###########

def preparePML(ClusterDictionary):
	log("Version " + version, "i")

	# prepare variables for the PML script
	number_of_clusters: int = 0
	clustered_chains: dict = dict()    
	pseudoatoms: str = ""
	group_distances: str = ""
	distance_calculations: str = ""
	pseudoatoms_for_label: str = ""
	close_contact_groups: str = ""

	for key, nested in ClusterDictionary.items():
		if nested[1] > number_of_clusters:
			number_of_clusters = nested[1]
		if str(nested[1]) in clustered_chains:
			clustered_chains[str(nested[1])].append(nested[0])
	else:
		clustered_chains[str(nested[1])] = [nested[0]]

	pseudoatoms += f"pseudoatom ps{nested[0]}, chain {nested[0]}\n"

	for position, item in enumerate(nested[2]):
		distance_calculations += f"dist dist_{nested[0]}-{item}, ps{nested[0]}////PS1, ps{item}////PS1\nhide label, dist_{nested[0]}-{item}\n"
		pseudoatoms_for_label += f"pseudoatom ps_{nested[0]}-{item}, ps{nested[0]} or ps{item}, label={nested[3][position]}\n"

	group_distances += f"group chain-{nested[0]}_contacts, dist_{nested[0]}-*\n"
	close_contact_groups += f"group chain-{nested[0]}_contacts, close\n"

	# Prepare coloring of chains according to cluster membership
	# First get number of clusters
	# Colors of the clusters according to iGraph coloring output
	color_list = ["red", "carbon", "blue", "yellow", "lightmagenta", "cyan", "grey", "ruby", "forest", "density", "sulfur", "deeppurple", "deepteal"] 

	filePML: str
	select_clusters: str = ""
	color_cluster: str = ""

	for cluster in range(number_of_clusters+1):
		select_clusters += "select cluster{}, chain {}\n".format(cluster, "".join(str("+" + e) for e in clustered_chains[str(cluster)])[1:])
		color_cluster += f"color {color_list[cluster]}, cluster{cluster}\n"

	# Prepare the PML script for PyMol
	filePML = f"""
	### PML file to represent the clusters in the structure.
	# Python is by default case insensitive for chain IDs but for large clusters with upper and lower case letters we have to care!
	set ignore_case, off

	# Load the structure
	load f{input_structure}, complex

	# Select and color the found clusters
	{select_clusters}
	{color_cluster}
	# Create pseudoatoms at the geometric center of the chains
	{pseudoatoms}
	group pseudoatoms, ps*

	# Create all distance objects originating from each chain (reverse dublicates are needed!)
	# Hide the distance label, generate a pseudoatom between both pseudoatoms for which the distance was calculated
	# and label it according to the edge weight
	{distance_calculations}
	# Group all distance measurements originating from one chain to all other connected ones
	{group_distances}
	# Disallow addition/removal from the group (allow with 'open')
	{close_contact_groups}
	# Set pseudoatoms along the distance measurement line and label them with the corresponding edge weights
	{pseudoatoms_for_label}
	group label_pseudoatoms, ps_*

	# Set some parameters
	set dash_gap, 0.7
	set dash_radius, 0.2
	set dash_color, black
	set label_position,(1,1,1) # label offset
	set label_color, black
	bg_color white
	set cartoon_highlight_color, grey40

	"""

	log(filePML)
	
def prepareClusteringRepresentationPyMOL():
	""" Helper function for import in scripts """
	# prepare dictionary with PTGL complex graph and partitioning information
	ClusterDictionary = PTGLComplexGraphClusterDictionary(protein_structure, graph_file_path, graph_partition)
	preparePML(ClusterDictionary)
	
	
if __name__ == "__main__":
	args = create_parser()
	print(args)
	# prepare dictionary with PTGL complex graph and partitioning information
	ClusterDictionary = PTGLComplexGraphClusterDictionary(args.protein_structure, args.graph_file_path, args.graph_partition)
	preparePML(ClusterDictionary)
else:
	pass
	
	
	
	

