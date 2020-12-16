import json
import csv
import os
import sys
import random as rd
import pandas as pd
from fileBuild import fileDescription


def randist(baseName):
    adj = openJson(f'{baseName}_adj')
    init = openJson(f'{baseName}_init')
    cbCSV = csv_dict(f'{baseName}')
    adjCopy = adj.copy()
    adj_subset = {}
    assigned_list = []
    cgp = None
    fd = openCSV(f'{baseName}_filedesc')
