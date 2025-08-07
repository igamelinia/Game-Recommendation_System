import os 
import sys 
from src.loger import get_loger
from src.custom_exception import CustomException
from config.path_config import *
from utils.recomendation_utils import *

logger = get_loger(__name__)

### Function for Give recommendation
def hybrid_recommendation(id, users_weight = 0.5, games_weight=0.5):
    try:
        if isinstance(id, str):
            similar_game_base_content = find_similar_game(id, n=10)
            df = pd.DataFrame(similar_game_base_content, columns=['title', 'date_release', 'support_devices', 'user_reviews', 'rating',
                                'price_final'])
            logger.info("Successed Give Recommendation base on similar Games")
            return df

        if isinstance(id, int):
            name = []
            date_release = []
            support_device = []
            price = []
            rating = [] 

            ### User Base Recommendation
            similar_users = SimilarUser(int(id), n=10)
            user_preferences = UserPreferance( int(id))
            game_recommendation = get_user_recommendation(users_similar= similar_users,
                                                        user_preferences= user_preferences,
                                                        n=10)
            
            user_recommended_game_list = game_recommendation['game_name'].tolist()
            #print(user_recommended_game_list)

            ### Content Base REcommendation

            content_recommendation_game_list = []

            for game in user_recommended_game_list:
                similar_games = find_similar_game(game, n=10)
                
                if similar_games is not None and not similar_games.empty:
                    content_recommendation_game_list.extend(similar_games["title"].tolist())
                else :
                    logger.warning(f"Similar game not found {game}")
                    print(f"Similar game not found {game}")

            
            combine_score = {}

            for game in user_recommended_game_list:
                combine_score[game] = combine_score.get(game, 0) + users_weight

            for game in content_recommendation_game_list:
                combine_score[game] = combine_score.get(game, 0) + games_weight

            sort_combine_score = sorted(combine_score.items() , key=lambda x:x[1] , reverse=True)

            recommendation_game_list = [game for game, score in sort_combine_score[:10]]

            for game in recommendation_game_list:
                if game in game_recommendation["game_name"].values:
                    row = game_recommendation[game_recommendation["game_name"] == game]
                    name.extend(row["game_name"].tolist())
                    date_release.extend(row["date_release"].tolist())
                    support_device.extend(row["devices"].tolist())
                    price.extend(row["price"].tolist())
                    rating.extend(row["rating"].tolist())

                if game in similar_games["title"].values:
                    row = similar_games[similar_games["title"] == game]
                    name.extend(row["title"].tolist())
                    date_release.extend(row["date_release"].tolist())
                    support_device.extend(row["support_devices"].tolist())
                    price.extend(row["price_final"].tolist())
                    rating.extend(row["rating"].tolist())

            df = pd.DataFrame({
                "Name" : name,
                "Date Release" : date_release,
                "Price" : price,
                "Playable" : support_device,
                "Rating" : rating
            })
            logger.info("Successed to Give Recommendation base on Hybrid Recommendation")

            return df
    except Exception as e:
        logger.error("Error occured while search Hybrid Recommendation", e)
        raise CustomException("Error occured while search Hybrid Recommendation", e)