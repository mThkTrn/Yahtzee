from flask import jsonify
from flask import request
from flask import render_template
import os

from Models import UserModel, GameModel, ScorecardModel

DB_location=f"{os.getcwd()}/Models/yahtzeeDB.db"
table_name = "users"
Users = UserModel.User(DB_location, table_name)

table_name = "games"
Games = GameModel.Game(DB_location, table_name)

table_name = "scorecard"
Scorecard = ScorecardModel.Scorecard(DB_location, table_name)

# def fruit():
#     print(f"request.method= {request.method} request.url={request.url}")
#     print(f"request.url={request.query_string}")
#     print(f"request.url={request.args.get('name')}") #GET request & query string
#     print(f"request.url={request.form.get('name')}") #POST request & form body

#     # curl "http://127.0.0.1:5000/fruit/"
#     if request.method == 'GET':
#         return jsonify(Fruit.get_all_fruit())
    
#     #curl -X POST -H "Content-type: application/json" -d '{ "name" : "tomato", "url":"https://en.wikipedia.org/wiki/Tomato"}' "http://127.0.0.1:5000/fruit/new"
#     elif request.method == 'POST':
#         return jsonify(Fruit.create_fruit(request.form))

def game_index(username):

    if not Users.exists(username=username)["data"]:
        message = "User for user_games did not exist!"
        return render_template("login.html", message = message)

    gameslist = Scorecard.get_all_user_game_names(username=username)["data"]

    scoreslist = Scorecard.get_user_high_scores(username = username)

    print("###")
    print("scoreslist", scoreslist)
    print("###")

    scoreslist = scoreslist["data"][:4]

    return render_template("user_games.html", gameslist = gameslist, scoreslist = scoreslist)

def game_create():
    return render_template("user_games.html")

def game_join():
    return render_template("user_games.html")

def game_remove(game_name, user_name):
    return render_template("login.html")

def game_get(game_name, user_name):
    return render_template("yahtzee.html")

