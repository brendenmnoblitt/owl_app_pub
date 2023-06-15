"""
name: @brenden.noblitt
date: 5/31/2023
"""

# LOGGING
import logging
import os
import platform

log_dir = os.path.join(os.getcwd() + '/owl_app/server/logs/run')
log_name = os.path.join(log_dir, 'run.log')
logging.basicConfig(level=logging.INFO,
                    filename=log_name,
                    filemode='w',
                    format="%(asctime)s %(levelname)s %(message)s")
