"""
The aim of this module is to deploy the model folder


Date: 15th of Feb, 2022
Author: Fabio Barbazza
"""
import pandas as pd
import pickle
import logging
import os

logger=logging.getLogger(__name__) 


####################function for deployment
def store_model_into_pickle(scoring_model_path, model_path, path_ingestedfiles,prod_deployment_path):
    """
        Copy the latest pickle file, the latestscore.txt value, and the ingestfiles.txt file into the deployment directory

        Args:
            scoring_model_path(str)
            model_path(str)
            path_ingestedfiles(str)
            prod_deployment_path(str): path of the folder where to store data
    """
    try:

        # copy trained model
        model_path_deployed=os.path.join(prod_deployment_path,'trainedmodel.pkl')
        with open(model_path, 'rb') as handle:
            model_trained = pickle.load(handle)

        with open(model_path_deployed, 'wb') as handle:
            pickle.dump(model_trained, handle, protocol=pickle.HIGHEST_PROTOCOL)

        # copy model score file
        score_path_deployed=os.path.join(prod_deployment_path,'latestscore.txt')
        with open(scoring_model_path, 'rb') as handle:
            score_txt = handle.read()

        with open(score_path_deployed, 'wb') as handle:
            handle.write(score_txt)

        # copy ingested file records
        ingested_data_path_deployed=os.path.join(prod_deployment_path,'ingestedfiles.txt')
        with open(scoring_model_path, 'rb') as handle:
            ingested_txt = handle.read()

        with open(ingested_data_path_deployed, 'wb') as handle:
            handle.write(ingested_txt)

        logger.info('SUCCESS')


    except Exception as err:
        logger.exception(err)
        raise
        
        

