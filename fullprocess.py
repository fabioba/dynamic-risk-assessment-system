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
scoring_model_path_prod = os.path.join(config_dict['prod_deployment_path'],'latestscore.txt') 
model_path_prod = os.path.join(config_dict['prod_deployment_path'],'trainedmodel.pkl') 
confusion_matrix_path_prod = os.path.join(config_dict['output_model_path'],'confusionmatrix2.png') 

path_ingestedfiles= os.path.join(config_dict['output_folder_path'],'ingestedfiles.txt')

confusion_matrix_path = os.path.join(config_dict['output_model_path'],'confusionmatrix.png') 


import logging

logger=logging.getLogger(__name__)

from risk_assessment_tool.src.ingestion import ingestion
from risk_assessment_tool.src.training import training
from risk_assessment_tool.src.scoring import scoring
from risk_assessment_tool.src.deployment import deployment
from risk_assessment_tool.src.diagnostics import diagnostics
from risk_assessment_tool.src.reporting import reporting
from risk_assessment_tool.src.reporting.server import apicalls

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

flag_automation=True

def check_read_new_data():
    """
        Check and read new data
    """
    try:
        # read ingestedfile.txt
        with open(path_ingestedfiles, 'r') as handler:
            ingested_files=handler.read().split('\n')

        logger.info('ingested_files: {}'.format(ingested_files))
        # check if there's some files in sourcedata that are not ingested yet
        list_elems=os.listdir(input_folder_path)
        logger.info('list_elems: {}'.format(list_elems))

        # get those files not ingested
        list_diff_files=list(set(set(list_elems)-set(ingested_files)))
        
        logger.info('len diff files: {}'.format(len(list_diff_files)))
        logger.info('list_diff_files: {}'.format(list_diff_files))


        # ingest not ingested files
        if len(list_diff_files):
            ingestion.merge_multiple_dataframe(input_folder_path,output_folder_path,list_diff_files)


        # read last score
        with open(scoring_model_path_prod,'r') as handler:
            scoring_stored=float(handler.read())
        logging.info('scoring_stored: {}'.format(scoring_stored))

        # run trained model
        model_trained=scoring.read_model(model_path_prod)
        data_stored=scoring.read_data(dataset_csv_path)

        preds=scoring.make_prediction(model_trained,data_stored)
        logging.info('preds: {}'.format(preds))

        new_score=scoring.score_model(preds,data_stored)
        logging.info('new score: {}'.format(new_score))

        # if new score < old score then drift has occured
        if new_score < scoring_stored:
            logging.info('MODEL DRIFT')
            training.train_model(dataset_csv_path,model_path_prod)

        else:

            reporting.score_model(dataset_csv_path,model_path_prod,confusion_matrix_path_prod,diagnostics.read_data,diagnostics.read_model)

        list_response=list()
        #Call each API endpoint and store the responses
        list_response.append(apicalls.get_response('prediction'))
        list_response.append(apicalls.get_response('scoring'))
        list_response.append(apicalls.get_response('summarystats'))
        list_response.append(apicalls.get_response('get_diagnostics'))
        
        # store all responses
        with open('apireturns2.txt','a+') as handler:
            for resp in list_response:
                handler.write(str(resp))
    except Exception as err:
        logger.exception(err)



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

        reporting.score_model(test_data_path,model_path,confusion_matrix_path,diagnostics.read_data,diagnostics.read_model)


        list_response=list()
        #Call each API endpoint and store the responses
        list_response.append(apicalls.get_response('prediction'))
        list_response.append(apicalls.get_response('scoring'))
        list_response.append(apicalls.get_response('summarystats'))
        list_response.append(apicalls.get_response('get_diagnostics'))
        
        # store all responses
        with open('apireturns.txt','a+') as handler:
            for resp in list_response:
                handler.write(str(resp))


    except Exception as err:
        logger.exception(err)

if __name__=='__main__':
    if flag_automation:
        check_read_new_data()
    else:
        workflow()






