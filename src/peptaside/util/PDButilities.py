#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Created By    : FJG
# Creation Date : 13/12/2022
version ='1.0.0'
# ---------------------------------------------------------------------------
"""
Utility to search and process PDB data.
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
class queryVariables:
    """
    TODO
    """

    # Finds PDB structures of serine peptidasesfiltered by enzyme classification
    # (EC) classes, determined by X-ray crystallography at a resolution better 
    # than 3.0 A. The results are further filtered for redundancy according to
    # sequence identity.
    serinePeptidasesEntitySequenceIdentity95 = {
      "query": {
        "type": "group",
        "logical_operator": "and",
        "nodes": [
            {
            "type": "terminal",
            "service": "text",
            "parameters": {
              "attribute": "rcsb_polymer_entity.rcsb_enzyme_class_combined.ec",
              "operator": "exact_match",
              "value": "3.4.21"
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
          }
        ]
    },
  "request_options": {
    "paginate": {
        "start": 0,
        "rows": 200000
        },
    "results_verbosity": "minimal",
    "group_by": {
      "aggregation_method": "sequence_identity",
      "similarity_cutoff": 95
    },
    "group_by_return_type": "representatives"
  },
"return_type": "polymer_entity"
}


# ---------------------------------------------------------------------------
# Functions
# ---------------------------------------------------------------------------

def searchPDB(query):
    """ 
    Perform PDB search with some query logic. Predefined queries can be found
    in the dataclass 'queryVariables'.
    """
    searchUrlEndpoint: str = 'https://search.rcsb.org/rcsbsearch/v2/query'


    # Make it bytes
    jsonQuery = json.dumps(query).encode("utf-8")

    cl.log("Performing query", "i")
    result = requests.post(searchUrlEndpoint, data=jsonQuery)

    results = []
    for query_hit in result.json()["result_set"]:
        results.append(query_hit["identifier"])

    return results


def searchStructureMotif():
    """ TODO """
    pass


def seach3dShape():
    """ TODO """
    pass
