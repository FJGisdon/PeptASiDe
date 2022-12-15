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

        self.__class__._args = self._parseBaseArguments().parse_args()



    @classmethod
    @property
    def args(cls):
        """ TODO """
        return cls._args
  

    def _parseBaseArguments(self):
        """ TODO """
        ## create the parser
        parseInput = argparse.ArgumentParser(add_help=False, fromfile_prefix_chars="@")

        # add mutually exclusive group for silent / verbose
        verbosity = parseInput.add_mutually_exclusive_group()
        verbosity.add_argument('-s',
                                '--silent',
                                action='store_const',
                                dest='verbosity',
                                const='silent',
                                help='only print errors to stdout, results to output')

        verbosity.add_argument('-a',
                                '--alerting',
                                action='store_const',
                                dest='verbosity',
                                const='alerting',
                                help='print up to warnings to stdout, results to output')

        verbosity.add_argument('-v',
                                '--verbose',
                                action='store_const',
                                dest='verbosity',
                                const='verbose',
                                help='print additional information to stdout, results to output')

        verbosity.add_argument('-d',
                                '--debug',
                                action='store_const',
                                dest='verbosity',
                                const='debut',
                                help='print every information to stdout, results to output')

        # add command line arguments
        parseInput.add_argument('--version',
                                action='version',
                                version='%(prog)s ' + version)

        parseInput.add_argument('-o',
                                '--outputfile',
                                metavar = 'path',
                                dest = 'outputLog',
                                type = argparse.FileType('w'),
                                default = sys.stdout,
                                help = 'results file')

        return parseInput


    @property
    def outputLog(self):
        """ TODO """
        return self.__class__._args.outputLog




class inputParser(baseParser):
    """
    A class to parse the input and prepare the output .

    Attributes
    ----------
    args : ;

    Methods
    -------
    createParser():
            Description.
    """


    def __init__(self):
        """
        TODO
        !!! Make it more general, that every application can add the respective command line arguments.
        !!! Here should be a method to generate additional arguments
        """
        self.__class__._args = self._parseAdditionalArguments().parse_args()


    # Should there also be a function to add arguments from within the main application? - Yes
    def _parseAdditionalArguments(self):
        """ TODO """

        ## create the parser
        parseInput = argparse.ArgumentParser(parents=[self._parseBaseArguments()],\
                                                        fromfile_prefix_chars="@")

        ## add arguments
    
        # positional arguments
        #parseInput.add_argument('protein_structure',
        #                        metavar = '<path to PDB/mmCIF>',
        #                        help = 'name of the PDB or mmCIF structure')
    
        #parseInput.add_argument('graph_file_path',
        #                        metavar = '<path to graph file (GML)>',
        #                        help = 'read the graph file (only GML input tested so far)')
    
        #parseInput.add_argument('graph_partition',
        #                        metavar = '<graph partitioning information>',
        #                        help = 'read the partitioning information from graph clustering (vector with cluster number for nodes)\
        #                                    (If iGraph is used for cluster membership calculations \'community-detection-object.membership\' can be used)')
    
        # add command line arguments
    
        #parseInput.add_argument('-w',
        #                        '--weighttype',
        #                        metavar = 'edge weight type',
        #                        default = "absoluteWeight",
        #                        help = 'the edge weight type to use')

        parseInput.add_argument('-t',
                                '--csvtable',
                                metavar = 'path',
                                dest = 'outputCSV',
                                type = argparse.FileType('w'),
                                default = sys.stdout,
                                help = 'csv file to store the peptidases and active sites')
    
        return parseInput
    
# ---------------------------------------------------------------------------
