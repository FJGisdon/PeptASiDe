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
    cl.log("Obtain the active site (should be 1-3 residues, for now we just need the active site serine) and the sequence (to check the active site residues) via UniProt and combine with previous information and write to CSV", "d")
    uniProtActiveSites: list = requestDataUniProt(requestVariablesUniProt.getActiveSiteResidues(uniProt_ids=[uniProtIDs[item][1] for item in range(len(uniProtIDs))])) 
    
    outputDict = dict()
    count_normal = 0
    count_plus = 0
    count_else = 0
    count_total = 0
    for item1 in uniProtActiveSites:
        for item2 in uniProtIDs:
            if item1[0] == item2[1]:
                count_total+=1
                #outputDict.update({item2[0], item1[0], item1[2]})
                cl.log(item2[0] , "d") # PDB entity
                cl.log(item1[0] , "d") # UniProt accession
                cl.log(item1[1] , "d") # active site information
                cl.log(item1[2] , "d") # sequence
                cl.log(f'{item2[0]}: {[item1[0], item1[1]]}', "i")
                for number in item1[1]:
                    if item1[2][number] == 'S':
                        cl.log(f'{number}, {item1[2][number]}', "i")
                        count_normal+=1
                    elif item1[2][number+1] == 'S':
                        cl.log(f'+1 - {number+1}, {item1[2][number+1]}', "i")
                        count_plus+=1
                    else:
                        count_else+=1
    cl.log(f'Counts for serine in listed position: {count_normal}, in position +1: {count_plus}, else: {count_else}', "i")
    cl.log(f'Total entities: {count_total}', "i")
    # TODO Finding the positions of the active site serine, this does not match for a lot of
    #       structures, even if I consider the initial methionine is not counted
    #print(outputDict)

    header = ['PDB entity', 'UniProtID', 'Active site', 'Sequence']
    cl.logCSV(args.outputCSV.name, outputDict, header) 

    # TODO
    # - Before running PTGL check, which residue is the nucleophile

# ---------------------------------------------------------------------------
# Program
# ---------------------------------------------------------------------------
if __name__ == "__main__":   
    # Parse settings and input arguments and eventually customize the logger
    args = initializePeptaside()
    # Start the application
    createPeptidaseActiveSiteCSV()

# ---------------------------------------------------------------------------
