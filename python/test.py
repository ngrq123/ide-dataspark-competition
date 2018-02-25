queryBody = {
                  "date": "2017-12-31",
                  "location":
                  {
                      "locationType": "locationHierarchyLevel",
                      "levelType":"staypoint_planningregion",
                      "id": "region"
                  },
                  "queryGranularity":
                  {
                      "type": "period",
                      "period": "PT1H"
                  },
                  "dimensionFacets": [
                      "staypoint_subzone",
                      "staypoint_planningarea",
                      "agent_nationality"
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

for key in queryBody.keys():
    print(key)

for value in queryBody.values():
    print(type(value))
