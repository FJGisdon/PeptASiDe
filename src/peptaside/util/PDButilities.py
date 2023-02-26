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
    @staticmethod
    def uniProtIDs(entity_ids: list):
        """  """
        # Requests sequence positional features, namely here the UniProt ID.
        # A list of entity IDs is required (e.g. ["7VPG_2"]).
        uniProtIDs = """query {
            polymer_entities(entity_ids: """+json.dumps(entity_ids)+""") {
                rcsb_polymer_entity_container_identifiers {
                    entry_id
                    entity_id
                    uniprot_ids
                    }
                }
            }
            """
        return uniProtIDs


@dataclass
class queryVariablesPDB:
    """
    TODO
    """

	# Finds PDB structures of serine peptidases filtered by enzyme classification
    # (EC) classes, determined by X-ray crystallography at a resolution better 
    # than 3.5 A. The results are further filtered for redundancy according to
    # matching_uniprot_accession and also mutant structures are discarded.
    cysteinePeptidasesEntities = {
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
              "value": "3.4.22"
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
              "value": 3.5,
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


    # Finds PDB structures of serine peptidases filtered by enzyme classification
    # (EC) classes, determined by X-ray crystallography at a resolution better 
    # than 3.5 A. The results are further filtered for redundancy according to
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
              "value": 3.5,
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
    #searchUrlEndpoint: str = 'https://data.rcsb.org/graphql'
    cl.log("Performing query", "i")
    #result = requests.post(searchUrlEndpoint, data={'query': query})
    result = requests.get(f'https://data.rcsb.org/graphql?query={query}')
    results = []
    if result.status_code == 200:
        response = result.json()['data']['polymer_entities']
        for item, entity in enumerate(response):
            entry_id = response[item]['rcsb_polymer_entity_container_identifiers']['entry_id']
            entity_id = response[item]['rcsb_polymer_entity_container_identifiers']['entity_id']
            uniprot_ids = response[item]['rcsb_polymer_entity_container_identifiers']['uniprot_ids']
            if len(response[item]['rcsb_polymer_entity_container_identifiers']['uniprot_ids']) == 1:
                results.append([entry_id+'_'+entity_id, "".join(uniprot_ids)])
            else:
                cl.log(f"Entity {entry_id+'_'+entity_id} was discarded, since it has two uniprot_ids: {uniprot_ids}", "i")
    else: cl.log(f"No data obtained from PDB, status code: {result.status_code} ", "w")
    cl.log(results, "d")

    return results


def searchStructureMotif():
    """ TODO """
    pass


def seach3dShape():
    """ TODO """
    pass
