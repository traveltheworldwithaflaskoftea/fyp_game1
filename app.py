from json import JSONEncoder
from flask import Flask, jsonify, request, redirect, render_template
from flask_pymongo import PyMongo
from flask_cors import CORS
from bson.json_util import dumps
import json

app = Flask(__name__)
CORS(app)
app.config["MONGO_URI"] = "mongodb+srv://fyp1:RacH3nBu9ER2NW2o@clusterfyp.dwacg.mongodb.net/Game1?retryWrites=true&w=majority"
mongo = PyMongo(app)

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
        lifestages = mongo.db.lifestage.find()
        return render_template("1_index.html", lifestages = lifestages), 200
    except Exception as e: 
        return dumps({'error': str(e)})


#Select goal page
@app.route('/goal')
def goalsPage():
    return render_template('2_goal.html'), 200

@app.route('/goal/<id>')
def getOneLifestage(id): 
    try:
        lifestage = mongo.db.lifestage.find_one_or_404({"_id": id})
        return render_template("2_goal.html", lifestage = lifestage), 200
        #return JSONEncoder().encode(goals), 200
    except Exception as e: 
        return dumps({'error': str(e)})

#Questionaire page 
@app.route('/questionaire')
def getAllQuestions(): 
    try:
        questions = mongo.db.questionaire.find()
        return render_template("3_questionaire.html", questions = questions), 200

        #Check for correct extraction from DB
        # questions = list(mongo.db.questionaire.find())
        # return JSONEncoder().encode(questions), 200
    except Exception as e: 
        return dumps({'error': str(e)})

#Tolerance Page 
@app.route('/tolerance')
def resultsPage(): 
    return render_template('4_result.html'), 200

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

