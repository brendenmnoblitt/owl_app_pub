"""
name: @brenden.noblitt
date: 6/8/2023
"""
# LIBRARIES
import os
import sys
import json

# SET CWD
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(root_path)

# PACKAGES
from handlers.service_handler import PlayerService


class CLPlayerLookup:

    def __init__(self):
        print("Initializing Player Service")
        self.player_service = PlayerService()
    
    def lookup(self):
        player_id = input("Please input a player id to lookup...")
        try:
            player_json = self.player_service.request_single_player_data(player_id)
            print("Player data found:")
            print(json.dumps(player_json, indent=2))
        except:
            print("Player not found, terminating...")

if __name__ == '__main__':
    cli = CLPlayerLookup()
    cli.lookup()
