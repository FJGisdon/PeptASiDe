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
class requestVariablesPDB:
    """
    TODO
    """
    # Variables
    entity_ids: list

    # Requests sequence positional features, namely here the UniProt ID.
    # A list of entity IDs is required (e.g. ["7VPG_2"]).
    requestUniProtID = """{
  polymer_entities(entity_ids: ["7VPG_2"]) {
    rcsb_polymer_entity_container_identifiers {
      entry_id
      entity_id
      uniprot_ids
    }
  }
}"""
    test =  """
query Query {
  allFilms {
    films {
      title
    }
  }
}
"""


@dataclass
class queryVariablesPDB:
    """
    TODO
    """

    # Finds PDB structures of serine peptidasesfiltered by enzyme classification
    # (EC) classes, determined by X-ray crystallography at a resolution better 
    # than 3.0 A. The results are further filtered for redundancy according to
    # matching_uniprot_accession and also mutant structures are discarded.
    serinePeptidasesEntities = {
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
              "attribute": "entity_poly.rcsb_mutation_count",
              "operator": "equals",
              "value": 0
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
      "aggregation_method": "matching_uniprot_accession"
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
    in the dataclass 'queryVariablesPDB'.
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

def requestDataPDB(query):
    """
    TODO
    """
    searchUrlEndpoint: str = 'https://data.rcsb.org/rest/v1/core'
    searchUrlEndpoint: str = "https://swapi-graphql.netlify.app/.netlify/functions/index"
    cl.log(query, "i")
    cl.log("Performing query", "i")
    result = requests.post(searchUrlEndpoint, data={'query': query})
    
    cl.log(result, "i")
    results = []
    for query_hit in result.json()["data"]:
        results.append(query_hit["uniprot_ids"])

    return results


def searchStructureMotif():
    """ TODO """
    pass


def seach3dShape():
    """ TODO """
    pass
