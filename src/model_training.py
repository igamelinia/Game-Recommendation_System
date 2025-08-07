import os 
import sys 
import numpy as np 
import joblib
from sklearn.utils import class_weight
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping, LearningRateScheduler
from src.loger import get_loger
from src.custom_exception import CustomException
from src.base_model import BaseModel
from config.path_config import *

import mlflow
import mlflow.tensorflow
from mlflow.models import infer_signature

logger = get_loger(__name__)

class ModelTraining():
    def __init__(self, data_process_path):
        self.data_path = data_process_path

    def load_data(self):
        try:
            X_train_array = joblib.load(X_TRAIN_ARRAY)
            X_test_array = joblib.load(X_TEST_ARRAY)
            y_train = joblib.load(Y_TRAIN)
            y_test = joblib.load(Y_TEST)

            logger.info("Load Data for Model Training is success")
            return X_train_array, X_test_array, y_train, y_test
            
        except Exception as e:
            raise CustomException("Error occured while load data in Model Training Step", e)

    def train(self):
        try:
            mlflow.set_tracking_uri("http://127.0.0.1:5000")
            mlflow.set_experiment("Game_Recommendation_model")

            # Activate autolog for tensorflow
            mlflow.tensorflow.autolog(log_models=True)

            with mlflow.start_run():
                X_train_array, X_test_array, y_train, y_test = self.load_data()
                n_users = len(joblib.load(USER_ENCODED))
                n_games = len(joblib.load(GAME_ENCODED))

                base_model = BaseModel(config_path=CONFIG_PATH)
                model = base_model.RecomendationNN(n_users=n_users, n_games=n_games)
                class_weights_dict = self.define_class_weight(y_train)

                # Function for search LR
                start_lr = 0.00001
                min_lr = 0.0001
                max_lr = 0.00005
                batch_size = 10000

                ramup_epochs = 5
                sustain_epochs = 0
                exp_decay = 0.8

                def lrfn(epoch):
                    if epoch<ramup_epochs:
                        return (max_lr-start_lr)/ramup_epochs*epoch + start_lr
                    elif epoch<ramup_epochs+sustain_epochs:
                        return max_lr
                    else:
                        return (max_lr-min_lr) * exp_decay ** (epoch-ramup_epochs-sustain_epochs)+min_lr
                    
                # Define Callbacks

                lr_callback = LearningRateScheduler(lambda epoch : lrfn(epoch), verbose=1)
                checkpoint_callback = ModelCheckpoint(filepath=CHECKPOINT_FILE_PATH,
                                                    monitor="val_loss",
                                                    mode="min",
                                                    save_weights_only=True,
                                                    save_best_only=True)
                
                stop_callback = EarlyStopping(patience=3, monitor="val_loss", mode="min", restore_best_weights=True )
                callbacks_list = [lr_callback, checkpoint_callback, stop_callback]

                os.makedirs(os.path.dirname(CHECKPOINT_FILE_PATH), exist_ok=True)
                os.makedirs(MODEL_DIR, exist_ok=True)
                os.makedirs(WEIGHTS_DIR, exist_ok=True)

                try :
                    history = model.fit(
                    x=X_train_array,
                    y=y_train,
                    batch_size=batch_size, 
                    epochs=32,  
                    verbose=1,
                    validation_data=(X_test_array,y_test),
                    class_weight=class_weights_dict,
                    callbacks=callbacks_list
                    )

                    model.load_weights(CHECKPOINT_FILE_PATH)
                    logger.info("Model Train is completed")

                except Exception as e :
                    raise CustomException("Model Training is fail ...", e)

                self.save_model_weights(model)

                mlflow.log_artifact(USERS_WEIGHT, artifact_path="weights")
                mlflow.log_artifact(GAMES_WEIGHT,  artifact_path="weights")
                mlflow.log_param("n_users", n_users)
                mlflow.log_param("n_games", n_games)
                mlflow.log_param("Batch_size", batch_size)
                mlflow.log_param("epochs", 32)
                mlflow.log_artifact(X_TRAIN_ARRAY, artifact_path="dataset")
                mlflow.log_artifact(X_TEST_ARRAY, artifact_path="dataset")
                mlflow.log_artifact(Y_TRAIN, artifact_path="dataset")
                mlflow.log_artifact(Y_TEST, artifact_path="dataset")

        except Exception as e:
            raise CustomException("Error occured while training model", e)
        
    def define_class_weight(self, y_train):
        try:
            class_weights = class_weight.compute_class_weight(
                            class_weight="balanced",
                            classes=np.unique(y_train),
                            y=y_train

                        )

            class_weights_dict = dict(zip(np.unique(y_train), class_weights))
            return class_weights_dict
                        
        except Exception as e:
            raise CustomException("Error occured while define weighth for class target",e)
    
    def extract_weight(self, layer_name, model):
        try:
            layer_weight = model.get_layer(layer_name)
            weight = layer_weight.get_weights()[0]
            weight = weight/np.linalg.norm(weight, axis=1).reshape((-1,1))
            logger.info(f"Extract weights for layer : {layer_name}")
            return weight
        except Exception as e :
            raise CustomException("Error occured while extract weight of layer",e)
    
    def save_model_weights(self, model):
        try:
            model.save(MODEL_PATH)
            logger.info(f"Model has saved in {MODEL_PATH}")

            user_weight = self.extract_weight("user_embedding", model)
            game_weight = self.extract_weight("game_embedding", model)
            joblib.dump(user_weight, USERS_WEIGHT)
            joblib.dump(game_weight, GAMES_WEIGHT)
            logger.info("Save Model Weight is success")

        except Exception as e:
            raise CustomException("Error occured while save weight model", e)


if __name__=="__main__":
    model_training = ModelTraining(PROCESSING_DIR)
    model_training.train()

