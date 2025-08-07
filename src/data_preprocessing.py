import os 
import pandas as pd 
import numpy as np 
import joblib
from src.loger import get_loger
from src.custom_exception import CustomException
from config.path_config import *
import sys 

logger = get_loger(__name__)

class DataProcessor:
    def __init__(self, input_file, output_dir):
        self.input_file = input_file
        self.output_dir = output_dir

        self.recommendation_df = None
        self.game_df = None
        self.X_train_array = None
        self.X_test_array = None 
        self.y_train = None 
        self.y_test = None 

        self.user_encoded = {}
        self.user_decoded = {}
        self.game_encoded = {}
        self.game_decoded = {}

        os.makedirs(self.output_dir, exist_ok=True)
        logger.info("Initiate Data Processing ....")

    staticmethod
    def load_file_csv(self, cols):
        try:
            # Read recommednadtion.csv
            self.recommendation_df = pd.read_csv(self.input_file, low_memory=True, usecols=cols)
            # Create column user count
            user_counts = self.recommendation_df["user_id"].value_counts()
            self.recommendation_df["user_count"] = self.recommendation_df["user_id"].map(user_counts)
            # Read game.csv
            self.game_df = pd.read_csv(GAMES_CSV, low_memory=True)
            logger.info("Data load successed for in Data Processed Step")
            
        except Exception as e:
            raise CustomException("Failed to load file csv in Data Processing Step", e)
        
    def remove_duplicated(self):
        try:
            self.recommendation_df.drop_duplicates(subset=["app_id", "user_id"], keep="last", inplace=True)
            logger.info("Remove Duplicate is success")
        except Exception as e:
            raise CustomException("Failed while remove the data duplicate in Data Processing Step", e)
        

    def filter_users(self, user_threshold=USER_THRESHOLD):
        try:
            self.recommendation_df = self.recommendation_df.loc[self.recommendation_df["user_count"]>=user_threshold]
            logger.info("Filter user that has given review at least for 100 games is success")
        except Exception as e:
            raise CustomException("Failed while filter user that has given review at least 100 games in Data Processing Step")
        
    def encode_target_column(self):
        try:
            self.recommendation_df["is_recommended"] = self.recommendation_df['is_recommended'].apply(lambda x: 1 if x == True else 0)
            logger.info("Encode target column is success")
        except Exception as e:
            raise CustomException("Failed while encode target column be 1 (is_recommended) and 0 (not_recommended) in Data Processing Step", e)
        
    def encoded_decoded_fetures(self):
        try:
            # USer Encode and Decode
            list_users = self.recommendation_df["user_id"].unique().tolist()
            self.user_encoded = {x : i for i, x in enumerate(list_users)}
            self.user_decoded = {i : x for i, x in enumerate(list_users)}
            self.recommendation_df["user"] = self.recommendation_df["user_id"].map(self.user_encoded)

            # Game Encode and Decode 
            list_apps = self.recommendation_df['app_id'].unique().tolist()
            self.game_encoded = {x : i for i, x in enumerate(list_apps)}
            self.game_decoded = {i : x for i, x in enumerate(list_apps)}
            self.recommendation_df['app'] = self.recommendation_df['app_id'].map(self.game_encoded)
            logger.info("Encode and Decode feature columns is success")
        except Exception as e:
            raise CustomException("Failed while encode and decoded features column in Data Processing Step", e)
        
    def Split_data(self, test_size = TEST_SIZE, random_state=42):
        try:
            # shuffle recommendation_df
            self.recommendation_df = self.recommendation_df.sample(frac=1, random_state=42).reset_index()

            X = self.recommendation_df[["user", "app"]].values
            y = self.recommendation_df["is_recommended"]

            train_size = self.recommendation_df.shape[0] - test_size

            X_train, X_test, y_train, y_test = (
                                                    X[:train_size],
                                                    X[train_size:],
                                                    y[:train_size],
                                                    y[train_size:]
                                                )
            
            self.X_train_array = [X_train[: , 0] , X_train[: ,1]]
            self.X_test_array = [X_test[: , 0] , X_test[: ,1]]
            self.y_train = y_train
            self.y_test = y_test
            logger.info("Split Data into Train and Test is success")
        except Exception as e:
            raise CustomException("Failed while Split data into Train and Test in Data Processing Step", e)
        
    def support_devices(self, cols = ['win', 'mac', 'linux']):
        try:
            devices = []
            for idx, row in self.game_df.iterrows():
                device = ", ".join([col for col in cols if row[col] == True])
                devices.append(device)
            self.game_df["support_devices"] = devices

            # Filter Columns that i wanna use
            self.game_df = self.game_df[['app_id', 'title', 'date_release', 'support_devices', 'user_reviews', 'rating', 'price_final']]

            logger.info("Create column Support Devices is success")
        except Exception as e:
            raise CustomException("Failed while create column Support Device on game_df in Data Processing Step", e)

    def save_artifacts(self):
        try:
            # Save Processed Datafame
            self.game_df.to_csv(GAMES_DF, index=False)
            self.recommendation_df.to_csv(RECOMMEND_DF, index=False)

            # Save Encode and Decode
            joblib.dump(self.user_encoded, USER_ENCODED)
            joblib.dump(self.user_decoded, USER_DECODED)
            joblib.dump(self.game_encoded, GAME_ENCODED)
            joblib.dump(self.game_decoded, GAME_DECODED)

            # Save Train and test array
            joblib.dump(self.X_train_array, X_TRAIN_ARRAY)
            joblib.dump(self.X_test_array, X_TEST_ARRAY)
            joblib.dump(self.y_train, Y_TRAIN)
            joblib.dump(self.y_test, Y_TEST)

            logger.info("Save Artifacts is success")

        except Exception as e:
            raise CustomException("Failed while save artifact in Data Processing Step")
        

    def run(self):
        try:
            self.load_file_csv(cols=["app_id", "user_id", "is_recommended"])
            self.remove_duplicated()
            self.filter_users()
            self.encode_target_column()
            self.encoded_decoded_fetures()
            self.Split_data()
            self.support_devices()
            self.save_artifacts()

            logger.info("Data Processing has successed")
        except Exception as e:
            logger.error("Error accured while do Data Processing", str(e))


if __name__ == "__main__":
    data_procees = DataProcessor(RECOMMENDATION_CSV, PROCESSING_DIR)
    data_procees.run()
            
