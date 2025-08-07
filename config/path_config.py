import os 

################################### DATA INGESTION ###########################
RAW_DIR = "artifacts/raw"
CONFIG_PATH = "config/config.yaml"

################################## DATA PREPOCESSING ##########################
PROCESSING_DIR = "artifacts/processed"
RECOMMENDATION_CSV = "artifacts/raw/recommendations.csv"
GAMES_CSV = "artifacts/raw/games.csv"
USER_THRESHOLD = 100
TEST_SIZE = 1000


X_TRAIN_ARRAY = os.path.join(PROCESSING_DIR, "X_train_array.pkl")
X_TEST_ARRAY = os.path.join(PROCESSING_DIR, "X_test_array.pkl")
Y_TRAIN = os.path.join(PROCESSING_DIR, "y_train.pkl")
Y_TEST = os.path.join(PROCESSING_DIR, "y_test.pkl")

RECOMMEND_DF = os.path.join(PROCESSING_DIR, "recommendation_df.csv")
GAMES_DF = os.path.join(PROCESSING_DIR, "game_df.csv")

USER_ENCODED = os.path.join(PROCESSING_DIR, "user_encoded.pkl")
USER_DECODED = os.path.join(PROCESSING_DIR, "user_decoded.pkl")

GAME_ENCODED = os.path.join(PROCESSING_DIR, "app_encoded.pkl")
GAME_DECODED = os.path.join(PROCESSING_DIR, "app_decoded.pkl")

################################# TRAIN MODEL ###################################
MODEL_DIR = "artifacts/model"
WEIGHTS_DIR = "artifacts/weights"
MODEL_PATH = os.path.join(MODEL_DIR, 'RecommendationNN.h5')
USERS_WEIGHT = os.path.join(WEIGHTS_DIR, 'users_weight.pkl')
GAMES_WEIGHT = os.path.join(WEIGHTS_DIR, 'games_weight.pkl')
CHECKPOINT_FILE_PATH = "artifacts/model_checkpoint/weight.weights.h5"

