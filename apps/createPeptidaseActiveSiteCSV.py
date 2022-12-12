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

#import peptaside.io.settings
from peptaside.io.loggingSetup import customLogger
from peptaside.io.inputParser import inputParser

# ---------------------------------------------------------------------------
# Logger
# ---------------------------------------------------------------------------
# Local logger instance
cl = customLogger(__name__)

# ---------------------------------------------------------------------------
# Functions
# ---------------------------------------------------------------------------

def initializePeptaside():
    """
    Initialize.
    """

    # Parse and process the settings and input arguments
    parser = inputParser()
    # Set up the logger to verbose for development
    cl.setUpLogger(loglevel = 'verbose')

    return parser.args



def createPeptidaseActiveSiteCSV():
    """
    Create a CSV file which contains peptidases and their active sites.
    TODO: Later this should be a database with additional residues for
            potential active sites.
    """

    cl.log(f"These are the args in main: {vars(args)}")
    cl.log("Program finished", "i")
	
    
# ---------------------------------------------------------------------------
# Program
# ---------------------------------------------------------------------------
if __name__ == "__main__":   
    # Parse settings and input arguments and eventually customize the logger
    args = initializePeptaside()
    # Start the application
    createPeptidaseActiveSiteCSV()

# ---------------------------------------------------------------------------
