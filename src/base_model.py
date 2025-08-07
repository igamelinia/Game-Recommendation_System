import os 
import sys 
import tensorflow as tf
from tensorflow.keras import layers
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.layers import Activation, BatchNormalization, Input, Embedding, Dot, Dense, Flatten


from src.loger import get_loger
from src.custom_exception import CustomException
from config.path_config import *
from utils.custom_utils import read_yaml, recall_score, precision_score, f1

logger = get_loger(__name__)

class BaseModel:
    def __init__(self, config_path):
        self.config = read_yaml(config_path)
        logger.info("Initiate Create Base Model..... ")

    def RecomendationNN(self, n_users, n_games):
        try:
            embedded_size = self.config['base_model']['embedding_size']
            loss = self.config['base_model']['loss']
            optimizer = self.config['base_model']['optimizer']

            # User Input and Embedding
            user = Input(name="user_input", shape=[1])
            user_embedding = Embedding(name="user_embedding", input_dim=n_users, output_dim=embedded_size)(user)

            # Game_id Input and Embedding
            game = Input(name="game_input", shape=[1])
            game_embedding = Embedding(name="game_embedding", input_dim=n_games, output_dim=embedded_size)(game)

            # Dot and Flatten
            X = Dot(name="dot_product", axes=2, normalize=True)([user_embedding, game_embedding]) 
            X = Flatten()(X)

            # NN
            X = Dense(1, kernel_initializer="he_normal")(X)
            X = BatchNormalization()(X)
            X = Activation("sigmoid")(X)

            model = Model(inputs=[user, game], outputs=X)
            model.compile(loss=loss,metrics=["accuracy", f1, precision_score, recall_score],optimizer=optimizer)

            logger.info("Create RecommendationNN is success.....")
            return model
        except Exception as e:
            raise CustomException("Failed while Create Base Model RecommendationNN", e)
   


