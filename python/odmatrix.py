# The OD Matrix API returns a list of origins for a specified destination or vice versa on a specified date, where an Origin-Destination pair are two consecutive Stay Points of an agent.

# JSON Request
# Method: POST
# URL: http://api.datastreamx.com/1925/605/v1/odmatrix/v3/query

# json API: https://docs.python.org/3.6/library/json.html
# ast API: https://docs.python.org/3.6/library/ast.html
# Request.requests API: http://docs.python-requests.org/en/master/api/

from datetime import datetime
import json, ast
import requests
import base64

consumerKey = "key"
consumerSecret = "secret"

keySecret = (consumerKey + ":" + consumerSecret).encode('utf-8')
consumerKeySecretB64 = base64.b64encode(keySecret).decode('utf-8')
tokenResponse = requests.post("https://apistore.datasparkanalytics.com/token",
                                data = { 'grant_type': 'client_credentials' },
                                headers = { 'Authorization': 'Basic ' + consumerKeySecretB64 })
token = tokenResponse.json()['access_token']

# Create queryBody dictionary
# queryBody = {
#                 "date": "2017-06-01",
#                 "timeSeriesReference": "origin",
#                 "location":
#                 {
#                     "locationType": "locationHierarchyLevel",
#                     "levelType":"origin_subzone",
#                     "id": "OTSZ02"
#                 },
#                 "queryGranularity":
#                 {
#                     "type": "period",
#                     "period": "P1D"
#                 },
#                 "aggregations": [
#                     {
#                         "metric": "origin_subzone",
#                         "type": "String"
#                     },
#                     {
#                         "metric": "origin_planningarea",
#                         "type": "String"
#                     },
#                     {
#                         "metric": "origin_planningregion",
#                         "type": "String"
#                     },
#                     {
#                         "metric": "destination_subzone",
#                         "type": "String"
#                     },
#                     {
#                         "metric": "destination_planningarea",
#                         "type": "String"
#                     },
#                     {
#                         "metric": "destination_planningregion",
#                         "type": "String"
#                     },
#                     {
#                         "metric": "Duration",
#                         "type": "longSum"
#                     },
#                     {
#                         "metric": "Distance",
#                         "type": "longSum"
#                     },
#                     {
#                         "metric": "agent_year_of_birth",
#                         "type": "String"
#                     },
#                     {
#                         "metric": "agent_gender",
#                         "type": "String"
#                     },
#                     {
#                         "metric": "agent_race",
#                         "type": "String"
#                     },
#                     {
#                         "metric": "agent_nationality",
#                         "type": "String"
#                     },
#                     {
#                         "metric": "agent_home_subzone",
#                         "type": "String"
#                     },
#                     {
#                         "metric": "agent_home_planningarea",
#                         "type": "String"
#                     },
#                     {
#                         "metric": "agent_home_planningregion",
#                         "type": "String"
#                     },
#                     {
#                         "metric": "agent_work_subzone",
#                         "type": "String"
#                     },
#                     {
#                         "metric": "agent_work_planningarea",
#                         "type": "String"
#                     },
#                     {
#                         "metric": "agent_work_planningregion",
#                         "type": "String"
#                     },
#                     {
#                         "metric": "dominant_mode",
#                         "type": "String"
#                     },
#                     {
#                         "metric": "purpose",
#                         "type": "String"
#                     },
#                     {
#                         "metric": "origin_subzone_name",
#                         "type": "String"
#                     },
#                     {
#                         "metric": "origin_planningarea_name",
#                         "type": "String"
#                     },
#                     {
#                         "metric": "origin_planningregion_name",
#                         "type": "String"
#                     },
#                     {
#                         "metric": "destination_subzone_name",
#                         "type": "String"
#                     },
#                     {
#                         "metric": "destination_planningarea_name",
#                         "type": "String"
#                     },
#                     {
#                         "metric": "destination_planningregion_name",
#                         "type": "String"
#                     },
#                     {
#                         "metric": "agent_home_subzone_name",
#                         "type": "String"
#                     },
#                     {
#                         "metric": "agent_home_planningarea_name",
#                         "type": "String"
#                     },
#                     {
#                         "metric": "agent_home_planningregion_name",
#                         "type": "String"
#                     },
#                     {
#                         "metric": "unique_agents",
#                         "type": "hyperUnique"
#                     },
#                     {
#                         "metric": "sum_duration",
#                         "type": "longSum"
#                     },
#                     {
#                         "metric": "sum_distance",
#                         "type": "longSum"
#                     },
#                     {
#                         "metric": "total_records",
#                         "type": "longSum"
#                     }
#                 ]
#             }

queryBody = {
                "date": "2017-06-01",
                "timeSeriesReference": "origin",
                "location":
                {
                    "locationType": "locationHierarchyLevel",
                    "levelType":"origin_subzone",
                    "id": "OTSZ02"
                },
                "queryGranularity":
                {
                    "type": "period",
                    "period": "P1D"
                },
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

data = []

# Printing and writing data
for dictionary in queryResponse.json():
    # json.dumps() formats json to json format Python string
    # ast.literal_eval() safely evaluates the string - I excluded this
    print(json.dumps(dictionary, indent=4))
    data.append(dictionary)

# Writing data to file
dataFile = open("../data/staypoint.json", "w+")
json.dump(data, dataFile)
