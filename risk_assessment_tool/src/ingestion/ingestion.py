"""
The aim of this module is to ingest data


Date: 15th of Feb, 2022
Author: Fabio Barbazza
"""
# import config file
from risk_assessment_tool import config
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

config_dict = config.read_config()
input_folder_path = config_dict['input_folder_path']
output_folder_path = config_dict['output_folder_path']



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


def store_list_files(list_files):
    """
        This method store the list of read files

        Args:
            list_files(list): list files to create output df
    """
    try:
        output_path=str(Path(__file__).parent / output_folder_path / 'ingestedfiles.txt')
        
        with open(output_path, 'w') as f:
            for item in list_files:
                f.write("%s\n" % item)

        logger.info('SUCCESS')

    except Exception as err:
        logger.exception(err)
        raise


def merge_multiple_dataframe():
    """
        This method ingest data from folders


        Output:
            df(pandas DF)
    """
    try:

        df_final=pd.DataFrame()

        data_folder=str(Path(__file__).parent / input_folder_path)

        # get all elements in folder
        list_elems=os.listdir(data_folder)
        for file in list_elems:
            logger.info('elem in {} folder: {}'.format(data_folder,file))

            path_file=os.path.join(data_folder,file)

            logger.info('path_file: {}'.format(path_file))

            # get extension
            ext=check_extension_file(path_file)

            # read data

            df_temp=read_file(path_file,ext)
            df_final=df_final.append(df_temp)

        clean_data(df_final)

        store_data(df_final)

        store_list_files(list_elems)

        return df_final
                
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

def store_data(df):
    """
        This method gets as argument the dataframe to be stored as csv

        Args(pandas DF)
    """
    try:
        output_path=str(Path(__file__).parent / output_folder_path / 'finaldata.csv')
        df.to_csv(output_path)

        logger.info('SUCCESS')

    except Exception as err:
        logger.exception(err)
        raise


