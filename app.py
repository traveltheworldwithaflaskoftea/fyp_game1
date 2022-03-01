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

@app.route('/')
def firstpage():
    return render_template('pick_char.html')

@app.route('/recommendation')
def getAllPortfolios(): 
    try:
        portfolios = mongo.db.portfolio.find()
        return render_template("recommend.html", portfolios = portfolios), 200
    except Exception as e: 
        return dumps({'error': str(e)})

@app.route('/recommendation/<id>')
def getOnePortfolio(id): 
    try:
        portfolio = mongo.db.portfolio.find_one_or_404({"_id": id})
        return render_template("recommend.html", portfolio = portfolio), 200
    except Exception as e: 
        return dumps({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)

