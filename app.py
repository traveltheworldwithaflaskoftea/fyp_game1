from json import JSONEncoder
from flask import Flask, jsonify, request, redirect, render_template, session, url_for
from flask_pymongo import PyMongo
from pymongo import ReturnDocument
from utils import JSONEncoder
from flask_cors import CORS
from bson.json_util import dumps
import json
import random

app = Flask(__name__)
CORS(app)
app.config["MONGO_URI"] = "mongodb+srv://fyp1:RacH3nBu9ER2NW2o@clusterfyp.dwacg.mongodb.net/Game1?retryWrites=true&w=majority"
mongo = PyMongo(app)
# Need to make user dynamic !! and save it here 
user = "user3"

app.secret_key = "testing"


#Login Page
@app.route('/', methods=['POST', 'GET'])
def login():
    try:
        lifestages = list(mongo.db.lifestage.find())
    except Exception as e: 
        return dumps({'error': str(e)})  

    message = ''
    if "email" in session:
        return redirect(url_for("getAllLifestages"))

    if request.method == "POST":
        #Recording into session
        email = request.form.get("email")

        #check if email exists in database
        user_data = mongo.db.user.find_one({"email": email})
        print(user_data)
        
        if user_data :
            user = user_data["_id"]
            session["user"]= user
            print(session.get("user"))
            # if "email" in session:
            return redirect(url_for("getAllLifestages"))
        else:
            message = 'Email not found/ incorrect'
            return render_template('0_login.html', lifestages= lifestages, message=message)

    return render_template("0_login.html", lifestages = lifestages), 200
    

#Logged In
@app.route('/logged_in')
def logged_in():
    if "email" in session:
        email = session["email"]
        return render_template('1_index.html', email=email)
    else:
        return redirect(url_for('getAllLifestages'))

#Logout
@app.route('/logout', methods=['POST', 'GET'])
def logout():
    return render_template('6_signout.html')

    

#Index Page Functions 
@app.route('/lifestages')
def getAllLifestages():
    try:
        #Use these 2 lines when checking on Postman
        # lifestages = list(mongo.db.lifestage.find())
        # return JSONEncoder().encode(lifestages), 200

        #Use these 2 lines when visualizing on page
        lifestages = list(mongo.db.lifestage.find())
        users = list(mongo.db.user.find())
        return render_template("1_index.html", lifestages = lifestages, users = users), 200
    except Exception as e: 
        return dumps({'error': str(e)})

@app.route('/test')
def test():
    return "App is working perfectly"


#Select goal page
@app.route('/goal')
def getGoals():
    return render_template('2_goal.html'), 200


@app.route('/goal/<id>')
def getOneLifestage(id): 
    try:
        lifestage = mongo.db.lifestage.find_one_or_404({"_id": id})
        return render_template("2_goal.html", lifestage = lifestage), 200
    except Exception as e: 
        return dumps({'error': str(e)})

#Receive and Store goal for user
@app.route('/saveGoal', methods=['POST'])
def saveGoal():
    # Simple check of input format and data of the request are JSON
    if request.is_json:
        try:
            result = request.get_json()
            print("\nReceived result in JSON:",
                  result)
            lifestage = result["lifestage"]
            goal_num = result["goal"]
            #print(lifestage, goal_num)
            # lifestage_data = mongo.db.lifestage.find_one_or_404({"_id": lifestage})
            # goal = lifestage_data["goals"][goal_num]
            values = {
                "lifestage": lifestage, 
                "goal": goal_num
            }
            
            data = mongo.db.user.find_one_and_update(
                {"_id": user},
                {"$set": values},
                return_document=ReturnDocument.AFTER,
            )
            return JSONEncoder().encode(data), 200

        except Exception as e:
            return jsonify({
                "code": 404,
                "message": str(e)
            }), 404

    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data()),
        "test": str(request.is_json)
    }), 400


#Questionaire page 
@app.route('/questionnaire')
def getAllQuestions(): 
    try:
        questions = list(mongo.db.questionaire.find())
        return render_template("3_questionnaire.html", questions = questions), 200

        #Check for correct extraction from DB
        # questions = list(mongo.db.questionaire.find())
        # return JSONEncoder().encode(questions), 200
    except Exception as e: 
        return dumps({'error': str(e)})

