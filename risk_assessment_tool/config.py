"""
This module contains all the global variables

Date: 15th of Feb, 2022
Author: Fabio Barbazza
"""
import json 
import logging
from pathlib import Path


def set_logger():
    logging.basicConfig(format='%(name)s %(funcName)s %(asctime)s %(message)s',level='INFO')

def read_config():
    with open(Path(__file__).parent / 'config/config.json','r') as f:
        config_dict = json.load(f) 

    return config_dict
        
logger=logging.getLogger(__name__)

#############Load config.json and get input and output paths


logger.info('read global vars')