# Stay Point API indicates the location where an individual agent has stayed for at least 15 minutes.
# It returns daily or hourly time series of stay points to a specified location on a specified date.

# JSON Request
# Method: POST
# URL: http://api.datastreamx.com/1925/605/v1/staypoint/v2/query

# json API: https://docs.python.org/3.6/library/json.html
# ast API: https://docs.python.org/3.6/library/ast.html
# Request.requests API: http://docs.python-requests.org/en/master/api/

from datetime import datetime
import json, ast
import requests
import base64
import csv
import os.path
import time


consumerKey = "key"
consumerSecret = "secret"

keySecret = (consumerKey + ":" + consumerSecret).encode('utf-8')
consumerKeySecretB64 = base64.b64encode(keySecret).decode('utf-8')
tokenResponse = requests.post("https://apistore.datasparkanalytics.com/token",
                                data = { 'grant_type': 'client_credentials' },
                                headers = { 'Authorization': 'Basic ' + consumerKeySecretB64 })
token = tokenResponse.json()['access_token']

region_codes = ["CR", "ER", "NR", "NER", "WR"]

# Writing data to file
csvFile = open("../data/staypoint-hour.csv", "a+", newline='')
csvWriter = csv.writer(csvFile)

if os.path.exists("../data/staypoint-hour.csv") == False:
    csvWriter.writerow(["timestamp", "staypoint_planningregion", "hyperUnique_unique_agents", "longSum_total_stays", "longSum_sum_stay_duration",
"staypoint_planningarea", "staypoint_subzone"])

for region in region_codes:
    # Create queryBody dictionary
    queryBody = {
                    "date": "2018-01-31",
                    "location":
                    {
                        "locationType": "locationHierarchyLevel",
                        "levelType":"staypoint_planningregion",
                        "id": region
                    },
                    "queryGranularity":
                    {
                        "type": "period",
                        "period": "PT1H"
                    },
                    "filter": {
                        "type": "not",
                        "field":
                        {
                            "type": "selector",
                            "dimension": "agent_nationality",
                            "value": "SGP"
                        }
                    },
                    "dimensionFacets": [
                        "staypoint_subzone",
                        "staypoint_planningarea"
                    ],
                    "aggregations": [
                        {
                            "metric": "unique_agents",
                            "type": "hyperUnique"
                        },
                        {
                            "metric": "sum_stay_duration",
                            "type": "longSum"
                        },
                        {
                            "metric": "total_stays",
                            "type": "longSum"
                        }
                    ]
                }

    # print(type(queryBody)) # prints <class 'dict'>

    # queryJson = json.dumps(queryBody)
    # print(type(queryJson)) # prints <class 'str'>

    # Execute POST request using Requests.request object's post method
    # queryResponse is of Requests.response type
    # token variable is a valid access token (see Getting Started)
    queryResponse = requests.post("https://apistore.datasparkanalytics.com:8243/staypoint/v2/query",
                                    data = json.dumps(queryBody),
                                    headers = {
                                    'Authorization': 'Bearer ' + token,
                                    'Content-Type': 'application/json'
                                    })

    # Printing and writing data
    for dictionary in queryResponse.json():
        # json.dumps() formats json to json format Python string
        # ast.literal_eval() safely evaluates the string - I excluded this
        print(json.dumps(dictionary, indent=4))
        if dictionary != "fault":
            csvWriter.writerow([dictionary["timestamp"],
                                dictionary["event"]["staypoint_planningregion"],
                                dictionary["event"]["hyperUnique_unique_agents"],
                                dictionary["event"]["longSum_total_stays"],
                                dictionary["event"]["longSum_sum_stay_duration"],
                                dictionary["event"]["staypoint_planningarea"],
                                dictionary["event"]["staypoint_subzone"]
                                ])
