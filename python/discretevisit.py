# The OD Matrix API returns a list of origins for a specified destination or vice versa on a specified date, where an Origin-Destination pair are two consecutive Stay Points of an agent.

# JSON Request
# Method: POST
# URL: http://api.datastreamx.com/1925/605/v1/discretevisit/v2/query

# json API: https://docs.python.org/3.6/library/json.html
# ast API: https://docs.python.org/3.6/library/ast.html
# Request.requests API: http://docs.python-requests.org/en/master/api/

from datetime import datetime
import json, ast
import requests
import base64
import csv

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
csvFile = open("../data/discretevisit.csv", "a+", newline='')
csvWriter = csv.writer(csvFile)

if os.path.exists("../data/staypoint-hour.csv") == False:
    csvWriter.writerow(["timestamp", "hyperUnique_unique_agents", "longSum_total_records", "discrete_visit_planningarea",
                    "discrete_visit_planningregion", "discrete_visit_subzone"])

for region in region_codes:
    # Create queryBody dictionary
    queryBody = {
                    "date": "2018-01-01",
                    "location":
                    {
                        "locationType": "locationHierarchyLevel",
                        "levelType":"discrete_visit_planningregion",
                        "id": region
                    },
                    "queryGranularity":
                    {
                        "type": "period",
                        "period": "P1D"
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
                        "discrete_visit_planningarea",
                        "discrete_visit_subzone"
                    ],
                    "aggregations": [
                        {
                            "metric": "unique_agents",
                            "type": "hyperUnique"
                        },
                        {
                            "metric": "total_records",
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
    queryResponse = requests.post("https://apistore.datasparkanalytics.com:8243/discretevisit/v2/query",
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
        csvWriter.writerow([dictionary["timestamp"],
                            dictionary["event"]["hyperUnique_unique_agents"],
                            dictionary["event"]["longSum_total_records"],
                            dictionary["event"]["discrete_visit_planningarea"],
                            dictionary["event"]["discrete_visit_planningregion"],
                            dictionary["event"]["discrete_visit_subzone"]
                            ])
