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
import sys
sys.path.append('../src/')

from peptaside.io.loggingSetup import customLogger
from peptaside.util.prepareOutputFile import check_file_writable

# ---------------------------------------------------------------------------
# Functions
# ---------------------------------------------------------------------------

def initializePeptaside():
    """
    Initialize.
    """
    
    # Parse and process the settings and input arguments
    # args = create_parser()
    # check_file_writable(args.output)

    # Create the logger
    cl = customLogger(__name__)
    # Set up the logger
    cl.set_up_logger()
    # TODO
    # Set up the logger for every new module, which is used to always update the name, which is printed in the end. Could this be done with a borg class? Is that something that implements a class and every new instance has the same information? Is the logger then changed for all of them?
    cl.log("Program started", "i")
    cl.log("This is the first output!!")
    cl.log("This is an ERROR test...", "e")


def createPeptidaseActiveSiteCSV():
    """
    Create a CSV file which contains peptidases and their active sites.
    TODO: Later this should be a database with additional residues for
            potential active sites.
    """

    cl.log("These are the results...")
    cl.log("Program finished", "i")
	
    
# ---------------------------------------------------------------------------
# Program
# ---------------------------------------------------------------------------
if __name__ == "__main__":    
    initializePeptaside()
    #createPeptidaseActiveSiteCSV()
