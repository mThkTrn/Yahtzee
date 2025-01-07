from flask import jsonify
from flask import request
from flask import render_template
import os

from Models import UserModel

DB_location=f"{os.getcwd()}/Models/yahtzeeDB.db"
table_name = "users"
Users = UserModel.User(DB_location, table_name)

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

def login():

    print("running login")

    user_info = {
        "username": request.args.get("username"),
        "password": request.args.get("password")
    }
    
    out = Users.get(username=user_info["username"])
    #f"User {request.form.get("username")} was successfully created"

    print(user_info)
    print(out)

    try:
        if out["data"]["password"] == user_info["password"]:
            return render_template("user_games.html")
        else:
            message = out["data"]
            return render_template("login.html", message = message)
    except:
        message = out["data"]
        return render_template("login.html", message = message)
    
def index():
    return render_template("login.html")

