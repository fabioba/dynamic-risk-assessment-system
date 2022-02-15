"""
The aim of this module is to make reporting


Date: 15th of Feb, 2022
Author: Fabio Barbazza
"""
import pickle
import pandas as pd
import numpy as np
from sklearn import metrics
import matplotlib.pyplot as plt
import seaborn as sns
import json
import os
import logging
from sklearn.metrics import confusion_matrix
from sklearn.metrics import plot_confusion_matrix
import matplotlib.pyplot as plt


logger=logging.getLogger(__name__) 




##############Function for reporting
def score_model(test_data_path,model_path,confusion_matrix_path,read_data,read_model):
    """
    calculate a confusion matrix using the test data and the deployed model
    write the confusion matrix to the workspace

        Args:  
            test_data_path(str)
            model_path(str)
            confusion_matrix_path(str)
            read_data(function)
            read_model(function)
    """
    try:

        logger.info('START')

        model_trained=read_model(model_path)

        data=read_data(test_data_path)


        store_confusion_matrix(model_trained,data,confusion_matrix_path)

    except Exception as err:
        logger.exception(err)
        raise



def store_confusion_matrix(model_trained,data,path_plot):
    """
        Store plot

        Args:
            model_trained(pickle)
            data(pandas DF)
            path_plot(str)

    """
    try:
        plot_confusion_matrix(model_trained, data.loc[:,['lastmonth_activity','lastyear_activity','number_of_employees']].values.reshape(-1, 3), data['exited'].values.reshape(-1, 1))
        
        plt.savefig(path_plot)

        #with open(path_plot) as handler:
        #    handler.write(conf_matr)

        logger.info('SUCCESS')

    except Exception as err:
        logger.exception(err)
        raise


if __name__ == '__main__':
    score_model()
