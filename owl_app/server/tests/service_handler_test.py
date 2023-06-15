"""
name: @brenden.noblitt
date: 6/1/2023
"""
import unittest
import sys
import os
import logging
from pathlib import Path

# SET CWD
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(root_path)

# PACKAGES
from handlers.service_handler import PlayerService
from handlers.mongo_handler import MongoDBHandler


class TestPlayerService(unittest.TestCase):
    """ Test suite for player service """
    def setUp(self):
        mongo_handler = MongoDBHandler(db='Players')
        self.team_roster = mongo_handler.import_team_rosters()
        self.player_service = PlayerService(self.team_roster)
        self.test_player = '15396'

    def test_player_lookup(self):
        actual_result = self.player_service.create_player_lookup()
        expected_result = ['name', 'id']
        self.assertEqual(expected_result, list(actual_result.keys()))
    
    def test_request_single_player_data(self):
        test_player = '15396'
        test_data = self.player_service.request_single_player_data(
            self.test_player)
        expected_results = ['Birdring', 15396]
        actual_results = [test_data['name'], test_data['id']]
        self.assertEqual(expected_results, actual_results)

    def test_parse_player_information(self):
        expected_data = {
            "number": 20,
            "preferredSlot": 1,
            "name": "Birdring",
            "familyName": "Kim",
            "role": "offense",
            "id": 15396
            }
        test_data = self.player_service.request_single_player_data(
            self.test_player)
        actual_data = self.player_service.parse_player_information(test_data)
        self.assertEqual(list(expected_data.keys()), list(actual_data.keys()))
    
    def test_player_stats(self):
        expected_data = {
            "number": 20,
            "player_name": "Birdring",
            "id": 15252,
            "heroDamageDone": 618286,
            "healingDone": 38048,
            "damageTaken": 305089,
            "finalBlows": 620,
            "eliminations": 1764,
            "deaths": 300,
            "timeSpentOnFire": 5450,
            "soloKills": 67,
            "ultsUsed": 317,
            "ultsEarned": 324,
            "timePlayed": 53052
            }
        test_data = self.player_service.request_single_player_data(
            self.test_player)
        actual_data = self.player_service.parse_player_stats(test_data)
        self.assertEqual(list(expected_data.keys()), list(actual_data.keys()))
    
    def test_player_media(self):
        expected_data = {
            "player_id": 15396,
            "headshot_url": "https://images.blz-contentstack.com/v3/assets/blt321317473c90505c/blt39bea5395fd7c591/64337aabbad30b6ff45736ec/Birdring_BostonUprising_600x600.png",
            "player_logo_url": None,
            "player_icon_url": None
            }
        test_data = self.player_service.request_single_player_data(
            self.test_player)
        actual_data = self.player_service.parse_player_media(test_data)
        self.assertEqual(list(expected_data.keys()), list(actual_data.keys()))

if __name__ == "__main__":
    unittest.main(verbosity=2)





