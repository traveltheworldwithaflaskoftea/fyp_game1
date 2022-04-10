from json import JSONEncoder
from flask import Flask, jsonify, request, redirect, render_template
from flask_pymongo import PyMongo
from pymongo import ReturnDocument
from utils import JSONEncoder
from flask_cors import CORS
from bson.json_util import dumps
import json

app = Flask(__name__)
CORS(app)
app.config["MONGO_URI"] = "mongodb+srv://fyp1:RacH3nBu9ER2NW2o@clusterfyp.dwacg.mongodb.net/Game1?retryWrites=true&w=majority"
mongo = PyMongo(app)
# Need to make user dynamic !! and save it here 
user = "user1"

@app.route('/test')
def test():
    return "App is working perfectly"

#Index Page Functions 
@app.route('/')
def getAllLifestages():
    try:
        #Use these 2 lines when checking on Postman
        # lifestages = list(mongo.db.lifestage.find())
        # return JSONEncoder().encode(lifestages), 200

        #Use these 2 lines when visualizing on page
        lifestages = list(mongo.db.lifestage.find())
        return render_template("1_index.html", lifestages = lifestages), 200
    except Exception as e: 
        return dumps({'error': str(e)})


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
            print(lifestage, goal_num)
            lifestage_data = mongo.db.lifestage.find_one_or_404({"_id": lifestage})
            goal = lifestage_data["goals"][goal_num]
            values = {
                "lifestage": lifestage, 
                "goal": goal
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
        # return JSONEncoder().encode(user_data), 200
        return render_template("4_result.html", user_data = user_data), 200
    except Exception as e: 
        return dumps({'error': str(e)})

#Recommend Page
@app.route('/recommendation')
def getAllPortfolios(): 
    try:
        portfolios = mongo.db.portfolio.find()
        return render_template("5_rec.html", portfolios = portfolios), 200
    except Exception as e: 
        return dumps({'error': str(e)})

@app.route('/recommendation/<id>')
def getOnePortfolio(id): 
    portfolio = mongo.db.portfolio.find_one_or_404({"_id": id})
    return JSONEncoder().encode(portfolio), 200

if __name__ == '__main__':
    app.run(debug=True)

