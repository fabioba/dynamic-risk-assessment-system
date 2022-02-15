"""
The aim of this module is to ingest data


Date: 15th of Feb, 2022
Author: Fabio Barbazza
"""
# import config file
from risk_assessment_tool import config
import os

# set logging dict
config.set_logger()

# read config.json

config_dict = config.read_config()
input_folder_path = config_dict['input_folder_path']
output_folder_path = config_dict['output_folder_path']


dataset_csv_path = os.path.join(config_dict['output_folder_path'],'finaldata.csv') 
model_path = os.path.join(config_dict['output_model_path'],'trainedmodel.pkl') 

test_data_path = os.path.join(config_dict['test_data_path'],'testdata.csv') 
scoring_model_path = os.path.join(config_dict['output_model_path'],'latestscore.txt') 

prod_deployment_path= config_dict['prod_deployment_path']
path_ingestedfiles= os.path.join(config_dict['output_folder_path'],'ingestedfiles.txt')


import numpy as np
import json
from datetime import datetime
import pandas as pd
from pathlib import Path
import logging

logger=logging.getLogger(__name__)

from risk_assessment_tool.src.ingestion import ingestion
from risk_assessment_tool.src.training import training
from risk_assessment_tool.src.scoring import scoring
from risk_assessment_tool.src.deployment import deployment
from risk_assessment_tool.src.diagnostics import diagnostics

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

        ingestion.merge_multiple_dataframe(input_folder_path,output_folder_path)

        training.train_model(dataset_csv_path,model_path)

        scoring.calculate_score_model(test_data_path,model_path,scoring_model_path)

        deployment.store_model_into_pickle(scoring_model_path, model_path,path_ingestedfiles, prod_deployment_path)

        diagnostics.check_data(dataset_csv_path,model_path)


    except Exception as err:
        logger.exception(err)

if __name__=='__main__':
    workflow()






