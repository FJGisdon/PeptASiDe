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
# First create the default logger, later parse the input and then set up the logger
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

    # Set up the logger
    cl.setUpLogger(loglevel = 'verbose')


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

# ---------------------------------------------------------------------------
