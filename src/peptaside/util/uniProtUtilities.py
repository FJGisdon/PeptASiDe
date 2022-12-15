#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Created By    : FJG
# Creation Date : 15/12/2022
version ='1.0.0'
# ---------------------------------------------------------------------------
"""
Utility to search and process UniProt data.
"""
# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------
import json
import requests
from dataclasses import dataclass
from ..io.loggingSetup import customLogger

# ---------------------------------------------------------------------------
# Logger
# ---------------------------------------------------------------------------
# Local logger instance for this module
cl = customLogger(__name__)

# ---------------------------------------------------------------------------
# Classes
# ---------------------------------------------------------------------------

@dataclass
class requestVariablesUniProt:
    """
    TODO
    """
    @staticmethod
    def getActiveSiteResidues(uniProt_ids: list):
        """  """
        cl.log(uniProt_ids, "d")
        # A list of UniProt IDs is required.
        return uniProt_ids


# ---------------------------------------------------------------------------
# Functions
# ---------------------------------------------------------------------------

def requestDataUniProt(query):
    """
    TODO
    """
    cl.log("Performing query", "i")
    results = []
    for item in query:
        cl.log(f'https://rest.uniprot.org/uniprotkb/search?format=json&fields=accession%2Cid%2Cft_act_site&query=%28{item}%29' ,"d")
        result = requests.get(f'https://rest.uniprot.org/uniprotkb/search?format=json&fields=accession%2Cid%2Cft_act_site&query=%28{item}%29')
        if result.status_code == 200:
            response = result.json()
        else: cl.log(f"No data obtained from UniProt, status code: {result.status_code} ", "w")
        results.append(response)
        # results:0:primaryAccession/uniProtkbId/features:0/1/2:type-Active site/location:start:value-220/modifier-EXACT
    cl.log(results, "i")

    return results

