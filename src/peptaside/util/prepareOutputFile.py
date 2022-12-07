#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Created By    : FJG
# Creation Date : 07/12/2022
version ='1.0.0'
# ---------------------------------------------------------------------------
"""
Prepare the file and the path for the output if not written to stout.
"""
# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------
import os

# ---------------------------------------------------------------------------
# Functions
# ---------------------------------------------------------------------------

def check_file_writable(fp):
    """Checks if the given filepath is writable"""
    if os.path.exists(fp):
        if os.path.isfile(fp):
            return os.access(fp, os.W_OK)
        else:
            return False
    # target does not exist, check perms on parent dir
    parent_dir = os.path.dirname(fp)
    if not parent_dir: parent_dir = '.'
    return os.access(parent_dir, os.W_OK)
