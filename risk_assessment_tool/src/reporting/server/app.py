"""
This module provides the api

Date: 15th of Feb, 2022
Author: Fabio Barbazza
"""
from risk_assessment_tool import config


from flask import Flask, session, jsonify, request
import pandas as pd
import numpy as np
import pickle
import json
import os
import logging
logging.basicConfig(format='%(name)s %(funcName)s %(asctime)s %(message)s',level='DEBUG')

# append the path of the
# parent directory
from risk_assessment_tool.src.diagnostics import diagnostics
from risk_assessment_tool.src.scoring import scoring

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

confusion_matrix_path = os.path.join(config_dict['output_model_path'],'confusionmatrix.png') 


logger=logging.getLogger(__name__)

logger.info(__name__)


######################Set up variables for use in our script
app = Flask(__name__)



#######################Prediction Endpoint
@app.route("/prediction", methods=['GET','POST'])
def predict(): 
    """
    call the prediction function you created in Step 3
    add return value for prediction outputs
    """    
    logger.info('prediction')

    logger.info('dataset_csv_path: {}'.format(dataset_csv_path))

    # read data
    final_dataset=diagnostics.read_data(dataset_csv_path)
    #logger.info('final_dataset: {}'.format(str(final_dataset.head())))

    # read model
    model_trained=diagnostics.read_model(model_path)
    #logger.info('model_trained')

    # make prediction
    preds=diagnostics.make_prediction(model_trained,final_dataset)
    #logger.info('preds: {}'.format(preds))

    return {'preds':str(preds),'status_code':200}

    

#######################Scoring Endpoint
@app.route("/scoring", methods=['GET','OPTIONS'])
def stats():        
    """
    check the score of the deployed model
    add return value (a single F1 score number)
    """
    f1_score=scoring.calculate_score_model(test_data_path,model_path,scoring_model_path)

    return {'f1_score':str(f1_score),'status_code':200}


#######################Summary Statistics Endpoint
@app.route("/summarystats", methods=['GET','OPTIONS'])
def summarystats():       
    """
    check means, medians, and modes for each column
    return a list of all calculated summary statistics
    """
    final_dataset=diagnostics.read_data(dataset_csv_path)

    model_trained=diagnostics.read_model(model_path)

    preds=diagnostics.make_prediction(model_trained,final_dataset)

    list_mean,list_median,list_std=diagnostics.dataframe_summary(final_dataset) 
    #check means, medians, and modes for each column
    return {"list_mean":str(list_mean),"list_median":str(list_median),"list_std":str(list_std), "status_code":200}

#######################Diagnostics Endpoint
@app.route("/get_diagnostics", methods=['GET','OPTIONS'])
def get_diagnostics():        
    """
    check timing and percent NA values
    return #add return value for all diagnostics
    """
    logger.info('get_diagnostics')
    final_dataset=diagnostics.read_data(dataset_csv_path)

    list_na_values_perc=diagnostics.check_integrity(final_dataset)
    logger.info('list_na_values_perc: {}'.format(list_na_values_perc))

    list_timing=diagnostics.training_timing()
    logger.info('list_timing: {}'.format(list_timing))

    table_packages=diagnostics.outdated_packages_list()

    return {"timing":str(list_timing),"missing_data":str(list_na_values_perc),"dependency_checks":str(table_packages), "status_code":200}



if __name__ == "__main__":    
    app.run(host='0.0.0.0', port=8000, debug=True)
