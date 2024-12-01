from os import environ as env
from algoliasearch.search.client import SearchClientSync
import json

# Algolia Config from .env (NECESSARY)
ALGOLIA_APP_ID = env["ALGOLIA_APP_ID"]
ALGOLIA_API_KEY = env["ALGOLIA_API_KEY"]
ALGOLIA_WORKOUT_INDEX = "Workouts"

client = SearchClientSync(ALGOLIA_APP_ID, ALGOLIA_API_KEY)







# ========= ALGOLIA FUNCTIONS =========
# These are here as examples from our project of how to use the Algolia API in Python
# It's best to only use the API for Create, Update, Delete. Searching is best done with instantsearch.js
# We left C, U, D functions in database.py so everything is in one place, but you can move them here if you want
# For more info, see https://www.algolia.com/doc/libraries/python/v4/

# Function to search the index using a query and return the SearchResponse object
def search_index(query, index_name=ALGOLIA_WORKOUT_INDEX):
    res = client.search(
        {
            "requests": [
                {
                    "indexName": index_name,
                    "query": query,
                }
            ]
        }
    )   
    
    # turn to json object and return
    return json.loads(res.to_json())

# Function to add multiple workouts to the index (such as when bulk importing)
# workouts is a JSON object with all the data for each workout (such as id, title, etc.)
def bulk_add_workouts(workouts):
    client.save_objects(index_name=ALGOLIA_WORKOUT_INDEX, objects=workouts)

# Function to delete all records for a given username
# def algolia_delete_user(username):
#     res = search_index(username, ALGOLIA_WORKOUT_INDEX)
#     hits = res['results'][0]['hits']
    
#     for hit in hits:
#         print(f"Deleting objectID: {hit['objectID']} from Workouts")
#         client.delete_object(index_name=ALGOLIA_WORKOUT_INDEX, object_id=hit['objectID'])
        
#     res = search_index(username, ALGOLIA_COMMUNITIES_INDEX)
#     hits = res['results'][0]['hits']
    
#     for hit in hits:
#         print(f"Deleting objectID: {hit['objectID']} from Communities")
#         client.delete_object(index_name=ALGOLIA_COMMUNITIES_INDEX, object_id=hit['objectID'])