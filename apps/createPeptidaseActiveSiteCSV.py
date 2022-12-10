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

import peptaside.io.settings
from peptaside.io.loggingSetup import customLogger
from peptaside.io.inputParser import inputParser

# ---------------------------------------------------------------------------
# Functions
# ---------------------------------------------------------------------------
#TODO Make initialize a class so that it is called by the user and 
# everything is set up and include the parser
def initializePeptaside():
    """
    Initialize.
    """

    # First create the logger then parse the input and then set up the logger
    CL = customLogger(__name__)

    # Parse and process the settings and input arguments
    parser = inputParser()

    # Set up the logger
    CL.setUpLogger()

    # Test of log level adjustment
    CL.setLogLevel("verbose")

    CL.log("Program started", "i")
    CL.log("This is the first output!!")
    CL.log("This is an ERROR test...", "e")

    # Test of name print for different module log
    parser2 = inputParser()


def createPeptidaseActiveSiteCSV():
    """
    Create a CSV file which contains peptidases and their active sites.
    TODO: Later this should be a database with additional residues for
            potential active sites.
    """

    CL.log("These are the results...")
    CL.log("Program finished", "i")
	
    
# ---------------------------------------------------------------------------
# Program
# ---------------------------------------------------------------------------
if __name__ == "__main__":    
    initializePeptaside()
    #createPeptidaseActiveSiteCSV()
