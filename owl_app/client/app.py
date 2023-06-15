"""
name: @brenden.noblitt
date: 6/10/2023
"""
# LIBRARIES
from flask import Flask, render_template
from pathlib import Path
import os
import sys

# SET CWD
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(root_path)

# PACKAGES
from handlers.flask_mongo_handler import FlaskMongoHandler

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/api/playerinfo")
def player_info():
    mongo_handler = FlaskMongoHandler(db='Players')
    player_info = mongo_handler.pull_prod_data()
    mongo_handler.close_conn()
    return player_info

@app.route("/api/playerstats")
def player_stats():
    mongo_handler = FlaskMongoHandler(db='Players')
    player_stats = mongo_handler.pull_player_stats()
    mongo_handler.close_conn()
    return player_stats

if __name__ == "__main__":
    app.run()
