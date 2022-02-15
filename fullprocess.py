"""
The aim of this module is to ingest data


Date: 15th of Feb, 2022
Author: Fabio Barbazza
"""
# import config file
from risk_assessment_tool import config

# set logging dict
config.set_logger()

# read config.json
config.read_config()


import numpy as np
import os
import json
from datetime import datetime
import pandas as pd
from pathlib import Path
import os
import logging

logger=logging.getLogger(__name__)

from risk_assessment_tool.src.ingestion import ingestion
#from src.training import training
#from src.scoring import scoring
#from src.deployment import deployment
#from src.diagnostics import diagnostics
#from src.reporting import reporting

##################Check and read new data
#first, read ingestedfiles.txt

#second, determine whether the source data folder has files that aren't listed in ingestedfiles.txt



##################Deciding whether to proceed, part 1
#if you found new data, you should proceed. otherwise, do end the process here


##################Checking for model drift
#check whether the score from the deployed model is different from the score from the model that uses the newest ingested data


##################Deciding whether to proceed, part 2
#if you found model drift, you should proceed. otherwise, do end the process here



##################Re-deployment
#if you found evidence for model drift, re-run the deployment.py script

##################Diagnostics and reporting
#run diagnostics.py and reporting.py for the re-deployed model


def workflow():
    """
        This is the orchestration method
    """
    try:

        logger.info('START')

        df_input=ingestion.merge_multiple_dataframe()


    except Exception as err:
        logger.exception(err)

if __name__=='__main__':
    workflow()






