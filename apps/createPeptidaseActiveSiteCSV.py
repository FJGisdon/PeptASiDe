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
                                        requestVariablesUniProt, \
                                        extractActiveSites

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


def createActiveSiteCSV(ECcode):
    """
    Create a CSV file which contains peptidases and their active sites.
    Search for peptidases with active site residues in MEROPS/UniProt/...

    param: str ECcode
    """
    cl.log(f"Performing PDB search for EC code {ECcode}.", "i")
    searchResults: list = searchPDB(queryVariablesPDB.serinePeptidasesEntities)
    cl.log("{} PDB entities found with the EC code {}:\n{}".format(len(searchResults), ECcode, ", ".join(searchResults)), "i")

    cl.log("Assign catalytic residues to structure using UniProt.", "i") 
    uniProtIDs: list = requestDataPDB(requestVariablesPDB.uniProtIDs(entity_ids=searchResults))
    cl.log(f"UniProt IDs for all entities:\n{uniProtIDs}", "d")
    uniProtActiveSites: list = extractActiveSites(requestVariablesUniProt.getActiveSiteResidues(uniProt_ids=[uniProtIDs[item][1] for item in range(len(uniProtIDs))])) 
    
    outputDict = dict()
    for entry in uniProtIDs:
        for result in uniProtActiveSites:
            if entry[1] == result[0]:
                outputDict[entry[0].split('_')[0]] = [str(entry[0]), \
                                                    str(entry[1]), \
                                                    result[1], \
                                                    result[2],\
                                                    ]
    # Check the data, shouldn't some of the entries appear more than once for different active site residues?
    # The dictionary contains entries more than once. For each active site residue, which was found one entry is generated. This makes processing later easier.
    return outputDict

# ---------------------------------------------------------------------------
# Program
# ---------------------------------------------------------------------------
if __name__ == "__main__":   
    # Parse settings and input arguments and eventually customize the logger
    args = initializePeptaside()
    # Start the application
    resultDict: dict = {}
    # TODO: make it universal to use with user-specific EC number
    resultDict = createActiveSiteCSV("3.4.21")
    # Save the dictionary as CSV
    header = ['PDB-ID', 'PDB entity', 'UniProtID', 'Residue number', 'Identity']
    cl.logCSV(args.outputCSV.name, resultDict, header)
# ---------------------------------------------------------------------------
