#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Created By    : FJG
# Creation Date : 13/12/2022
version ='1.0.0'
# ---------------------------------------------------------------------------
"""
Utility to search and process PDB.
"""
# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------
import json
import requests
from ..io.loggingSetup import customLogger

# ---------------------------------------------------------------------------
# Logger
# ---------------------------------------------------------------------------
# Local logger instance for this module
cl = customLogger(__name__)

# ---------------------------------------------------------------------------
# Functions
# ---------------------------------------------------------------------------

def searchXray():
    """ 
    TODO 
    Test: This query finds PDB structures of virus's thymidine kinase with 
    substrate/inhibitors, determined by X-ray crystallography at a resolution 
    better than 2.5 A.
    """
    searchUrlEndpoint: str = 'https://search.rcsb.org/rcsbsearch/v2/query'

    jsonQuery = {
  "query": {
    "type": "group",
    "logical_operator": "and",
    "nodes": [
      {
        "type": "terminal",
        "service": "full_text",
        "parameters": {
          "value": "\"thymidine kinase\""
        }
      },
      {
        "type": "terminal",
        "service": "text",
        "parameters": {
          "operator": "exact_match",
          "value": "Viruses",
          "attribute": "rcsb_entity_source_organism.taxonomy_lineage.name"
        }
      },
      {
        "type": "terminal",
        "service": "text",
        "parameters": {
          "operator": "exact_match",
          "value": "X-RAY DIFFRACTION",
          "attribute": "exptl.method"
        }
      },
      {
        "type": "terminal",
        "service": "text",
        "parameters": {
          "operator": "less_or_equal",
          "value": 2.5,
          "attribute": "rcsb_entry_info.resolution_combined"
        }
      },
      {
        "type": "terminal",
        "service": "text",
        "parameters": {
          "operator": "greater",
          "attribute": "rcsb_entry_info.nonpolymer_entity_count",
          "value": 0
        }
      }
    ]
  },
  "return_type": "entry"
}

    jsonQueryUniProt = {
  "query": {
    "type": "group",
    "logical_operator": "and",
    "nodes": [
      {
        "type": "terminal",
        "service": "text",
        "parameters": {
          "operator": "exact_match",
          "value": "P69905",
          "attribute": "rcsb_polymer_entity_container_identifiers.reference_sequence_identifiers.database_accession"
        }
      },
      {
        "type": "terminal",
        "service": "text",
        "parameters": {
          "operator": "exact_match",
          "value": "UniProt",
          "attribute": "rcsb_polymer_entity_container_identifiers.reference_sequence_identifiers.database_name"
        }
      }
    ]
  },
  "return_type": "polymer_entity"
}

    # Make it bytes
    jsonQueryBytes = json.dumps(jsonQuery).encode("utf-8")

    cl.log("Performing query", "i")
    result = requests.post(searchUrlEndpoint, data=jsonQueryBytes)

    results = []
    for query_hit in result.json()["result_set"]:
        results.append(query_hit["identifier"])

    # String seperator has to be prefixed to turn it into a bytes object 
    # to use the string seperator to join a list containing bytes objects
    # and then the decode() method is used to obtain a string.
    return b''.join(result).decode('utf-8')


def searchStructureMotif():
    """ TODO """
    pass


def seach3dShape():
    """ TODO """
    pass
