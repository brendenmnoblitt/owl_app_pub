"""
name: @brenden.noblitt
date: 5/28/2023
"""
# LIBRARIES
import os
import sys
import json
import logging
from pymongo import MongoClient

# SET CWD
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(root_path)

# LOGGING
# logger = logging.getLogger(__name__)

# PACKAGES
import env.secrets as GlobalVars
from utils.logger import logger

class MongoDBHandler:
    """Mongo handler for Overwatch League App
    
    The handler that manages communication between the app and
    Mongo Cloud server.

    Attributes:
        client (obj):
            A mongo client object from the pymongo library
        db (obj):
            The connected database to the mongo client
    """
    def __init__(self, db: str) -> None:
        """Initializes a MongoDBHandler object

        Creates a mongo client connected to the specified database.

        Args:
            db (str): The name of the database to connect
        """
        logger.info("Mongo handler created with database: %s", db)
        self.client = MongoClient(GlobalVars.MONGO_CONN_STR)
        self.db = self.client[db]

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
        
    def import_team_rosters(self) -> dict:
        projection = {"_id": 0}
        collection = self.db['TeamRoster']
        team_roster = list(collection.find({}, projection))
        return team_roster

    def export_players(self, collection_name: str, player_dict: dict) -> None:
        """Exports parsed player data to mongo

        Exports the provided player dictionary to a specified collection.

        Args:
            collection (str):
                The name of the collection to write data to
            player_dict (dict):
                A dictionary of player data to export to mongo
        """
        collection = self.db[collection_name]
        
        if set(player_dict.keys()) == {'name', 'id'}:
            documents = []
            for i in range(len(player_dict['name'])):
                document = {
                    'name': player_dict['name'][i],
                    'id': player_dict['id'][i]
                }
                documents.append(document)
            
            result = collection.insert_many(documents)
            logger.info("Inserted %s documents into collection %s",
                        result.inserted_ids, collection_name)
        else:
            logger.error("player_dict does not contain the required keys")
            raise KeyError("player_dict does not contain the required keys")

    def export_player_overview(self, collection_name: str, player_info: dict) -> None:
        """Exports parsed player info data to mongo

        Exports the provided player info dictionary to a specified collection.

        Args:
            collection_name (str):
                The name of the collection to write data to
            player_info (dict):
                A dictionary of player info data to export to mongo
        """
        collection = self.db[collection_name]

        if set(player_info.keys()) == {'number', 'preferredSlot', 'name',
                                        'familyName', 'role', 'id'}:
            data = {
                'number': player_info['number'],
                'preferredSlot': player_info['preferredSlot'],
                'name': player_info['name'],
                'familyName': player_info['familyName'],
                'role': player_info['role'],
                'id': player_info['id']
            }
            result = collection.insert_one(data)
            logger.info("Inserted document ID: %s into collection %s",
                        result.inserted_id, collection_name)
        else:
            logger.error("player_dict does not contain the required keys")
            raise KeyError("Missing the required keys for player_info")
    
    def export_player_stats(self, collection_name: str, player_stats: dict) -> None:
        """Exports parsed player stats data to mongo

        Exports the provided player stats dictionary to a specified collection.

        Args:
            collection_name (str):
                The name of the collection to write data to
            player_stats (dict):
                A dictionary of player stats data to export to mongo
        """
        collection = self.db[collection_name]
        if player_stats is not None:
            data = {
                'number': player_stats['number'],
                'player_name': player_stats['player_name'],
                'id': player_stats['id'],
                'heroDamageDone': player_stats['heroDamageDone'],
                'healingDone': player_stats['healingDone'],
                'damageTaken': player_stats['damageTaken'],
                'finalBlows': player_stats['finalBlows'],
                'eliminations': player_stats['eliminations'],
                'deaths': player_stats['deaths'],
                'timeSpentOnFire': player_stats['timeSpentOnFire'],
                'soloKills': player_stats['soloKills'],
                'ultsUsed': player_stats['ultsUsed'],
                'ultsEarned': player_stats['ultsEarned'],
                'timePlayed': player_stats['timePlayed']
            }
            result = collection.insert_one(data)
            logger.info("Inserted document ID: %s into collection %s",
                        result.inserted_id, collection_name)
        else:
            logger.error("A player_stats of NoneType was passed into the export method")

    def export_player_media(self, collection_name: str, player_media: dict) -> None:
        """Exports parsed player media data to mongo

        Exports the provided player media dictionary to a specified collection.

        Args:
            collection_name (str):
                The name of the collection to write data to
            player_media (dict):
                A dictionary of player media data to export to mongo
        """
        collection = self.db[collection_name]

        data = {
            'player_id': player_media['player_id'],
            'headshot_url': player_media['headshot_url'],
            'player_logo_url': player_media['player_logo_url'],
            'player_icon_url': player_media['player_icon_url']
        }
        result = collection.insert_one(data)
        logger.info("Inserted document ID: %s into collection %s",
                    result.inserted_id, collection_name)
        
    def export_teams(self, collection: str, teams: dict) -> None:
        """Exports parsed team data to mongo

        Exports all overwatch league teams into a specified collection.

        Args:
            collection (str):
                The name of the collection to write data to
            teams (dict):
                A dictionary of team data to export to mongo
        """
        collection = self.db[collection]
        
        documents = []
        for i in range(len(teams['team_name'])):
            document = {
                'team_id': teams['team_id'][i],
                'team_name': teams['team_name'][i],
                'team_code': teams['team_code'][i],
                'team_icon': teams['team_icon'][i]
            }
            documents.append(document)

        result = collection.insert_many(documents)
        logger.info("Inserted %s documents into collection %s",
                    result.inserted_ids, collection)

    def export_team_roster(self, collection_name: str, team_roster: dict) -> None:
        """Exports parsed team roster data to mongo

        Exports all overwatch league teams into a specified collection.

        Args:
            collection (str):
                The name of the collection to write data to
            team_roster (dict):
                A dictionary of team roster data to export to mongo
        """
        collection = self.db[collection_name]

        try:
            data = {
                'team_id': team_roster['team_id'],
                'player_ids': team_roster['player_ids'],
            }
            result = collection.insert_one(data)
            logger.info("Inserted document ID: %s into collection %s",
                        result.inserted_id, collection_name)
        except (AttributeError, TypeError):
            logger.warning("An error occurred while writing team to mongo: %s",
                           team_roster)


