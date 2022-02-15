"""
The aim of this module is to score the model


Date: 15th of Feb, 2022
Author: Fabio Barbazza
"""
import pandas as pd
import pickle
import logging
from sklearn.metrics import f1_score

logger=logging.getLogger(__name__) 


#################Function for model scoring
def calculate_score_model(test_data_path,model_path,scoring_model_path):
    """
    The aim of this function is to take a trained model, load test data, and calculate an F1 score for the model relative to the test data
    it should write the result to the latestscore.txt file

        Args:
            test_data_path(str): path of the input data
            model_path(str): path of the model
            scoring_model_path(str): path of the folder to store score
        Output:
            scoring(numpy array)
    """
    try:

        test_data=read_data(test_data_path)

        model_trained=read_model(model_path)

        preds=make_prediction(model_trained,test_data)

        scoring=score_model(preds,test_data)

        store_score(scoring,scoring_model_path)

        return scoring

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
        logging
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

def score_model(preds, original):
    """
        Thie method runs prediction

        Args:
            preds(list)
            original(pandas Dataframe)
    """
    try:
        logger.info('START')

        y_true=original['exited'].values.reshape(-1, 1)

        f1_value=f1_score(y_true, preds)


        logger.info('f1_value: {}'.format(f1_value))

        return f1_value

    except Exception as err:
        logger.info(err)
        raise


def store_score(scoring,scoring_model_path):
    """
        Storing score

        Args:
            scoring(np array)
            scoring_model_path(str)
    """
    try:
        with open(scoring_model_path,'w') as write_score:
            write_score.write(str(scoring))

    except Exception as err:
        logger.exception(err)
        raise