#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Created By    : FJG
# Creation Date : 07/12/2022
version ='1.0.0'
# ---------------------------------------------------------------------------
"""
Base class to parse the standard input. Child class to extend the input
options.
Possible TODO: provide customization method to add user-defined arguments.
"""
# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------
import argparse
import sys
import os

from .loggingSetup import customLogger

# ---------------------------------------------------------------------------
# Logger
# ---------------------------------------------------------------------------
# Local logger instance for this module
cl = customLogger(__name__)

# ---------------------------------------------------------------------------
# Classes
# ---------------------------------------------------------------------------

class baseParser(object):
    """
    A base class for the input parser.

    Attributes
    ----------
    args : Namespace, description;

    Methods
    -------
    createParser():
            Description.
    checkFileWritable():
            Description.
    createPathAndFile():
            Description.
    """

    _args = dict()

    def __init__(self):
        """
        TODO
        """

        self.__class__._args = self._parseArguments()



    @classmethod
    @property
    def args(cls):
        """ TODO """
        return cls._args
  

    def _parseArguments(self):
        """ TODO """
        ## create the parser
        parseInput = argparse.ArgumentParser(description="Parse user arguments and settings.",
                                                fromfile_prefix_chars="@")

        # add mutually exclusive group for silent / verbose
        verbosity = parseInput.add_mutually_exclusive_group()
        verbosity.add_argument('-s',
                                '--silent',
                                action='store_true',
                                help='only print results to stdout, e.g., no status messages and meta information')

        verbosity.add_argument('-a',
                                '--allerting',
                                action='store_true',
                                help='print more to stdout, e.g., status messages and meta information')

        verbosity.add_argument('-v',
                                '--verbose',
                                action='store_true',
                                help='print more to stdout, e.g., status messages and meta information')

        verbosity.add_argument('-d',
                                '--debug',
                                action='store_true',
                                help='print everything including debug information')

        # add command line arguments
        parseInput.add_argument('--version',
                                action='version',
                                version='%(prog)s ' + version)

        parseInput.add_argument('-o',
                                '--outputfile',
                                metavar = 'path',
                                dest = 'output',
                                type = argparse.FileType('w'),
                                default = sys.stdout,
                                help = 'PML file for PyMOL to file')

        return parseInput.parse_args()


    def checkFileWritable(self, fp):
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


    def createPathAndFile(self):
        pass




class inputParser(baseParser):
    """
    A class to parse the input and prepare the output file if specified.

    Attributes
    ----------
    args : ;

    Methods
    -------
    createParser():
            Description.
    checkFileWritable():
            Description.
    createPathAndFile():
            Description.
    """


    def __init__(self):
        """
        TODO
        """
        super().__init__()
        cl.log("Another test message from parser child.", "e")

    # Should there also be a function to add arguments from within the main application? - Yes
    # Should there be all arguments accessible from this child class?
    def _parseArguments(self):
        """ TODO """
        super()._parseArguments()
        ## add arguments
    
        # positional arguments
        parseInput.add_argument('protein_structure',
                                metavar = '<path to PDB/mmCIF>',
                                help = 'name of the PDB or mmCIF structure')
    
        #parseInput.add_argument('graph_file_path',
        #                        metavar = '<path to graph file (GML)>',
        #                        help = 'read the graph file (only GML input tested so far)')
    
        #parseInput.add_argument('graph_partition',
        #                        metavar = '<graph partitioning information>',
        #                        help = 'read the partitioning information from graph clustering (vector with cluster number for nodes)\
        #                                    (If iGraph is used for cluster membership calculations \'community-detection-object.membership\' can be used)')
    
        # add command line arguments
    
        parseInput.add_argument('-w',
                                '--weighttype',
                                metavar = 'edge weight type',
                                default = "absoluteWeight",
                                help = 'the edge weight type to use')
    
        return parseInput.parse_args()
    
# ---------------------------------------------------------------------------
