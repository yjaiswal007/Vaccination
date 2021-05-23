import json
import os
import pandas as pd


files = os.listdir()
path = os.getcwd()

json_files = [x for x in files if '.json' in x]

# read and convert to df
for file in json_files[:1]:
    with open(os.path.join(path, file), 'r') as fh:
        data = json.load(fh)

df1 = pd.json_normalize(data['centers'])
df2 = pd.json_normalize(df1['sessions'].str[0])
df = pd.concat([df1, df2], axis=1)