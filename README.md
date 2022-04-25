# 🧍 Solution 1 - Portfolio Recommender
[FYP Project] Gamifying Financial Literacy

## Project Tools
- [Notion](https://www.notion.so/ng-pei-ming-jessie/846cc0d09da74884a65581b2b1b7fc0b?v=55f27f5d83094e9484e1b6ef67bdcb02), our home page for the project
- [GitHub](https://github.com/traveltheworldwithaflaskoftea/fyp_game1), for version control
- [Balasmiq](https://drive.google.com/file/d/17DneBRFHjLqSMf__QU4schfs7CL0lqn6/view?usp=sharing), for Low-Fi Prototypes
- [Miro](https://miro.com/app/board/uXjVOUxufMg=/), for Portfolio Mappings

## Application Technologies
- **Front-End**: HTML, CSS, Javascript, Jinja2
- **Back-End**: Python Flask
- **Database**: MongoDB Atlas
- **Deployment**: Heroku
- **Testing**: Postman, SIT, UAT
- **Continuous Integration (CI)**: GitHub Actions
- **Continuous Deployment (CD)**: Heroku
- **Design**: Miro, Draw.io

## Directory Layout
- `.github\workflows` contains the github actions 
- `json_files` contains the MongoDB documents according to collections
- `templates` contains the page views
- `assets` contains the image files (they are deployed on AWS as well)

```
.
├───.github\workflows
├───json_files
└───templates
     ├───assets
├───Procfile
├───README.md
├───app.py
├───requirements.txt
├───utils.py
```
## Deployed Application 
   Navigate to https://portfolio-recc.herokuapp.com/
   
## Installation & Running on Local Machine
1. Install requirements 
   ```
   $ pip install Flask-PyMongo
   $ pip install flask
   $ pip install jinja2
   ```
2. Run the Flask app in the terminal window.
   ```
   python app.py
   ```
   Navigate to http://localhost:5000/
   

   
