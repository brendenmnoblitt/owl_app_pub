"""
name: @brenden.noblitt
date: 5/29/2023
"""
# LIBRARIES
import os
import sys
import logging
from pymongo import MongoClient

# SET CWD
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(root_path)

# PACKAGES
from utils.logger import logger
import vars.globals as GlobalVars

# LOGGER
# logger = logging.getLogger(__name__)

class MongoDataHandler:

    def __init__(self, db: str):
        self.client = MongoClient(GlobalVars.MONGO_CONN_STR)
        self.db = self.client[db]
    
    def close_conn(self):
        self.client.close()

    def truncate_collection(self, collection_name: str) -> None:
        """Truncates the specified mongo collection

        Method that dynamically truncates a mongo collection. Use
        of this method is recommend to align with Blizzard's policy
        of retaining data for no longer than 30 days.
        
        Args:
            collection (str):
                The name of the collection to be truncated
        """
        collection = self.db[collection_name]
        result = collection.delete_many({})
        logger.info("Deleted %s documents from collection %s",
                    result.deleted_count, collection_name)

    def build_prod_player_data(self):
        projection = {"_id": 0}
        playermedia_coll = self.db['PlayerMedia']
        playermedia_docs = list(playermedia_coll.find({}, projection))

        teamroster_coll = self.db['TeamRoster']
        teamroster_docs = list(teamroster_coll.find({}, projection))

        playerinfo_coll = self.db['PlayerInfo']
        playerinfo_docs = list(playerinfo_coll.find({}, projection))

        teams_coll = self.db['Teams']
        teams_docs = list(teams_coll.find({}, projection))

        joined_data = []
        for playermedia_doc in playermedia_docs:
            player_id = playermedia_doc['player_id']
            
            matching_teamroster_docs = [
                teamroster_doc for teamroster_doc in teamroster_docs
                if player_id in teamroster_doc["player_ids"]
            ]
            matching_playerinfo_docs = [
                playerinfo_doc for playerinfo_doc in playerinfo_docs
                if player_id == playerinfo_doc['id']
            ]
            for teamroster_doc in matching_teamroster_docs:
                for playerinfo_doc in matching_playerinfo_docs:
                    matching_teams = [
                        team_doc for team_doc in teams_docs
                        if teamroster_doc['team_id'] == team_doc['team_id']
                    ]
                    for team in matching_teams:
                        joined_doc = {
                            'playerId': playerinfo_doc['id'],
                            'playerMedia': playermedia_doc,
                            'currentTeam': {'teamName': team['team_name'], 'teamId': team['team_id'], 'teamIcon': team['team_icon']},
                            'playerInfo': playerinfo_doc
                        }
                        joined_data.append(joined_doc)
        target_coll = self.db['PlayerProd']
        result = target_coll.insert_many(joined_data)
        print(f'Inserted {len(result.inserted_ids)} documents into {target_coll}')

