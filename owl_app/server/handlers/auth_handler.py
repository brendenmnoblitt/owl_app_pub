"""
name: @brenden.noblitt
date: 6/1/2023
"""
# LIBRARIES
import env.secrets as secrets
import requests
import base64
import logging
from oauthlib.oauth2 import WebApplicationClient
import os
import sys

# SET CWD
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(root_path)

# GLOBALS 
TOKEN_URL = "https://oauth.battle.net/token"
AUTHORIZE_URL = "https://oauth.battle.net/authorize"
CLIENT_ID = "d3bfc0487992446fb484b8310e2ae3ea"
CLIENT_SECRET = "GNgdso0Dt0mo1T3KVi6FiBdjIe4OEVtB"
DATA = {"grant_type": "client_credentials"}

# LOGGING
from utils.logger import logger

def get_bearer_token() -> str:
    HEADERS = {"Content-Type": "application/x-www-form-urlencoded"}
    auth = (secrets.CLIENT_ID, secrets.CLIENT_SECRET)
    auth_string = f"{secrets.CLIENT_ID}:{secrets.CLIENT_SECRET}"
    encoded_auth_string = base64.b64encode(auth_string.encode()).decode("utf-8")
    HEADERS["Authorization"] = f"Basic {encoded_auth_string}"

    response = requests.post(TOKEN_URL, headers=HEADERS, data=DATA)

    if response.status_code == 200:
        access_token = response.json()["access_token"]
        logger.info("OAuth battle.net token received")
        return (f"Bearer {access_token}")
    else:
        logger.error("An error occurred while requesting OAth token %s: %s",
                     response.status_code, response.text)
        return(f"Error: {response.status_code} - {response.text}")