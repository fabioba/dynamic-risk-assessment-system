"""
The aim of this module is to train input data


Date: 15th of Feb, 2022
Author: Fabio Barbazza
"""
# import config file
from risk_assessment_tool import config

#from flask import Flask, session, jsonify, request
import pandas as pd
import numpy as np
import pickle
import os
from sklearn import metrics
#from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import json
import logging
from pathlib import Path

config_dict = config.read_config()
input_folder_path = config_dict['input_folder_path']
output_folder_path = config_dict['output_folder_path']


dataset_csv_path = os.path.join(config_dict['output_folder_path'],'finaldata.csv') 
model_path = os.path.join(config_dict['output_model_path'],'trainedmodel.pkl') 

test_data_path = os.path.join(config_dict['test_data_path'],'testdata.csv') 
scoring_model_path = os.path.join(config_dict['output_model_path'],'latestscore.txt') 

prod_deployment_path= config_dict['prod_deployment_path']
path_ingestedfiles= os.path.join(config_dict['output_folder_path'],'ingestedfiles.txt')


logger=logging.getLogger(__name__)



#################Function for training the model
def train_model(dataset_csv_path,model_path):
    """
        This method is the entrypoint of the module


        Args:
            dataset_csv_path(str)
            model_path(str)
    
    """
    try:
        df=read_data(dataset_csv_path)


        X,y=get_x_y_data(df)


        #use this logistic regression for training
        lr=LogisticRegression(C=1.0, class_weight=None, dual=False, fit_intercept=True,
                        intercept_scaling=1, l1_ratio=None, max_iter=100,
                        multi_class='auto', n_jobs=None, penalty='l2',
                        random_state=0, solver='liblinear', tol=0.0001, verbose=0,
                        warm_start=False)
        
        #fit the logistic regression to your data
        lr.fit(X,y)
        
        #write the trained model to your workspace in a file called trainedmodel.pkl
        with open(model_path, 'wb') as handle:
            pickle.dump(lr, handle, protocol=pickle.HIGHEST_PROTOCOL)


    except Exception as err:
        logger.exception(err)
        raise

def read_data(dataset_csv_path):
    """
    read data from path

    Args:
        path(str): path of the input file
    """
    try:
        df=pd.read_csv(dataset_csv_path)

        return df

    except Exception as err:
        logger.exception(err)
        raise

def get_x_y_data(df):
    """
        This method returns one array per X and one per Y

        Args:
            df(pandas DF)

        Output:
            X(np array)
            y(np arra)
    """
    try:

        X=df.loc[:,['lastmonth_activity','lastyear_activity','number_of_employees']].values.reshape(-1, 3)
        y=df['exited'].values.reshape(-1, 1)

        return X,y

    except Exception as err:
        logger.exception(err)
        raise