#Receive and Store risk tolerance & sustainability indication
@app.route('/storeResult', methods=['POST'])
def storeResult():
    # Simple check of input format and data of the request are JSON
    if request.is_json:
        try:
            result = request.get_json()
            print("\nReceived result in JSON:",
                  result)
            data = mongo.db.user.find_one_and_update(
                {"_id": user},
                {"$set": result},
                return_document=ReturnDocument.AFTER,
            )
            return JSONEncoder().encode(data), 200

        except Exception as e:
            return jsonify({
                "code": 404,
                "message": str(e)
            }), 404

    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data()),
        "test": str(request.is_json)
    }), 400

#Tolerance Page 
@app.route('/result')
def getResult(): 
    try:
        user_data = mongo.db.user.find_one_or_404({"_id": user})
        lifestage = user_data["lifestage"]
        risk = user_data["risk"]
        risk_data = mongo.db.byrisk.find_one_or_404({"_id": risk})
        percentage = risk_data["def"]
        print(percentage)

        lifestage_data = mongo.db.lifestage.find_one_or_404({"_id": lifestage})
        img = lifestage_data["img"]
        name = lifestage_data["name"]
        #print(img, name)
        # return JSONEncoder().encode(user_data), 200
        return render_template("4_result.html", user_data = user_data, name = name, img = img, percentage = percentage), 200
    except Exception as e: 
        return dumps({'error': str(e)})

#Recommendation Page
@app.route('/recommendation')
def getRecommendation():
    try:
        #1. Get goal num , interest in sustainability & risk
        user_data = mongo.db.user.find_one_or_404({"_id": user})
        lifestage = user_data["lifestage"]
        goal = user_data["goal"]
        sustainability = user_data["sustainability"]
        risk = user_data["risk"]
        if str(sustainability) == "are":
            sustainability = "s"
        else: 
            sustainability = "ns"
        #print(goal,sustainability, lifestage, risk)

        #2. Get mapping & fund source
        mappings = mongo.db.mappings.find_one_or_404({"_id": lifestage})
        mapping = mappings[goal]["rec"]
        source = mappings[goal]["source"]
        reason = mappings[goal]["reason"]
        #print(mapping, source)

        #3. Get portfolio category array according to sustainability 
        recommendations = mongo.db.recommendations.find_one_or_404({"_id": mapping})
        rec = recommendations["rec"][sustainability]
        # print(rec)

        #4. Get specific portfolio _id in an array
        portfolioIDs = [] 
        portfolios = mongo.db.byrisk.find_one_or_404({"_id": risk})

        #Function: Choose random portfolio ID  
        def randomPortfolio(item):
            portfolioByCategory = portfolios[item]
            chosenPortfolio = random.choice(tuple(portfolioByCategory))
            portfolioIDs.append(chosenPortfolio)

        #Checking for flagship duplicates
        if rec.count("flagship") > 1: 
            for i in portfolios["flagship"]: 
                portfolioIDs.append(i)
            randomPortfolio(rec[2])
        elif rec.count("esg") > 1: 
            for i in portfolios["esg"]: 
                portfolioIDs.append(i)
            randomPortfolio(rec[2])
        else: 
            for item in rec: 
                randomPortfolio(item)
        #print(rec)
        print(portfolioIDs)

        #Save the recommendations in DB
        mongo.db.user.find_one_and_update(
                {"_id": user},
                {"$set": {"recommendations": portfolioIDs}},
                return_document=ReturnDocument.AFTER,
        )
       

        #5. Return portfolios to be visualised 
        portfolioFile = []
        for id in portfolioIDs:    
            recSources = [] 
            finalRecommend = mongo.db.portfolio.find_one_or_404({"_id": id})
            for i in source: 
                if i in finalRecommend["source"]: 
                    recSources.append(i)
            print("list:", recSources)
            recSources = ",".join(recSources)
            print("string:",  recSources)
            finalRecommend["source"] = recSources
            portfolioFile.append(finalRecommend)
        #print(portfolioFile)
        return render_template("5_rec.html", portfolioFile = portfolioFile, reason = reason), 200

    except Exception as e: 
        return dumps({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)

