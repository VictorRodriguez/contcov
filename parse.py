#!/usr/bin/python

import json

adds = {}
dels = {}
mods = {}

with open('result.json') as json_file:
    data = json.load(json_file)
    for p in data[0]['Diff']['Adds']:
        adds.append(p)
    for p in data[0]['Diff']['Dels']:
        dels.append(p)
    for p in data[0]['Diff']['Mods']:
        mods.append(p)
