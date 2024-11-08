import sqlite3
import random
import re

class Game:
    def __init__(self, db_name, table_name):
        self.db_name =  db_name
        self.max_safe_id = 9007199254740991 #maximun safe Javascript integer
        self.table_name = table_name
    
    def initialize_table(self):
        db_connection = sqlite3.connect(self.db_name)
        cursor = db_connection.cursor()
        schema=f"""
                CREATE TABLE {self.table_name} (
                    id INTEGER PRIMARY KEY UNIQUE,
                    name TEXT UNIQUE,
                    created DATE,
                    finished DATE
                );
                """
        cursor.execute(f"DROP TABLE IF EXISTS {self.table_name};")
        results=cursor.execute(schema)
        db_connection.close()
    
    def exists(self, name=None, id=None):
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()
            if not name and not id:
                return {"status":"error",
                    "data":"No name or id given to search for game by."}
            elif not name and id:
                results =  cursor.execute(f"SELECT id, name FROM {self.table_name} WHERE id = {id}")
            elif name and not id:
                results =  cursor.execute(f"SELECT id, name FROM {self.table_name} WHERE name = '{name}'")
            elif name and id:
                results =  cursor.execute(f"SELECT id, name FROM {self.table_name} WHERE id = {id} AND name = '{name}'")
            
            return any(results)
        except sqlite3.Error as error:
            return {"status":"error",
                    "data":error}
        finally:
            db_connection.close()

    def create(self, game_info):
        try:
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()

            unique = False
            while not unique:
                game_id = random.randint(0, self.max_safe_id)
                results = cursor.execute(f"SELECT id from {self.table_name}")
                unique = not any([i[0] == game_id for i in results.fetchall()])

            if not re.search("^[a-zA-Z0-9_-]*$", game_info["name"]):
                return {"status": "error", "data": "name contains invalid characters. name should only contain alphanumberic characters, '-' and '_'"}
            
            if game_info['id'] > self.max_safe_id:
                return {"status": "error", "data": f"Id must be at most {self.max_safe_id}"}

            if any(cursor.execute(f"SELECT * FROM {self.table_name} WHERE name = '{game_info["name"]}' OR email = '{game_info["email"]}'").fetchall()):
                return {"status": "error", "data": "name or email is not unique"}

            
            
            game_data = (game_id, game_info["email"], game_info["name"], game_info["password"])
            #are you sure you have all data in the correct format?
            cursor.execute(f"INSERT INTO {self.table_name} VALUES (?, ?, ?, ?);", game_data)
            db_connection.commit()
            
            return {"status": "success",
                    "data": self.to_dict(game_data)
                    }
        
        except sqlite3.Error as error:
            return {"status":"error",
                    "data":error}
        
        finally:
            db_connection.close()
    
    def get(self, name=None, id=None):
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()
            if not name and not id:
                return {"status":"error",
                    "data":"No name or id given to search for game by."}
            elif name and not id:
                results = cursor.execute(f"SELECT * FROM {self.table_name} WHERE name = '{name}'")
            elif not name and id:
                results = cursor.execute(f"SELECT * FROM {self.table_name} WHERE id = 'id'")
            elif name and id:
                results = cursor.execute(f"SELECT * FROM {self.table_name} WHERE name = '{name}' AND id = 'id'")
            
            return {"status" : "success", "data" : self.to_dict(results.fetchone())}
        except sqlite3.Error as error:
            return {"status":"error",
                    "data":error}
        finally:
            db_connection.close()
    
    def get_all(self): 
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()
            
            return cursor.execute(f"SELECT * FROM {self.table_name}").fetchall()

        except sqlite3.Error as error:
            return {"status":"error",
                    "data":error}
        finally:
            db_connection.close()

    def update(self, game_info): 
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()
            cursor.execute(f"UPDATE {self.table_name} SET name = {game_info["name"]}, email = {game_info["email"]}, password = {game_info["password"]} WHERE id = {game_info["id"]}")
        except sqlite3.Error as error:
            return {"status":"error",
                    "data":error}
        finally:
            db_connection.close()

    def remove(self, name):
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()
            results = cursor.execute(f"DELETE FROM {self.table_name} WHERE name = '{name}'")
            db_connection.commit()
        except sqlite3.Error as error:
            return {"status":"error",
                    "data":error}
        finally:
            db_connection.close()
    
    def to_dict(self, game_tuple):
        '''Utility function which converts the tuple returned from a SQLlite3 database
           into a Python dictionary
        '''
        game_dict={}
        if game_tuple:
            game_dict["id"]=game_tuple[0]
            game_dict["email"]=game_tuple[1]
            game_dict["name"]=game_tuple[2]
            game_dict["password"]=game_tuple[3]
        return game_dict

if __name__ == '__main__':
    import os
    print("Current working directory:", os.getcwd())
    DB_location=f"{os.getcwd()}/Models/yahtzeeDB.db"
    table_name = "games"
    
    games = game(DB_location, table_name) 
    games.initialize_table()

    game_details={
        "email":"justin.gohde@trinityschoolnyc.org",
        "name":"justingohde",
        "password":"123TriniT"
    }
    results = games.create(game_details)

    game_details={
        "email":"bobthebuilder@gmail.com",
        "name":"bobthebuilder",
        "password":"buildWithMe"
    }
    results = games.create(game_details)

    print(results)

    print("game 'justingohde' exists:", games.exists("justingohde"))

    print(games.get("justingohde"))


    #games.remove("justingohde")

    print("game 'justingohde' exists:", games.exists("justingohde"))

    print("game 'bob' exists:", games.exists("bob"))

    print(games.get_all())

