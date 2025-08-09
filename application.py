from flask import Flask, render_template, request
from pipeline.predict_pipeline import hybrid_recommendation
from utils.recomendation_utils import search_keyword
from config.path_config import *

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/personal", methods=["GET", "POST"])
def personal():
    recommendations = None
    names_list = None
    game_name = ""
    keyword = ""
    if request.method == "POST" :
        try:
            keyword = str(request.form.get('keyword', ""))
            game_name = str(request.form.get("game_name", "").strip())

            if keyword and not game_name :
                df_keyword = search_keyword(keyword)
                if not df_keyword.empty:
                    names_list = df_keyword.to_dict(orient="records")

            
            if game_name:
                df = hybrid_recommendation(game_name)

                # Convert DataFrame to list of dict
                recommendations = df.to_dict(orient="records")
        
        except Exception as e:
            print("Error occured while Personal Recommendation..")

    return render_template('content_recommend.html', 
                           recommendations=recommendations,
                            game_name=game_name, 
                            names_list=names_list,
                            keyword=keyword)

@app.route("/members", methods=["GET", "POST"])
def members():
    recommendations = None
    userid = None
    
    if request.method == "POST" :
        try:
            userid = int(request.form["userid"])
            df = hybrid_recommendation(userid)
            recommendations = df.to_dict(orient="records")
        except Exception as e :
            print("Error occured while Personal Recommendation..")

    return render_template('hybrid_recommend.html',
                           recommendations = recommendations,
                           userid=userid)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0',port=5000)