import os 
import sys 
import pandas as pd
import numpy as np
import joblib
from src.loger import get_loger
from src.custom_exception import CustomException
from config.path_config import *

logger = get_loger(__name__)

############################ FUNCTION FOR RECOMENDATION SYSTEM ###########################################
def GetGameName(game_id):
    try:
        game_df = pd.read_csv(GAMES_DF)
        name = game_df.loc[game_df["app_id"] == game_id].title.values[0]
        if name is np.nan:
            print(f"There is no Game with game id : {game_id}")

        logger.info("Successed to get Game Name")
        return name                                                 
    except Exception as e:
        logger.error(f"Error to get Name of Game : {e}")
        raise CustomException(f"Error to get Name of Game : {e}")
    

def GetGameDetail(game):
    try:
        df = pd.read_csv(GAMES_DF)
        if isinstance(game, int):
            return df[df.app_id == game]
        if isinstance(game, str):
            return df[df.title == game]
        logger.info("Successed to get Game Detail")
    except Exception as e:
        logger.error(f"Error to get Game Detail : {e}")
        raise CustomException(f"Error to get Game Detail : {e}")
    
# Function to get similar games
def find_similar_game(name, n=10,  return_dist=False, neg=False):
    try :
        game_weight=joblib.load(GAMES_WEIGHT)
        app_decode=joblib.load(GAME_DECODED)
        app_encode=joblib.load(GAME_ENCODED)

        # get Game Id from game name
        indx = GetGameDetail(name).app_id.values[0]
        encoded_index = app_encode.get(indx)

        if encoded_index is None :
            print(f"Encode {name} is not found in Game ID : {indx}")

        weight = game_weight
        #weight_index = weight[encoded_index[0]]

        # Evaluate similiarity
        dist = np.dot(weight, weight[encoded_index])
        sorted_dist = np.argsort(dist) # sort from small to big

        n = n + 1

        if neg == True:
            closest = sorted_dist[:n]

        else:
            closest = sorted_dist[-n:]

        # return Dist and closest if true
        if return_dist:
            return dist, closest
        
        # Return result
        results = []
        
        for close in closest:
            decoded_index = app_decode.get(close)

            game_detail = GetGameDetail(decoded_index)
            similarity = dist[close]
            game_detail["similarity_score"] = similarity

            results.append(game_detail)

            result_df = pd.concat(results, ignore_index=True).sort_values(by='similarity_score', ascending=False).reset_index(drop=True)
            logger.info("Successed to get similar game......")
        return result_df[result_df.app_id != indx].drop(['app_id'], axis=1)
    
    except Exception as e:
        logger.error(f"Error to get similar Game : {e}")
        raise CustomException(f"Error to get similar Game : {e}")
    

# Function for get similar users
def SimilarUser(user, n=10, return_dist=False, neg=False):
    try:
        user_weight = joblib.load(USERS_WEIGHT)
        user_encoded = joblib.load(USER_ENCODED)
        user_decoded = joblib.load(USER_DECODED)

        # function
        index = user
        encode_user = user_encoded.get(index)
        weight = user_weight
        dists = np.dot(weight, weight[encode_user])
        soreted_dists = np.argsort(dists)

        n = n + 1

        if neg:
            closest = soreted_dists[:n]
        else:
            closest = soreted_dists[-n:]

        if return_dist:
            return dists, closest

        result = [] 

        for close in closest:
            similarity = dists[close]

            if isinstance(user, int):
                decode_index = user_decoded.get(close)
                result.append({
                    "user" : decode_index,
                    "similarity_score" : similarity
                })

        similar_users = pd.DataFrame(result).sort_values(by="similarity_score", ascending=False)
        similar_users = similar_users[similar_users.user != user]
        logger.info("Successed to get similar users....")
        return similar_users
            
    except Exception as e:
        logger.error("Error while search similar Usesr", e)
        raise CustomException("Error while search similar Users", e)
    

#Function for get user preference
def UserPreferance(user):
    try:
        game_df = pd.read_csv(GAMES_DF)
        recommendation_df = pd.read_csv(RECOMMEND_DF)
        games_played_by_user = recommendation_df[recommendation_df.user_id == user]
        games_recommended_by_user = games_played_by_user[games_played_by_user.is_recommended == 1]
        #games_not_recommend_by_user = games_played_by_user[games_played_by_user.is_recommended == 0]
        games_frame =  pd.merge(games_recommended_by_user, game_df, on="app_id", how="left")
        game_percentile = np.percentile(games_frame.user_reviews, 75) 
        games_most_reviews = games_frame[games_frame.user_reviews >= game_percentile]
        top_games_by_user = games_most_reviews.sort_values(by="user_reviews", ascending=False).drop(columns='index', axis=1)
        top_games_by_user = top_games_by_user[['title', 'date_release', 'support_devices', 'user_reviews',
        'rating', 'price_final']]
        
        logger.info("Successed to get Users Preference")
        return top_games_by_user
    except Exception as e:
        logger.error("Error while search Users Preference", e)
        raise CustomException("Error while search Users Preference", e)
    
# Function for get user recommendation
def get_user_recommendation(users_similar, user_preferences, n=10):
    try:
        recommended_games = []
        games_list = []

        # Get preference of each similar user
        for user in users_similar.user.values:
            pref_list = UserPreferance(int(user))
            pref_list = pref_list[~pref_list.title.isin(user_preferences.title.values)]

            if not pref_list.empty:
                games_list.append(pref_list.title.values)

        if games_list:
            games_list = pd.DataFrame(games_list)
            sorted_list = pd.DataFrame(pd.Series(games_list.values.ravel()).value_counts()).head(n)

            for i, game_name in enumerate(sorted_list.index):
                n_users_pref = sorted_list[sorted_list.index == game_name].values[0][0]

                if isinstance(game_name, str):
                    frame = GetGameDetail(game_name)
                    date_release = frame.date_release.values[0]
                    devices = frame.support_devices.values[0]
                    rating = frame.rating.values[0]
                    price = frame.price_final.values[0]


                    recommended_games.append({
                            "n" : n_users_pref,
                            "game_name" : game_name,
                            "date_release" : date_release,
                            "devices": devices,
                            "rating" : rating,
                            "price" : price
                        })
        logger.info("Successed for search Recommendation Base on User")
        return pd.DataFrame(recommended_games).head(n)

    except Exception as e:
        logger.error("Error while search Recommendation base on User", e)
        raise CustomException("Error while search Recommendation base on User", e)
    
def search_keyword(game_name):
    try:
        game_df = pd.read_csv(GAMES_DF)
        keyword = str(game_name).strip()

        result = game_df[game_df['title'].str.strip().str.contains(keyword, case=False, na=False)]
        return result
    except Exception as e:
        logger.error("Error while search keyword", e)
        raise CustomException("Error while Search Keyword name", e)