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

def create_user():
    user_info = {
        "email": request.form.get("email"),
        "username": request.form.get("username"),
        "password": request.form.get("password")
    }
    out = Users.create(user_info=user_info)
    #f"User {request.form.get("username")} was successfully created"
    try:
        message = f"User '{(out['data']['username'])}' created."
        return render_template("user_games.html")
    except:
        message = out["data"]
        return render_template("create.html", message = message)
def delete_user():
    pass
def update_user():
    user_info = {
        "email": request.form.get("email"),
        "username": request.form.get("username"),
        "password": request.form.get("password")
    }
    user_info_updating = Users.get(username = user_info["username"])["data"]

    user_info_updating["email"] = user_info["email"]
    user_info_updating["username"] = user_info["username"]
    user_info_updating["password"] = user_info["password"]

    out = Users.update(user_info=user_info_updating)
    try:
        message = f"User '{(out['data']['username'])}' updated."
    except:
        message = out["data"]
        return render_template("create.html", purpose = "update", message = message)
def read_user_create():
    print("running!")
    return render_template("create.html", message = "")
def read_user_update_delete(username):
    if not Users.exists(username=username)["data"]:
        return render_template("create.html", purpose = "update", message = "Specified user does not exist.")
    else: 
        return render_template("create.html", purpose = "update", message = "")

