import os 
import pandas as pd
import yaml
import numpy as np
import tensorflow as tf
from tensorflow.keras import backend as K
from src.loger import get_loger
from src.custom_exception import CustomException

logger = get_loger(__name__)

################### Function read yaml file
def read_yaml(file_path):
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"There is no YAML file in PATH")
        
        with open(file_path, "r") as yaml_file:
            file = yaml.safe_load(yaml_file)
            logger.info("Succesfully read the YAML file")
            return file

    except Exception as e:
        logger.error("Error while reading YAML file....")
        raise CustomException("Failed to read YAML file", e)
    

## Create custom function to recall, precision, and f1-score 
def recall_score(y_true, y_pred):
    try:
        y_true = K.cast(y_true, tf.float32)
        y_pred = K.cast(y_pred, tf.float32)
        true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
        possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
        recall = true_positives / (possible_positives + K.epsilon())
        return recall
    except Exception as e:
        logger.error("Error occured while calculate Recall Score")
        raise CustomException("Failed to calculate Recall Score", e)

def precision_score(y_true, y_pred):
    try:
        y_true = K.cast(y_true, tf.float32)
        y_pred = K.cast(y_pred, tf.float32)
        true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
        predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
        precision = true_positives / (predicted_positives + K.epsilon())
        return precision
    except Exception as e:
        logger.error("Error occured while calculate Precision Score")
        raise CustomException("Failed to calculate Precision Score", e)

def f1(y_true, y_pred):
    try:
        y_true = K.cast(y_true, tf.float32)
        y_pred = K.cast(y_pred, tf.float32)
        precision = precision_score(y_true, y_pred)
        recall = recall_score(y_true, y_pred)
        return 2*((precision*recall)/(precision+recall+K.epsilon()))
    except Exception as e:
        logger.error("Error occured while calculate F1 Score")
        raise CustomException("Failed to calculate F1 Score", e)
