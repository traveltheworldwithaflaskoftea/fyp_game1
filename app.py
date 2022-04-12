from json import JSONEncoder
from flask import Flask, jsonify, request, url_for, redirect, render_template, json, session
from flask_pymongo import PyMongo
from flask_cors import CORS
from bson.json_util import dumps
import json


app = Flask(__name__)
CORS(app)
app.config["MONGO_URI"] = "mongodb+srv://fyp1:RacH3nBu9ER2NW2o@clusterfyp.dwacg.mongodb.net/Game1?retryWrites=true&w=majority"
mongo = PyMongo(app)

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
    # if "email" in session:
    #     session.pop("email", None)
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
        #return JSONEncoder().encode(goals), 200
    except Exception as e: 
        return dumps({'error': str(e)})

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

#Tolerance Page 
@app.route('/result')
def getResult(): 
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

