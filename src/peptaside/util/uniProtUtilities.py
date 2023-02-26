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
from xml.etree import ElementTree
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

def requestDataUniProt(query: list):
    """
    TODO
    """
    cl.log("Performing query", "i")
    cl.log(query, "d")
    results = []
    if isinstance(query, list):
        pass
    else:
        query = [query]

    for item in query:
        cl.log(f'https://rest.uniprot.org/uniprotkb/search?format=json&fields=accession%2Cid%2Cft_act_site%2Csequence&query=%28{item}%29' ,"d")
        result = requests.get(f'https://rest.uniprot.org/uniprotkb/search?format=json&fields=accession%2Cid%2Cft_act_site%2Csequence&query=%28{item}%29')
        if result.status_code == 200:
            response = result.json()['results'][0]
            primaryAccession: str = response['primaryAccession']
            activeSite: list = []
            sequence: str = response['sequence']['value']
            if response.get('features') is not None:
                cl.log(f'{primaryAccession}', "d")
                for feature in response['features']:
                    if feature['type'] == 'Active site':
                        activeSite.append(feature['location']['start']['value'])
        else: cl.log(f"No data obtained from UniProt, status code: {result.status_code} ", "w")
        if not activeSite:
            cl.log(f"No active site information available on UniProt for accession {primaryAccession}\n->Discarted", "i")
        else:
            results.append([primaryAccession, activeSite, sequence])
    cl.log(results, "d")

    return results


def extractActiveSites(uniProtIDs: list):
    """
    TODO
    """
    results = []
    for uniprot_id in uniProtIDs:
        cl.log(f'Active site search for UniProt ID {uniprot_id}', 'i')
        # Define the URL for the UniProt REST API request
        url = f"https://www.uniprot.org/uniprot/{uniprot_id}.xml"

        # Send the request to the UniProt server and retrieve the response
        response = requests.get(url)

        # Extract the active site residue numbers from the XML
        active_site_residues = []
        if response.ok:
            xml_content = response.content
            root = ElementTree.fromstring(xml_content)
            for feature in root.findall(".//{http://uniprot.org/uniprot}feature[@type='active site']"):
                positions = feature.find("{http://uniprot.org/uniprot}location/{http://uniprot.org/uniprot}position")
                if positions is not None and positions.get("position") is not None:
                    active_site_residue_number = int(positions.get("position"))
                    active_site_residues.append(active_site_residue_number)
        else:
            print(f"Error: {response.status_code} - {response.reason}")

        # Retrieve the protein sequence from the UniProt REST API
        response = requests.get(f"https://www.uniprot.org/uniprot/{uniprot_id}.fasta")
        if response.ok:
            sequence_lines = response.text.split("\n")
            sequence = "".join(sequence_lines[1:])
        else:
            print(f"Error: {response.status_code} - {response.reason}")

        # Get the amino acid codes for the active site residues from the protein sequence
        active_site_residue_names = []
        for active_site_residue_number in active_site_residues:
            active_site_residue_name = sequence[active_site_residue_number - 1]
            active_site_residue_names.append(active_site_residue_name)
            results.append([uniprot_id, active_site_residue_number, active_site_residue_name])
        # Print the active site residue numbers and residue names
        #for i in range(len(active_site_residues)):
        #    print(f"Active site residue {active_site_residues[i]} ({active_site_residue_names[i]})")
    return results        


# ---------------------------------------------------------------------------
