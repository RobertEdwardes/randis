import pandas as pd
import geopandas as gpd
import random as rnd
import sys
import asyncio
import json
import csv
from collections import MutableMapping

def openJson(inputName):
    with open(f'{inputName}.json', "r") as f2:
            file = json.load(f2)
    return file

def csv_dict(inputName, array=None):
    if isinstance(arary, list) is False and array is not None :
        print('fieldName is wrong needs list of 1 param')
        sys.exit()
    with open(f'{inputName}.csv', newline='') as f2:
        file = csv.DictReader(f2, fieldName=f'{array}')
    return file

def delete_keys_from_dict(dict, keys):
    keys_set = keys
    modified_dict = {}
    for key, value in dict.items():
        if key not in keys_set:
            if isinstance(value, MutableMapping):
                modified_dict[key] = delete_keys_from_dict(value, keys_set)
            else:
                modified_dict[key] = value
    return modified_dict

def CensusBlockTable(geo, pl1, shp, baseName):
    PLGEO = pd.read_fwf(f'{geo}',widths=[6,2,3,2,3,2,7,1,1,2,3,2,2,5,2,2,5,2,2,6,1,4,2],header=None, dtype=str)
    print('PLGEO Loaded')
    PL1 = pd.read_csv(f'{pl1}', header=None, dtype=str)
    print('PL1 Loaded')
    PL1_logrec_pop = PL1.iloc[:,4:6]
    PL1_logrec_pop.columns = ['logrec', 'pop']
    PLGEOSimp = PLGEO.iloc[:, 6:22]
    PLGEOSimp.columns = ['logrec', 'region', 'division', 'state',
                        'county', 'ctycc', 'ctysc', 'cousub',
                        'cousubcc', 'cousubsc','place', 'placecc',
                        'placesc', 'tract', 'blkgrp', 'block']
    PLGEOSimp['GEOID'] = PLGEOSimp['state'].fillna('') + PLGEOSimp['county'].fillna('')  + PLGEOSimp['tract'].fillna('')  + PLGEOSimp['blkgrp'].fillna('')
    rslt_df = PLGEOSimp[PLGEOSimp['blkgrp'].notnull()]
    PL_Merged = pd.merge(rslt_df, PL1_logrec_pop, on=['logrec', 'logrec'])
    shp_file = gpd.read_file(shp)
    print('shp_file Loaded')
    ct = pd.merge(PL_Merged, shp_file, on=['GEOID','GEOID'])
    gdf = gpd.GeoDataFrame(ct, geometry=ct['geometry'])
    return gdf

def adjGraph(file, baseName):
    shp_file = file
    a = shp_file.copy()
    b = shp_file.copy()
    cbVE = {}
    total_rows = len(a.index)
    count = 0
    for idx, row in a.iterrows():
        count += 1
        polyA = row['geometry']
        geoID_A = row['GEOID']
        pop_a = row['pop']
        GEOID_array = []
        adjObj = {}
        for jdx, array in b.iterrows():
            polyB = array['geometry']
            geoID_B = array['GEOID']
            pop_b = array['pop']
            if polyA.touches(polyB) is True:
                adjObj[f'{geoID_B}'] = int(pop_b)
        cbVE[f'{geoID_A}'] = {'Pop': int(pop_a),
                             'adjObj': adjObj}
        print(f'{(count / total_rows)*100}%')
    with open(f"{baseName}_adj.json", "W") as outfile:
        json.dump(cbVE, outfile)
    return cbVE


def fileDescription(table, baseName, district=None):
    if district is None:
        print('Missing district. One is needed to produce map')
        sys.exit()
    pl_file = table
    description = pl_file['pop'].astype({'pop': 'int32'}).describe()
    description['district_pop'] = pl_file['pop'].astype({'pop': 'int32'}).sum()/district
    description['district'] = district
    description.to_csv(f'{baseName}_filedesc.csv')
    return description
