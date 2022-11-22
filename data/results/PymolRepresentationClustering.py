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
	
	def __init__(self, graph_file_input: str, cluster_membership: [int], edge_weight_type: str = "absoluteWeight"):
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
		
		self.prepareDictionary()
		
		
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
						elif line.split()[0] == f"{self.edge_weight_type}":
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
        


########### vamos ###########

def preparePML(ClusterDictionary, input_structure):

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

	print(filePML)
	
def prepareClusteringRepresentationPyMOL(protein_structure, graph_file_path, graph_partition):
	# prepare dictionary with PTGL complex graph and partitioning information
	ClusterDictionary = PTGLComplexGraphClusterDictionary(graph_file_path, graph_partition)
	preparePML(ClusterDictionary.cluster_dictionary, protein_structure)
	

	
	
	

