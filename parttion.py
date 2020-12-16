import pandas as pd
import geopandas as gpd
import random as rnd
import json
from fileBuild import delete_keys_from_dict

def parttionInit(adj, districtPopulation, districtNumber):
    return
def populationParttion(adj, districtPopulation, districtNumber, populationMargin = 0.05):

    margin = float(districtPopulation) * populationMargin
    upop = int(float(districtPopulation) + margin)
    lpop = int(float(districtPopulation) - margin)
    copy = adj.copy()
    geoIDgroups = {}
    d = 1

    while d <= districtNumber:
        print(d)
        setArray = []
        adjList = []
        setPop = 0
        while setPop < lpop:
            if len(setArray) != 0 and len(adjList) == 0:
                print('adjList 0')
                tempAdj = []
                try:
                    for id in setArray:
                        geoids = list(copy[f'{id}']['adjObj'].keys())
                        tempAdj.extend(geoids)
                    for dups in setArray:
                        adjList = [ elem for elem in tempAdj if elem != dups]
                except:
                    geoIDgroups[f'{d}'] = {
                        'Population': setPop,
                        'GEOID_set': setArray
                    }
                    leftover = 0
                    for k, v in copy.items():
                        leftover += v['Pop']

                    geoIDgroups[f'{d+1}'] = {
                        'Population': leftover,
                        'GEOID_set': list(copy.keys())
                    }
                    return geoIDgroups
            if len(setArray) == 0:
                GEOID = rnd.choice(list(copy.keys()))
                cbObj = copy[f'{GEOID}']
            else:
                GEOID = adjList[0]
                cbObj = copy[f'{GEOID}']
            adjList.extend(cbObj['adjObj'].keys())
            setPop += int(cbObj['Pop'])
            setArray.append(f'{GEOID}')
            adjList = [ elem for elem in adjList if elem != GEOID]
            copy = delete_keys_from_dict(copy, GEOID)

        geoIDgroups[f'{d}'] = {
            'Population': setPop,
            'GEOID_set': setArray
        }
        d += 1
    return geoIDgroups
