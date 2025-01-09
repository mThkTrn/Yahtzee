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

# #SESSION CONTROLLER

# app.add_url_rule('/', view_func=SessionController.entry, methods = ["GET"])

# app.add_url_rule('/login', view_func=SessionController.login, methods = ['GET'])

# #GAME CONTROLLER

# app.add_url_rule('/games/<username>', view_func=GameController.user, methods = ['GET'])

# app.add_url_rule('/games', view_func=GameController.create, methods = ['POST'])

# app.add_url_rule('/games/join', view_func=GameController.join, methods = ['POST'])

# app.add_url_rule('/games/delete/<game_name>/<username>', view_func=GameController.delete, methods = ['GET'])

# app.add_url_rule('/games/<game_name>/<user_name>', view_func=GameController.get, methods = ['GET'])

# #SCORECARD CONTROLLER

# app.add_url_rule('/scorecard/<scorecard_id>', view_func=ScorecardController.update, methods = ['GET'])

#USER CONTROLLER

app.add_url_rule('/users', view_func=UserController.read_user_create, methods = ['GET'])
app.add_url_rule('/users/<username>', view_func=UserController.read_user_update_delete, methods = ['GET'])
app.add_url_rule('/users', view_func=UserController.create_user, methods = ['POST'])
app.add_url_rule('/users/<username>', view_func=UserController.update_user, methods = ['POST'])
app.add_url_rule('/users/delete/<username>', view_func=UserController.delete_user, methods = ['GET'])
app.add_url_rule("/users/update", view_func=UserController.update_user, methods = ['POST'])

# SESSION CONTROLLER

app.add_url_rule("/", view_func=SessionController.index, methods = ['GET'])
app.add_url_rule("/login", view_func=SessionController.login, methods = ['GET'])

# SESSION CONTROLLER

app.add_url_rule("/games/<username>", view_func=GameController.game_index, methods = ['GET'])
app.add_url_rule("/games", view_func=GameController.game_create, methods = ['POST'])
app.add_url_rule("/games/join", view_func=GameController.game_join, methods = ['POST'])
app.add_url_rule("/games/delete/<game_name>/<user_name>", view_func=GameController.game_remove, methods = ['GET'])
app.add_url_rule("/games/<game_name>/<user_name>", view_func=GameController.game_get, methods = ['GET'])

#Start the server
app.run(debug=True, port=8080)