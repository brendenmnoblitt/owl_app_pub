"""
name: @brenden.noblitt
date: 6/11/2023
"""
# LIBRARIES
import os
import sys
from pymongo import MongoClient

# SET CWD
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(root_path)

# PACKAGES
import server.env.secrets as GlobalVars

class FlaskMongoHandler:
    """Mongo Handler for front-end API

    Mongo handler for transporting data to the front-end application.
    Created as a separate class as to not couple DDL statements and
    avoid unwanted data modifications.

    Attributes:
        client (obj):
            A mongo client object from the pymongo library
        db (obj):
            The connected database to the mongo client
        db_name (str):
            The name of the database
    """
    def __init__(self, db: str) -> None:
        """Initializes a FlaskMongoHandler object

        Creates a FlaskMongoHandler object based on the specified database.

        Args:
            db (str):
                The name of the database to connect
        """
        self.client = MongoClient(GlobalVars.MONGO_CONN_STR)
        self.db_name = db
        self.db = self.client[db]

    def __str__(self) -> str:
        """Returns a string representation of the FlaskMongoHandler object"""
        return f"Flask Mongo Handler; DB: {self.db_name}"
    
    def pull_collection(self, collection_name: str, key: str) -> dict:
        """Pulls cleaned Blizzard API data

        Gets data from the specified mongo collection by the requested key.

        Args:
            collection_name (str):
                The name of the mongo collection to pull from
            key (str):
                The name of the key for the returned data
        """
        try:
            collection = self.db[collection_name]
            projection = {"_id": False}
            documents = collection.find({}, projection)
            data = {}
            for document in documents:
                group_key = document.get(key)
                if group_key:
                    data.setdefault(group_key, []).append(document)
            return data
        except:
            return None

    def pull_prod_data(self) -> dict:
        """Pulls processed Blizzard API data

        Gets processed data used for the front-end application
        """
        try:
            target_coll = self.db['PlayerProd']
            projection = {"_id": 0}

            prod_data = list(target_coll.find({}, projection))
            return prod_data
        except:
            return None
        
    def pull_player_stats(self) -> dict:
        projection = {"_id": 0}
        collection = self.db['PlayerStats']
        stats_data = list(collection.find({}, projection))
        return stats_data

    def close_conn(self) -> None:
        """Closes the established connection to Mongo"""
        self.client.close()




