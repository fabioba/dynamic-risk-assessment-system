"""
The aim of this module is to make diagnostic on trained model


Date: 15th of Feb, 2022
Author: Fabio Barbazza
"""

from cgi import test
import pandas as pd
import numpy as np
import timeit
import os
import pickle
import logging
import subprocess
import json

logger=logging.getLogger(__name__) 



##################Function to get model predictions
def check_data(dataset_csv_path,model_path):
    """
    Check data

        Args:
            dataset_csv_path(str)
            model_path(str)
    
    """
    try:

        final_dataset=read_data(dataset_csv_path)

        model_trained=read_model(model_path)

        preds=make_prediction(model_trained,final_dataset)

        list_mean,list_median,list_std=dataframe_summary(final_dataset)

        list_na_values_perc=check_integrity(final_dataset)

        list_timing=training_timing()

        table_packages=outdated_packages_list()
        

    except Exception as err:
        logger.exception(err)
        raise



def read_data(path):
    """
        Read test data

        Args:
            path(str): path of the file
    """
    try:
        logger.info('START')
        
        df=pd.read_csv(path)
        
        logger.info('shape:{}'.format(df.shape))

        return df
    except Exception as err:
        logger.exception(err)
        raise

def read_model(path):
    """
        Read model

        Args:
            path(str): path of the model
    """
    try:
        logger.info('START')


        model=pickle.load(open(path, 'rb'))
        

        return model
    except Exception as err:
        logger.exception(err)
        raise    

def make_prediction(model, data):
    """
        Thie method runs prediction

        Args:
            model(pickle)
            data(pandas Dataframe)
        Output:
            list_predictions(list): predictions
    """
    try:
        logger.info('START')


        X=data.loc[:,['lastmonth_activity','lastyear_activity','number_of_employees']].values.reshape(-1, 3)
        y=data['exited'].values.reshape(-1, 1)

        list_predictions=model.predict(X)

        logger.info('list_predictions: {}'.format(list_predictions))
        return list_predictions

    except Exception as err:
        logger.info(err)
        raise


##################Function to get summary statistics
def dataframe_summary(df):
    """
    calculate summary statistics here

        Args:
            df(pandas DF)
    """
    try:
        list_mean=list(df.mean())
        list_median=list(df.median())
        list_std=list(df.std())

        logger.info('list_mean: {}, list_median:{}, list_std: {}'.format(list_mean,list_median,list_std))


        return list_mean,list_median,list_std

    except Exception as err:
        logger.exception(err)
        raise



def check_integrity(df):
    
    """
        Check integrity

        Args:
            df(pandas Dataframe)
            
        Output:
            list_means(list): list with na values
    """
    try:
        logger.info('START')
        
        list_na_values=list(df.isnull().sum(axis=0))

        size_df=df.shape[0]

        list_na_values_perc=[item/size_df for item in list_na_values]

        logger.info('list_na_values_perc: {}'.format(list_na_values_perc))

        return list_na_values_perc

    except Exception as err:
        logger.exception(err)
        raise 
 

def training_timing():
    """
    Timing training process

        Output:
            result_list(list): list composed by two value: computation time for ingestion and training process
            
    """
    try:
        logger.info('START')

        result_list=list()


        start_ingestion=timeit.default_timer()
        os.system('python3 src/ingestion/ingestion.py')

        timing_ingestion=timeit.default_timer()-start_ingestion
        logger.info('timing_ingestion: {}'.format(timing_ingestion))

        result_list.append(timing_ingestion)

        start_training=timeit.default_timer()
        os.system('python3 src/training/training.py')

        timing_training=timeit.default_timer()-start_training

        logger.info('timing_training: {}'.format(timing_training))

        result_list.append(timing_training)

        logger.info('SUCCESS')

        return result_list

    except Exception as err:
        logger.exception(err)

def outdated_packages_list():
    """
        Monitor installed packages

        Output:
            df(pandas DF): dataframe with installed packages
    """
    try:
        data = subprocess.check_output(["pip", "list", "--format", "json"])
        parsed_results = json.loads(data)
        table_final=[(element["name"], element["version"]) for element in parsed_results]
        #table_final=[subprocess.check_output(['python','-m','pip', 'show', element["name"]]) for element in parsed_results]

        df=pd.DataFrame(table_final)
        logger.info('df: {}'.format(str(df.head())))

        return df

    except Exception as err:
        logger.exception(err)






    
