#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Created By    : FJG
# Creation Date : 19/11/2022
version ='1.0.0'
# ---------------------------------------------------------------------------
"""
Application to prepare a list of peptidases from the PDB with their
corresponding active sites.
"""
# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------
import argparse
import sys
import os

sys.path.append('../src/')

from peptaside.io.loggingSetup import customLogger

# ---------------------------------------------------------------------------
# Functions
# ---------------------------------------------------------------------------

def createPeptidaseActiveSiteCSV():
    """  """
    # Read the settings and arguments
    #args = create_parser()

    # create the logger
    cl = customLogger(__name__)
    # TODO
    # Set up the logger for every new module, which is used to always update the name, which is printed in the end. Could this be done with a borg class? Is that something that implements a class and every new instance has the same information? Is the logger then changed for all of them?
    cl.set_up_logger()
	
    #check_file_writable(args.output)
	
    cl.log("Program started", "i")
    cl.log("This is the first output!!")
    cl.log("This is an ERROR test...", "e")
    cl.log("Program finished", "i")
	

    

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



	

# ---------------------------------------------------------------------------
# Program
# ---------------------------------------------------------------------------
if __name__ == "__main__":    
    createPeptidaseActiveSiteCSV()
