#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Created By    : FJG
# Creation Date : 19/11/2022
version ='1.0.0'
# ---------------------------------------------------------------------------
"""
Application to prepare a list of peptidase entities from the PDB with their
corresponding active sites nucleophiles and write them to a CSV file.
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
from peptaside.util.uniProtUtilities import requestDataUniProt, \
                                        requestVariablesUniProt

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
    # TODO make the parser more general!!!
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
    cl.log("{} PDB entities found for serine peptidases with the EC code 3.4.21:\n{}".format(len(serinePeptidaseSearchResults), ", ".join(serinePeptidaseSearchResults)), "i")

    cl.log("Assign catalytic serine to structure using UniProt.", "i") 
    uniProtIDs: list = requestDataPDB(requestVariablesPDB.uniProtIDs(entity_ids=serinePeptidaseSearchResults))
    cl.log(f"UniProt IDs for serine peptidase entities:\n{uniProtIDs}", "d")
    cl.log("Obtain the active site serine via UniProt and combine with previous information and write to CSV", "d")
    requestDataUniProt(requestVariablesUniProt.getActiveSiteResidues(uniProt_ids=[uniProtIDs[item][1] for item in range(len(uniProtIDs))])) 


# ---------------------------------------------------------------------------
# Program
# ---------------------------------------------------------------------------
if __name__ == "__main__":   
    # Parse settings and input arguments and eventually customize the logger
    args = initializePeptaside()
    # Start the application
    createPeptidaseActiveSiteCSV()

# ---------------------------------------------------------------------------
