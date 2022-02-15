"""
This module provides the api

Date: 15th of Feb, 2022
Author: Fabio Barbazza
"""


from flask import Flask, session, jsonify, request
import pandas as pd
import numpy as np
import pickle
import json
import os
import logging


from risk_assessment_tool.src.diagnostics import diagnostics
from risk_assessment_tool.src.scoring import scoring

from risk_assessment_tool import config

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


######################Set up variables for use in our script
app = Flask(__name__)
app.secret_key = '1652d576-484a-49fd-913a-6879acfa6ba4'

prediction_model = None


#######################Prediction Endpoint
@app.route("/prediction", methods=['POST','OPTIONS'])
def predict(): 
    """
    call the prediction function you created in Step 3
    add return value for prediction outputs
    """    

    # read data
    final_dataset=diagnostics.read_data(dataset_csv_path)

    # read model
    model_trained=diagnostics.read_model(model_path)

    # make prediction
    preds=diagnostics.make_prediction(model_trained,final_dataset)

    return {'preds':preds,'status_code':200}

    

#######################Scoring Endpoint
@app.route("/scoring", methods=['GET','OPTIONS'])
def stats():        
    """
    check the score of the deployed model
    add return value (a single F1 score number)
    """
    f1_score=scoring.calculate_score_model(test_data_path,model_path,scoring_model_path)

    return {'f1_score':f1_score,'status_code':200}


#######################Summary Statistics Endpoint
@app.route("/summarystats", methods=['GET','OPTIONS'])
def stats():       
    """
    check means, medians, and modes for each column
    return a list of all calculated summary statistics
    """
    final_dataset=diagnostics.read_data(dataset_csv_path)

    model_trained=diagnostics.read_model(model_path)

    preds=diagnostics.make_prediction(model_trained,final_dataset)

    list_mean,list_median,list_std=diagnostics.dataframe_summary(final_dataset) 
    #check means, medians, and modes for each column
    return {"list_mean":list_mean,"list_median":list_median,"list_std":list_std, "status_code":200}

#######################Diagnostics Endpoint
@app.route("/diagnostics", methods=['GET','OPTIONS'])
def stats():        
    """
    check timing and percent NA values
    return #add return value for all diagnostics
    """
    final_dataset=diagnostics.read_data(dataset_csv_path)

    model_trained=diagnostics.read_model(model_path)

    preds=diagnostics.make_prediction(model_trained,final_dataset)

    list_mean,list_median,list_std=diagnostics.dataframe_summary(final_dataset)

    list_na_values_perc=diagnostics.check_integrity(final_dataset)

    list_timing=diagnostics.training_timing()

    table_packages=diagnostics.outdated_packages_list()

    return {"timing":list_timing,"missing_data":list_na_values_perc,"dependency_checks":table_packages, "status_code":200}


if __name__ == "__main__":    
    app.run(host='0.0.0.0', port=8000, debug=True, threaded=True)
