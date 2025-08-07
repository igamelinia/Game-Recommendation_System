import os 
import sys 
from src.loger import get_loger
from src.custom_exception import CustomException
from src.data_preprocessing import DataProcessor
from src.model_training import ModelTraining
from config.path_config import *

logger = get_loger(__name__)

class TrainPipeline():
    def __init__(self):
        pass 
    def run_pipeline(self):
        try:
            data_procees = DataProcessor(RECOMMENDATION_CSV, PROCESSING_DIR)
            data_procees.run()
            model_training = ModelTraining(PROCESSING_DIR)
            model_training.train()
        except Exception as e:
            logger.error("Error occured while run Training Pipeline", e)

if __name__=="__main__":
    train_pipeline = TrainPipeline()
    train_pipeline.run_pipeline()