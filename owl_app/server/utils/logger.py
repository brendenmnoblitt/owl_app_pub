"""
name: @brenden.noblitt
date: 6/10/2023
"""
import logging
import os
from pathlib import Path
parent_dir = str(Path(__file__).parents[1])
log_path = os.path.join(parent_dir + r"\logs\run\run.log")
logging.basicConfig(level=logging.INFO,
                    filename=log_path,
                    filemode='w',
                    format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)





