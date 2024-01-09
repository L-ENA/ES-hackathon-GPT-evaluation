# -*- coding: utf-8 -*-
"""
Created on Thu Sep 19 13:50:24 2019

Unzipping the ebm-nlp data can take a while on windows, because it contains so many tiny files.
This script works faster than the normal unzipping process on Windows

@author: Lena Schmidt, University of Bristol
"""

from zipfile import ZipFile

with ZipFile("archive.zip", 'r') as zipObj:
   # Extract all the contents of zip file in current directory
   zipObj.extractall()