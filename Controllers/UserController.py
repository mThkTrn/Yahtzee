from flask import jsonify
from flask import request
import os

from Models import UserModel

DB_location=f"{os.getcwd()}/Models/yahtzeeDB.db"
table_name = "users"
Users = UserModel.User(DB_location, table_name)

def fruit():
    print(f"request.method= {request.method} request.url={request.url}")
    print(f"request.url={request.query_string}")
    print(f"request.url={request.args.get('name')}") #GET request & query string
    print(f"request.url={request.form.get('name')}") #POST request & form body

    # curl "http://127.0.0.1:5000/fruit/"
    if request.method == 'GET':
        return jsonify(Fruit.get_all_fruit())
    
    #curl -X POST -H "Content-type: application/json" -d '{ "name" : "tomato", "url":"https://en.wikipedia.org/wiki/Tomato"}' "http://127.0.0.1:5000/fruit/new"
    elif request.method == 'POST':
        return jsonify(Fruit.create_fruit(request.form))

def 
