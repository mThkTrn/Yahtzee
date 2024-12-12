from flask import Flask
from flask import request
import os
import sys

#Connect Controller definitions
fpath = os.path.join(os.path.dirname(__file__), 'controllers')
sys.path.append(fpath)
fpath = os.path.join(os.path.dirname(__file__), 'models')
sys.path.append(fpath)
from Controllers import GameController, SessionController, ScorecardController, UserController


app = Flask(__name__, static_url_path='', static_folder='static')

#The Router section of our application conects routes to Contoller methods
app.add_url_rule('/', view_func=SessionController.login, methods = ['GET'])
app.add_url_rule('/index', view_func=SessionController.login, methods = ['GET'])
app.add_url_rule('/login', view_func=SessionController.login, methods = ['GET'])

#SESSION CONTROLLER

app.add_url_rule('/', view_func=SessionController.login, methods = ["GET"])

app.add_url_rule('/login', view_func=SessionController.login, methods = ['GET'])

#GAME CONTROLLER

app.add_url_rule('/games/<username>', view_func=GameController.user, methods = ['GET'])

app.add_url_rule('/games', view_func=GameController, methods = ['GET'])

#SCORECARD CONTROLLER



#Start the server
app.run(debug=True, port=5000)