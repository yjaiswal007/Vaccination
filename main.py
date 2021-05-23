
import requests
import datetime
import json
import pandas as pd
from fake_useragent import UserAgent
import time
import os
import random

# create temp user agent
temp_user_agent = UserAgent()
browser_header = {'User-Agent': temp_user_agent.random}

path = os.getcwd()

# check if we have district codes otherwise generate it
if not os.path.exists(os.path.join(path, 'district_codes.csv')):
    # get districts codes
    json_data = {}
    for state_code in range(1, 40):
        print("State code: ", state_code)
        response = requests.get("https://cdn-api.co-vin.in/api/v2/admin/location/districts/{}".format(state_code), headers=browser_header)
        time.sleep(1 + (random.randint(1, 9)/10))
        json_data[state_code] = json.loads(response.text)
        for i in json_data[state_code]["districts"]:
            print(i["district_id"], '\t', i["district_name"])
        print("\n")

    # write district codes to file
    df_ids = pd.DataFrame()
    for state_id in json_data.keys():
        df_temp = pd.json_normalize(json_data[state_id]['districts'])
        df_temp['state_id'] = [state_id]*len(df_temp)
        df_ids = pd.concat([df_ids, df_temp], axis=0)

    df_ids = df_ids.astype({'district_id': int, 'state_id': int})
    df_ids = df_ids[['state_id', 'district_id', 'district_name']]
    df_ids.to_csv(os.path.join(path, 'district_codes.csv'), index=False)

# DIST_ID = 392 # Thane
# DIST_ID = 167 # Valsad
# DIST_ID = 164 # Navsari
# DIST_ID = 163 # Dangs
# DIST_ID = 137 # DNH
# DIST_ID = 138 # Daman
# DIST_ID = 389 # Nashik
# DIST_ID = 394 # Palghar
# DIST_ID = 394 # Palghar
# DIST_ID = 388 # Dhule
# DIST_ID = 387 # Nandurbar
# DIST_ID = 165 # Surat
dist_ids = [137, 138, 163, 164, 165, 167, 387, 388, 389, 394]
# dist_ids = [138,  167]

numdays = 7

base = datetime.datetime.today()
date_list = [base + datetime.timedelta(days=x) for x in range(numdays)]
date_str = [x.strftime("%d-%m-%Y") for x in date_list]

df = pd.DataFrame()
for INP_DATE in date_str:

    for DIST_ID in dist_ids:

        URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={}&date={}".format(
            DIST_ID, INP_DATE)

        response = requests.get(URL, headers=browser_header)
        time.sleep(2.1 + (random.randint(1, 9)/10))

        if response.ok:
            resp_json = response.json()

            with open(str(DIST_ID) + '_' + INP_DATE + '.json', 'w') as fh:
                json.dump(resp_json, fh, indent=4)

            if resp_json["centers"]:
                print("Available on: {} in {}".format(INP_DATE, DIST_ID))
                df1 = pd.json_normalize(resp_json['centers'])
                df2 = pd.json_normalize(df1['sessions'].str[0])
                df_temp = pd.concat([df1, df2], axis=1)
                df = pd.concat([df, df_temp], axis=0)

            else:
                print("No available slots on {} in {}".format(INP_DATE, DIST_ID))

# write df to file
df.to_csv(os.path.join(path, date_str[0] + '_vaccine_availability.csv'), index=False)
