from utils.recomendation_utils import GetGameName, GetGameDetail, find_similar_game, SimilarUser, UserPreferance, get_user_recommendation, search_keyword
from config.path_config import *
from pipeline.predict_pipeline import hybrid_recommendation

game_name = GetGameName(460930)
#print(game_name)

game_detail = GetGameDetail(460930)
#print(game_detail)

#game_similar = find_similar_game("Honkai Impact 3rd", n=10)
#print(game_similar)

#users_similar = SimilarUser(int(11764552), n=10)
#print(users_similar)

#user_preferences = UserPreferance( int(11764552))
#print(user_preferences)

#user_recommendation = get_user_recommendation(users_similar= users_similar,
#                        user_preferences= user_preferences,
#                        n=10)
#print(user_recommendation)

#Recommendation_by_hybrid = hybrid_recommendation(11764552)
#print(f"Hybrid Recommenation : {Recommendation_by_hybrid}")

#Recommendation_by_similar_game = hybrid_recommendation("Honkai Impact 3rd")
#print(f"Content Recommenation : {Recommendation_by_similar_game}")

print(search_keyword("Honkai"))