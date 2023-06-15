"""
name: @brenden.noblitt
date: 5/15/2023
"""
# SET CWD
import os
import sys
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(root_path)

# LIBRARIES
import logging
import requests
import time
import json
from typing import List

# PACKAGES
import vars.globals as GlobalVars
import models.player_models as PlayerModel
import models.team_models as TeamModel
import models.segment_models as SegmentModel
import handlers.auth_handler as AuthHandler
from utils.logger import logger

# LOGGING
# logger = logging.getLogger(__name__)

class PlayerService:
    """API Services relating to Player data
    
    An object used for interacting with the player
    endpoints of the Blizzard API

    Attributes:
        token (str): A string bearer token used for authentication
    """
    def __init__(self, team_roster: dict):
        """Initializes a PlayerService object
        
        Creates a PlayerService object by using the authentication
        handler to create and assign an auth token.

        Raises:
            ValueError: Bearer token string contains 'error'
        """
        token = AuthHandler.get_bearer_token()
        if 'Error' not in token:
            self.token = token
            logger.info("Player service started")
        else:
            logger.error(f"There was an error when assigning the bearer token: {token}")
            raise ValueError(f"Error with bearer token: {token}")
        self.team_roster = team_roster

    def create_player_lookup(self) -> dict:
        """Creates a player lookup with player id's and names
        
        Creates a player lookup dictionary to connect data points
        from different api endpoints.

        Raises:
            (KeyError, ValueError): Returned JSON from Blizzard API
            doesn't fit the expected schema.
        
        Returns:
            status == 200 -> A dictionary of player names and id's
            status != 200 -> None
        
        """
        logger.info("Creating player lookup...")
        data = {"grant_type": "client_credentials"}
        headers = {"Authorization": self.token}
        response = requests.get(GlobalVars.US_BASE_URL + 
                                GlobalVars.SUMMARY_DATA_URL, 
                                headers=headers, 
                                data=data)
        response_json = response.json()
        response_status = response.status_code
        player_names = []
        player_ids = [] 
        
        if response_status == 200:
            logger.info("[%s]: Player lookup data received", response_status)
            try:
                for id in response_json['players']:
                    player = response_json['players'][id]
                    player_names.append(player['name'])
                    player_ids.append(player['id'])
                players = PlayerModel.Players(name=player_names, id=player_ids)
                logger.info("Player lookup successfully created")
                return players.dict()
            except (KeyError, ValueError) as excp:
                logger.error("An error occurred while creating the player lookup: %s",
                             excp)
                raise excp(f"An error occurred while creating the player lookup: {excp}")
        else:
            logger.error("An error occurred while requesting player data from the Blizzard API: [%s]: %s",
                         response_status, response_json)
            return None

    def request_single_player_data(self, player_id: int) -> dict:
        """Requests data for a single overwatch player
        
        Calls the Blizzard API for data on a single player.

        Args:
            player_id (int): An integer player id
        
        Returns:
            status == 200 -> A JSON response from the Blizzard API
            status != 200 -> None
        """
        logger.info("Requested data for player %s", player_id)
        data = {"grant_type": "client_credentials"}
        headers = {"Authorization": self.token}
        response = requests.get(GlobalVars.US_BASE_URL + 
                                GlobalVars.PLAYER_DATA_URL + (f"{player_id}"), 
                                headers=headers, 
                                data=data)
        response_json = response.json()
        response_status = response.status_code
        
        if response_status == 200:
            logger.info("[%s]: Data received for player %s", response_status, player_id)
            return response_json
        else:
            logger.error("An error occurred while requesting player data from the Blizzard API: [%s]: %s",
                        response_status, response_json)
            return None
    
    def parse_player_information(self, api_response: dict) -> dict:
        """Parses JSON from Blizzard API for basic player information

        Parses the requested JSON API response for basic player information, such
        as name and role.

        Args:
            api_response (dict): The JSON response from the Blizzard API
        
        Returns:
            A dictionary of parsed player information
        """
        logger.info("Parsing player information for player: %s", api_response['name'])
        try:
            player_info = PlayerModel.PlayerOverview.parse_obj(api_response)
            logger.info("Player information found for player: %s", api_response['name'])
            return player_info.dict()
        except (IndexError, KeyError):
            logger.error("An error occured while parsing for player %s", api_response['name'])
            return None
    
    def parse_player_stats(self, api_response: dict) -> dict:
        """Parses JSON from Blizzard API for player stats

        Parses the requested JSON API response for basic player statistics, such
        as damage done and time played.

        Args:
            api_response (dict): The JSON response from the Blizzard API
        
        Returns:
            A dictionary of parsed player stats
        """
        logger.info("Parsing player stats for player: %s", api_response['name'])
        current_player_id = api_response['id']
        current_team = None
        try:
            for team in self.team_roster:
                for idx, player_id in enumerate(team['player_ids']):
                    if team['player_ids'][idx] == current_player_id:
                        current_team = team['team_id']
        except(AttributeError) as excp:
            logger.error("An error occurred while parsing team roster")
        try:
            for idx, team in enumerate(api_response['teams']):
                if team['id'] == current_team:
                    playerstats_json = api_response['teams'][idx]
                    player_number = api_response['number']
                    player_name = api_response['name']
                    team_number = playerstats_json['id']
                    
                    player_stats = PlayerModel.PlayerStats.parse_obj(playerstats_json['stats'])
                    player_stats = player_stats.dict()
                    player_stats['number'] = player_number
                    player_stats['player_name'] = player_name
                    player_stats['id'] = team_number
                    return player_stats
        except (IndexError, KeyError) as excp:
            logger.error("An error occurred while parsing stats for player %s: %s",
                         api_response['name'], excp)
            return None
    
    def parse_player_media(self, api_response: dict) -> dict:
        """Parses JSON from Blizzard API for player media

        Parses the requested JSON API response for player media, such as
        their headshot image URL.

        Args:
            api_response (dict): The JSON response from the Blizzard API
        
        Returns:
            A dictionary of parsed player media
        """
        logger.info("Parsing player media for player: %s", api_response['name'])
        try:
            media_data = PlayerModel.PlayerMedia.parse_obj(api_response).dict()
            return media_data
        except (IndexError, KeyError) as excp:
            logger.error("An error occurred while parsing media for player %s: %s",
                         api_response['name'], excp)
    

