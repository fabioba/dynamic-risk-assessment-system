"""
The aim of this module is to ingest data


Date: 15th of Feb, 2022
Author: Fabio Barbazza
"""
from risk_assessment_tool import config

import numpy as np
import os
import json
from datetime import datetime
import pandas as pd
from pathlib import Path
import os
import logging

logger=logging.getLogger(__name__)

config_dict = config.read_config()
input_folder_path = config_dict['input_folder_path']
output_folder_path = config_dict['output_folder_path']


dataset_csv_path = os.path.join(config_dict['output_folder_path'],'finaldata.csv') 
model_path = os.path.join(config_dict['output_model_path'],'trainedmodel.pkl') 

test_data_path = os.path.join(config_dict['test_data_path'],'testdata.csv') 
scoring_model_path = os.path.join(config_dict['output_model_path'],'latestscore.txt') 

prod_deployment_path= config_dict['prod_deployment_path']
path_ingestedfiles= os.path.join(config_dict['output_folder_path'],'ingestedfiles.txt')


def check_extension_file(file):
    """
        This method gets a file as input and return its extension

        Args:
            file(str): path of the file

        Output:
            ext(str): extension of the file
    """
    try:
        ext=Path(file).suffix
        return ext

    except Exception as err:
        logger.exception(err)
        raise


def read_file(path_file,ext):
    """
        This method gets path of the file and its extension and read the content

        Args:
            path_file(str): path of the file
            ext(str): extension of the file
    """
    try:
        if ext=='.csv':
            df=pd.read_csv(path_file)
        elif ext=='.json':
            df=pd.read_json(path_file)
        else:
            df=pd.DataFrame()

        return df

    except Exception as err:
        logger.exception(err)
        raise


def store_list_files(list_files,output_folder_path):
    """
        This method store the list of read files

        Args:
            list_files(list): list files to create output df
            output_folder_path(str)
    """
    try:
        output_path=os.path.join( output_folder_path , 'ingestedfiles.txt')
        
        with open(output_path, 'a+') as f:
            for item in list_files:
                f.write("%s\n" % item)

        logger.info('SUCCESS')

    except Exception as err:
        logger.exception(err)
        raise


def merge_multiple_dataframe(input_folder_path,output_folder_path,list_ingested_prior=list()):
    """
        This method ingest data from folders

        Args:
            input_folder_path(str): path input data
            output_folder_path(str): path output folder
            list_ingested_prior(list): list previous ingested files (empty as default)


    """
    try:

        df_final=pd.DataFrame()

        data_folder=input_folder_path

        # get all elements in folder
        list_elems=os.listdir(data_folder)

        # if list has been passed 
        if len(list_ingested_prior)>0:
            list_file_to_ingest=list_ingested_prior
        else:
            # get file to ingest
            list_file_to_ingest=list(set(set(list_elems)-set(list_ingested_prior)))

        for file in list_file_to_ingest:
            logger.info('elem in {} folder: {}'.format(data_folder,file))

            path_file=os.path.join(data_folder,file)

            logger.info('path_file: {}'.format(path_file))

            # get extension
            ext=check_extension_file(path_file)

            # read data

            df_temp=read_file(path_file,ext)
            df_final=df_final.append(df_temp)

        clean_data(df_final)

        store_data(df_final,output_folder_path)

        store_list_files(list_elems,output_folder_path)
                
    except Exception as err:
        logger.exception(err)
        raise


def clean_data(df):
    """
        This method cleans data

        Args(pandas DF)
    """
    try:
        df.drop_duplicates(inplace=True)
        logger.info('SUCCESS')

    except Exception as err:
        logger.exception(err)
        raise        

def store_data(df,output_folder_path):
    """
        This method gets as argument the dataframe to be stored as csv

        Args:
            df(pandas DF)
            output_folder_path(str)
    """
    try:
        output_path=os.path.join(output_folder_path , 'finaldata.csv')
        df.to_csv(output_path)

        logger.info('SUCCESS')

    except Exception as err:
        logger.exception(err)
        raise


