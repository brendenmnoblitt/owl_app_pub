"""
name: @brenden.noblitt
date: 5/31/2023
"""
# LOGGING
import logging
import os
import platform
import sys

log_dir = os.path.join(os.getcwd() + '\server\owl_app\logs')
log_name = os.path.join(log_dir, 'python_tests_logs.log')
logging.basicConfig(level=logging.INFO,
                    filename=log_name,
                    filemode='w',
                    format="%(asctime)s %(levelname)s %(message)s")

