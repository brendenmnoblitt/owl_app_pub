"""
name: @brenden.noblitt
date: 5/15/2023
"""
# LIBRARIES
import json
import time
from tqdm import tqdm

# SET CWD
import os, sys
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(root_path)

# PACKAGES
import handlers.service_handler as ServiceHandler
import handlers.mongo_handler as MongoHandler
from handlers.data_handler import MongoDataHandler

def run_player():
    """ Runs player pipeline """
    mongo_handler = MongoHandler.MongoDBHandler(db='Players')
    team_roster = mongo_handler.import_team_rosters()
    player_service = ServiceHandler.PlayerService(team_roster=team_roster)
    mongo_handler.truncate_collection('Player')
    mongo_handler.truncate_collection('PlayerInfo')
    mongo_handler.truncate_collection('PlayerMedia')
    mongo_handler.truncate_collection('PlayerStats')
    players = player_service.create_player_lookup()
    mongo_handler.export_players('Player', players)
    print("Beginning run job for Players")
    for id in tqdm(players['id'], desc='Progress'):
        player_response = player_service.request_single_player_data(id)
        player_information = player_service.parse_player_information(player_response)
        player_stats = player_service.parse_player_stats(player_response)
        player_media = player_service.parse_player_media(player_response)
        mongo_handler.export_player_overview('PlayerInfo', player_information)
        mongo_handler.export_player_media('PlayerMedia', player_media)
        mongo_handler.export_player_stats('PlayerStats', player_stats)

def run_team():
    """ Runs team pipeline """
    team_service = ServiceHandler.TeamService()
    mongo_handler = MongoHandler.MongoDBHandler(db='Players')
    teams = team_service.create_team_lookup()
    mongo_handler.truncate_collection('Teams')
    mongo_handler.truncate_collection('TeamRoster')
    mongo_handler.export_teams('Teams', teams)
    print("Beginning run job for Teams")
    for team_id in tqdm(teams['team_id'], desc='Progress'):
        team_json = team_service.request_team_data(team_id)
        team_roster = team_service.parse_team_roster(team_json)
        mongo_handler.export_team_roster('TeamRoster', team_roster)

def run_data_handler():
    """ Runs data handler """
    data_handler = MongoDataHandler('Players')
    data_handler.truncate_collection('PlayerProd')
    data_handler.build_prod_player_data()


if __name__ == "__main__":
    run_player()
    time.sleep(5)
    run_team()
    time.sleep(5)
    run_data_handler()
