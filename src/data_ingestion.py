import os 
import pandas as pd 
from google.cloud import storage
from src.custom_exception import CustomException
from src.loger import get_loger
from utils.custom_utils import read_yaml
from config.path_config import *

logger = get_loger(__name__)

class DataIngestion:
    def __init__(self, config):
        self.config = config["data_ingestion"]
        self.bucket_name = self.config["bucket_name"]
        self.file_names = self.config["bucket_file_names"]

        os.makedirs(RAW_DIR, exist_ok=True)
        logger.info("Data Ingestion Started......")

    def download_csv_from_gcp(self):
        try:
            client = storage.Client()
            bucket = client.bucket(self.bucket_name)

            for file in self.file_names:
                file_path = os.path.join(RAW_DIR, file)

                blob = bucket.blob(file)
                blob.download_to_filename(file_path)

                data = pd.read_csv(file_path)
                data.to_csv(file_path, index=False)
                logger.info("Downloading each csv file in GCP bucket")

        except Exception as e:
            logger.error("Error occured while downloading data csv in DATA INGESTION prosess...")
            raise CustomException("Error occured while downloading data csv in DATA INGESTION prosess", e)
        

    def run(self):
        try:
            logger.info("Starting Data Ingestion Prosess....")
            self.download_csv_from_gcp()
            logger.info("Data Ingestion Completed...")
        except Exception as e:
            logger.error("Error occured in DATA INGESTION prosess.....")
            raise CustomException("Error occured in DATA INGESTION proses", e)
        


################## RUN Data Ingestion ########################
if __name__ == "__main__":
    data_ingestion = DataIngestion(read_yaml(CONFIG_PATH))
    data_ingestion.run()

