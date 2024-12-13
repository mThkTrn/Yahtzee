# Madhavendra Thakur

import sqlite3
import random
import re
import datetime
import os

class Game:
    def __init__(self, db_name, table_name="games"):
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
                    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    finished TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                """
        cursor.execute(f"DROP TABLE IF EXISTS {self.table_name};")
        results=cursor.execute(schema)
        db_connection.close()
    
    def exists(self, game_name=None, id=None, update = False):
        try:
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()
            if not update:
                if game_name:
                    results =  cursor.execute(f"SELECT id, name FROM {self.table_name} WHERE name = '{game_name}'").fetchall()
                elif id:
                    results =  cursor.execute(f"SELECT id, name FROM {self.table_name} WHERE id = {id}").fetchall()
                else:
                    return {"status" : "error",  "data" : "Name or id must be given to check if game exists"}
            else:
                print("running this bit - good")
                results =  cursor.execute(f"SELECT id, name FROM {self.table_name} WHERE id = {id}").fetchall()
            
            
            return {"status" : "success", "data" : bool(results)}
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

            if not self.validate(game_info=game_info, game_id=game_id):
                return {"status" : "error", "data" : "The data enterd is not in the correct format"}

            
            
            game_data = (game_id, game_info["name"])
            #are you sure you have all data in the correct format?
            cursor.execute(f"INSERT INTO {self.table_name} (id, name) VALUES (?, ?);", game_data)
            db_connection.commit()
            
            return {"status": "success",
                    "data": self.get(game_name=game_info["name"])["data"]
                    }


        
        except sqlite3.Error as error:
            return {"status":"error",
                    "data":error}
        
        finally:
            db_connection.close()
    
    def get(self, game_name = None, id = None):
        global db_connection
        try: 

            
            db_connection = sqlite3.connect(self.db_name)

            if not self.exists(game_name=game_name, id = id)["data"]:
                return {"status": "error", "data" : "Game does not exist."}
                        
            cursor = db_connection.cursor()

            if game_name:
                results = cursor.execute(f"SELECT * FROM {self.table_name} WHERE name = '{game_name}'"
)
            elif id:
                results = cursor.execute(f"SELECT * FROM {self.table_name} WHERE id = {id}")
            else:
                return {"status" : "error", "data": "Game name of id must be provided to get user"}
            
            out = results.fetchone()

            return {"status" : "success", "data" : self.to_dict(out)}
        except sqlite3.Error as error:
            return {"status":"error",
                    "data":error}
        finally:
            db_connection.close()
    
    def get_all(self): 
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()
            
            return {"status" : "success", "data" : [self.to_dict(k) for k in cursor.execute(f"SELECT * FROM {self.table_name}").fetchall()]}

        except sqlite3.Error as error:
            return {"status":"error",
                    "data":error}
        finally:
            db_connection.close()

    def validate(self, game_info, game_id = None, update = False):

        db_connection = sqlite3.connect(self.db_name)
        cursor = db_connection.cursor()

        if not re.search("^[a-zA-Z0-9_-]*$", game_info["name"]):
            print("name has unpermitted characters validate")
            return False
        
        if game_id:
            if game_id > self.max_safe_id:
                print("id too long validate")
                return False
        
        if "id" in game_info.keys():
            if int(game_info["id"]) > self.max_safe_id:
                print("id too long validate")
                return False

        if not update and any(cursor.execute(f"SELECT * FROM {self.table_name} WHERE name = '{game_info['name']}'").fetchall()):
            print("name duplicate validate")
            return False

        return True   
    
    def is_finished(self, game_name):

        game_info =  self.get(game_name = game_name)["data"]
        # print("game info")
        # print(game_info)

        return {"status": "success", "data" : not game_info["created"] == game_info["finished"]}

    def update(self, game_info): 
        # try: 

            db_connection = sqlite3.connect(self.db_name)

            if not self.validate(game_info, update=True):
                return {"status" : "error", "data" : "The format of the input data is invalid"}
            
            if not self.exists(id = game_info["id"], update = True)["data"]:
                return {"status": "error", "data" : "Game does not exist."}
            
            cursor = db_connection.cursor()
            numres = cursor.execute(f"SELECT * FROM games WHERE name = '{game_info['name']}'")
            numres = numres.fetchall()

            if len(numres) == 1:
                if numres[0][0] == game_info["id"]:
                    execstring = f"UPDATE {self.table_name} SET created = '{game_info['created']}', finished = '{game_info['finished']}' WHERE id = {game_info['id']}"
                else:
                    return {"status" : "error", "data" : "You cannot update the name of this game to be the same as the name of another game."}
            else:
                execstring = f"UPDATE {self.table_name} SET name = '{game_info['name']}', created = '{game_info['created']}', finished = '{game_info['finished']}' WHERE id = {game_info['id']}"

            print(execstring)
            cursor.execute(execstring)
            
            db_connection.commit()

            return {"status": "success", "data" : self.get(game_name = game_info["name"])["data"]}

        
        # except sqlite3.Error as error:
        #     if type(error).__name__ == "IntegrityError":
        #         return {"status":"error",
        #             "data":"It seems like the server had an error processing the data"}
        #     return {"status":"error",
        #             "data":str(error)}
        # finally:
        #     db_connection.close()

    def remove(self, game_name):
        try: 
            db_connection = sqlite3.connect(self.db_name)

            if not self.exists(game_name=game_name)["data"]:
                return {"status": "error", "data" : "Game does not exist."}
        
            cursor = db_connection.cursor()
            deleted_game = self.get(game_name=game_name)["data"]
            print("deleter_game:", deleted_game)
            cursor.execute(f"DELETE FROM {self.table_name} WHERE name = '{game_name}'")
            db_connection.commit()
            return {"status": "success", "data": deleted_game}
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
            game_dict["name"]=game_tuple[1]
            game_dict["created"]=game_tuple[2]
            game_dict["finished"]=game_tuple[3]
        return game_dict

if __name__ == '__main__':
    import os
    # print("Current working directory:", os.getcwd())
    DB_location=f"{os.getcwd()}/Models/yahtzeeDB.db"
    table_name = "games"

    game = Game(DB_location, table_name=table_name)

    changedict = {
        "id" : "2610751908864900",
        "name" : "ourGame2",
        "created" : "2024-11-21 00:56:23",
        "finished" : datetime.datetime.now(),
    }
    out = game.update(changedict)

    print(out)
    