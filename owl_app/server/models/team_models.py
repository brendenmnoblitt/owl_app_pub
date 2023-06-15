"""
name: @brenden.noblitt
date: 5/21/2023
"""
from pydantic import BaseModel, Field
from typing import List

class TeamLookup(BaseModel):
    team_id: List[int]
    team_name: List[str]
    team_code: List[str]
    team_icon: List[str]

class TeamRoster(BaseModel):
    team_id: int
    player_ids: List[int]







