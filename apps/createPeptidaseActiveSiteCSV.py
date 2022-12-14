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
from peptaside.io.inputParser import inputParser
from peptaside.util.PDButilities import queryVariablesPDB, \
                                        searchPDB, \
                                        requestVariablesPDB, \
                                        requestDataPDB

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
    # Set up the user-defined loglevel and output
    cl.setUpLogger(usrOutput = parser.args.outputLog, loglevel = parser.args.verbosity)
    
    return parser.args


def createPeptidaseActiveSiteCSV():
    """
    Create a CSV file which contains peptidases and their active sites.
    Search for peptidases with active site residues in MEROPS/UniProt/...
    Only take those, whith complete information and obtain structural
    information from PDB.
    Information can be found in UniProt json download
    'Active site' or 'Binding site'
    - search maybe UniProt to find active site residues
    - fill csv with relevant information
    TODO: Later this should be a database with additional residues for
            potential active sites.

    :param: peptidaseStructures: list, description...;
    """

    cl.log("Performing PDB search for serine peptidases with the EC code 3.4.21.", "i")
    serinePeptidaseSearchResults: list = searchPDB(queryVariablesPDB.serinePeptidasesEntities)

    cl.log("PDB search results for serine peptidases with the EC code 3.4.21:\n{}".format(", ".join(serinePeptidaseSearchResults)))
    cl.log(f"{len(serinePeptidaseSearchResults)} results for the PDB search:\n{serinePeptidaseSearchResults}", "i")
    cl.log(f"Results written to {args.outputLog}", "i")

    cl.log("Assign catalytic serine to structure.", "i") 
    uniProtIDs: list = requestDataPDB(requestVariablesPDB.test)
    cl.log("UniProt IDs for serine peptidase entities:\n{}".format(", ".join(uniProtIDs)))


# ---------------------------------------------------------------------------
# Program
# ---------------------------------------------------------------------------
if __name__ == "__main__":   
    # Parse settings and input arguments and eventually customize the logger
    args = initializePeptaside()
    # Start the application
    createPeptidaseActiveSiteCSV()

# ---------------------------------------------------------------------------
