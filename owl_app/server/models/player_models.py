"""
name: @brenden.noblitt
date: 5/15/2023
"""
from pydantic import BaseModel, Field
from typing import List

class Player(BaseModel):
    """ Data model for an overwatch league player """
    name: str
    id: int

class Players(BaseModel):
    """ Data model for a list of overwatch league players """
    name: List[str]
    id: List[int]

class PlayerOverview(BaseModel):
    """ Data model for player related statistics from Blizzard API """
    number: int
    preferredSlot: int = Field(None)
    name: str
    familyName: str = Field(None)
    role: str = Field(None)
    id: int

class PlayerStats(BaseModel):
    """ Data model for overall statistics on an overwatch league player """
    number: int = Field(None)
    player_name: str = Field(None)
    id: int = Field(None)
    heroDamageDone: int = Field(None)
    healingDone: int = Field(None)
    damageTaken: int = Field(None)
    finalBlows: int = Field(None)
    eliminations: int = Field(None)
    deaths: int = Field(None)
    timeSpentOnFire: int = Field(None)
    soloKills: int = Field(None)
    ultsUsed: int = Field(None)
    ultsEarned: int = Field(None)
    timePlayed: int = Field(None)

class PlayerMedia(BaseModel):
    player_id: int = Field(alias='id')
    headshot_url: str = Field(None, alias='headshotUrl')
    player_logo_url: str = Field(None, alias='logo')
    player_icon_url: str = Field(None, alias='icon')


