{
                "date": "2018-01-01",
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
                "filter":
                {
                    "type": "not",
                    "field":
                    {
                        "type": "selector",
                        "dimension": "agent_nationality",
                        "value": "SGP"
                    }
                },
                "dimensionFacets": [
                    "agent_nationality"
                ],
                "aggregations": [
                    {
                        "metric": "unique_agents",
                        "type": "hyperUnique"
                    }
                ]
            }
