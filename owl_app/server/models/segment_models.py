"""
name: @brenden.noblitt
date: 5/21/2023
"""
from pydantic import BaseModel, Field
from typing import List

class SegmentLookup(BaseModel):
    segment_id: List[str] = Field(None)
    segment_name: List[str] = Field(None)
    competition_id: List[str] = Field(None)
    season_id: List[str] = Field(None)




