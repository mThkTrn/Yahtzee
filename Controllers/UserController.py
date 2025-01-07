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
def delete_user(username):
    print("delete_user running")

    out = Users.remove(username=username)

    print(out)

    try:
        message = f"User '{(out['data']['username'])}' deleted."
        return render_template("user_games.html", message = message)
    except:
        message = out["data"]
        return render_template("user_games.html", message = message)

def update_user():
    print("update_user running")
    user_info = {
        "email": request.form.get("email"),
        "username": request.form.get("username"),
        "password": request.form.get("password"),
        "user_id": request.form.get("user_id")
    }
    user_info_updating = Users.get(id = user_info["user_id"])

    print(user_info_updating)

    user_info_updating = user_info_updating["data"]

    user_info_updating["email"] = user_info["email"]
    user_info_updating["username"] = user_info["username"]
    user_info_updating["password"] = user_info["password"]

    print(user_info_updating)
    
    out = Users.update(user_info=user_info_updating)

    print(out)
    try:
        message = f"User '{(out['data']['username'])}' updated."
    except:
        message = out["data"]
        return render_template("create.html", purpose = "update", message = message)
def read_user_create():
    print("running!")
    return render_template("create.html", message = "")
def read_user_update_delete(username):

    print("read_user_update_delete running")

    user_info_updating = Users.get(username = username)

    print(user_info_updating)

    # print(user_info_updating["data"]["username"], user_info_updating["data"]["email"], user_info_updating["data"]["password"])

    if not Users.exists(username=username)["data"]:
        return render_template("create.html", purpose = "update", message = "Specified user does not exist.")
    else: 
        return render_template("create.html", purpose = "update", message = "", user_id = user_info_updating["data"]["id"], username = user_info_updating["data"]["username"], email = user_info_updating["data"]["email"], password = user_info_updating["data"]["password"])

