from flask import jsonify
from flask import request
from flask import render_template
from flask import redirect
import os

from Models import Game_Model, Scorecard_Model, User_Model

DB_location=f"{os.getcwd()}/Models/yahtzeeDB.db"
table_name = "users"
Users = User_Model.User(DB_location, table_name)

table_name = "games"
Games = Game_Model.Game(DB_location, table_name)

table_name = "scorecard"
Scorecard = Scorecard_Model.Scorecard(DB_location, table_name)

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

def game_index(username, message = ""):

    print("gme index running")

    if not Users.exists(username=username)["data"]:
        message = "User for user_games did not exist!"
        return render_template("login.html", message = message)

    gameslist = Scorecard.get_all_user_game_names(username=username)

    print("---gameslist---")

    print(gameslist)

    print("---#---")

    gameslist = gameslist["data"]

    scoreslist = Scorecard.get_user_high_scores(username = username)

    print("---scoreslist---")

    print(scoreslist)

    print("---#---")

    scoreslist = scoreslist["data"]

    return render_template("user_games.html", gameslist = gameslist, scoreslist = scoreslist, username=username, message = message)

def game_create():
    game_name = request.form.get("game_name")
    username = request.form.get("username")
    game_info = {
        "name" : game_name
    }
    if Games.exists(game_name=game_name)["data"]:
        return game_index(username=username, message = "Game already exists!")
    else:
        out = Games.create(game_info=game_info)
        if out["status"] == "success":
            Scorecard.create(game_id=out["data"]["id"], user_id=Users.get(username=username)["data"]["id"], name = f"{game_name}|{username}")
            return redirect(f"games/{username}")
        else:
            return render_template("user_games.html", message = out)
def game_join():
    return render_template("user_games.html")

def game_remove(game_name, user_name):

    print("game remove running")

    id = Scorecard.get_scorecard_id_user_game_name(user_name=user_name, game_name=game_name)["data"]
    
    out = Scorecard.remove(id = id)
    Games.remove(game_name=game_name)

    print("scorecard remove", out)
    return game_index(username=user_name)

def game_get(game_name, user_name):
    return render_template("yahtzee.html")