class TeamService:
    """API Services relating to Team data
    
    An object used for interacting with the team
    endpoints of the Blizzard API

    Attributes:
        token (str): A string bearer token used for authentication
    """
    def __init__(self):
        """Initializes a PlayerService object
        
        Creates a PlayerService object by using the authentication
        handler to create and assign an auth token.

        Raises:
            ValueError: Bearer token string contains 'error'
        """
        token = AuthHandler.get_bearer_token()
        if 'Error' not in token:
            self.token = token
            logger.info("Team service started")
        else:
            logger.error(f"There was an error when assigning the bearer token: {token}")
            raise ValueError(f"Error with bearer token: {token}")

    def create_team_lookup(self) -> dict:
        """Creates a team lookup with team id's and names
        
        Creates a team lookup dictionary to connect data points
        from different api endpoints.

        Raises:
            (KeyError, ValueError): Returned JSON from Blizzard API
            doesn't fit the expected schema.
        
        Returns:
            status == 200 -> A dictionary of player names and id's
            status != 200 -> None
        
        """
        logger.info("Creating team lookup...")
        data = {"grant_type": "client_credentials"}
        headers = {"Authorization": self.token}
        response = requests.get(GlobalVars.US_BASE_URL + 
                                GlobalVars.SUMMARY_DATA_URL, 
                                headers=headers, 
                                data=data)
        response_json = response.json()
        response_status = response.status_code

        if response_status == 200:
            team_id = []
            team_name = []
            team_code = []
            team_icon = []
            logger.info("[%s] Data for team lookup received", response_status)
            try:
                for id in response_json['teams']:
                    team = response_json['teams'][id]
                    team_id.append(team['id'])
                    team_name.append(team['name'])
                    team_code.append(team['code'])
                    team_icon.append(team['icon'])
                team_lookup = TeamModel.TeamLookup(team_id = team_id,
                                                team_name = team_name,
                                                team_code = team_code,
                                                team_icon = team_icon)
                self.team_lookup = team_lookup
                logger.info("Team lookup successfully created")
                return team_lookup.dict()
            except (KeyError, ValueError) as excp:
                logger.error("An error occurred while creating the player lookup: %s",
                             excp)
                raise excp(f"An error occurred while creating the player lookup: {excp}")
        else:
          logger.error("An error occurred while requesting team data from the Blizzard API: [%s]: %s",
                         response_status, response_json)
          return None
    
    def request_team_data(self, team_id: int) -> dict:
        """Requests data for a single overwatch team
        
        Calls the Blizzard API for data on a single team.

        Args:
            player_id (int): An integer team id
        
        Returns:
            status == 200 -> A JSON response from the Blizzard API
            status != 200 -> None
        """
        logger.info("Requesting data for team %s", team_id)
        data = {"grant_type": "client_credentials"}
        headers = {"Authorization": self.token}
        response = requests.get(GlobalVars.US_BASE_URL + 
                                GlobalVars.TEAM_DATA_URL + (f"{team_id}"), 
                                headers=headers, 
                                data=data)
        response_json = response.json()
        response_status = response.status_code

        if response_status == 200:
            logger.info("[%s] Data received for team %s", response_status, team_id)
            return response_json
        else:
            logger.error("An error occurred while requesting team data from the Blizzard API: [%s]: %s",
                         response_status, response_json)
            return None

    def parse_team_roster(self, api_response: dict) -> dict:
        """Parses team roster from JSON API response

        Parses for the team roster in the team JSON API response

        Args:
            api_response (dict): JSON team response from the Blizzard API

        Returns:
            A dictionary with the team roster
        """
        try:
            player_ids = api_response['roster']
            team_roster = TeamModel.TeamRoster(team_id = api_response['id'],
                                player_ids = player_ids).dict()
            team_id_fill = [api_response['id']] * (len(team_roster['player_ids']))
            # team_roster['team_id'] = team_id_fill
            logger.info("Data found for team %s", api_response['id'])
            return team_roster
        except:
            logger.error("An error occurred while parsing data %s", api_response)

class SegmentService:
    """ API services relating to overwatch league segments (competitions) """
    def __init__(self):
        self.token = AuthHandler.get_bearer_token()
        print("Segment Service Started")

    def create_segment_lookup(self) -> dict:
        print("Creating Segment lookup...")
        data = {"grant_type": "client_credentials"}
        headers = {"Authorization": self.token}
        response = requests.get(GlobalVars.US_BASE_URL + 
                                GlobalVars.SUMMARY_DATA_URL, 
                                headers=headers, 
                                data=data).json()
        segment_id = []
        segment_name = []
        competition_id = []
        season_id = []

        for idx, id in enumerate(response['segments']):
            segment = response['segments'][id]
            print(segment['id'])
            segment_id.append(segment['id'])
            segment_name.append(segment['name'])
            competition_id.append(segment['competitionId'])
            season_id.append(segment['seasonId'])

        segment_lookup = SegmentModel.SegmentLookup(segment_id = segment_id,
                                                    segment_name = segment_name,
                                                    competition_id = competition_id,
                                                    season_id = season_id).json(indent=2)
        return segment_lookup










