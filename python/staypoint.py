# Stay Point API indicates the location where an individual agent has stayed for at least 15 minutes.
# It returns daily or hourly time series of stay points to a specified location on a specified date.

# JSON Request
# Method: POST
# URL: http://api.datastreamx.com/1925/605/v1/staypoint/v2/query

# json API: https://docs.python.org/3.6/library/json.html
# ast API: https://docs.python.org/3.6/library/ast.html
# Request.requests API: http://docs.python-requests.org/en/master/api/

import json, ast, requests

DataStreamXKey = "key"
URL = "http://api.datastreamx.com/1925/605/v1/staypoint/v2/query"

# Create queryBody dictionary
queryBody = {
                "date": "2017-05-29",
                "location":
                {
                    "locationType": "locationHierarchyLevel",
                    "levelType":"staypoint_subzone",
                    "id": "OTSZ02"
                },
                "queryGranularity":
                {
                    "type": "period",
                    "period": "PT1H"
                },
                "aggregations": [
                    {
                        "metric": "unique_agents",
                        "type": "hyperUnique"
                    }
                ]
            }

# print(type(queryBody)) # prints <class 'dict'>

# queryJson = json.dumps(queryBody)
# print(type(queryJson)) # prints <class 'str'>

# Execute POST request using Requests.request object's post method
# queryResponse is of Requests.response type
queryResponse = requests.post(URL, data = json.dumps(queryBody), headers = {'DataStreamX-Data-Key': DataStreamXKey, 'Content-Type': 'application/json'})

dataFile = open("../data/staypoint.json", "a+")

# Printing and writing data
for dictionary in queryResponse.json():
    # json.dumps() formats json to json format Python string
    # ast.literal_eval() safely evaluates the string - I excluded this
    print(json.dumps(dictionary, indent=4))
    json.dump(dictionary, dataFile)
