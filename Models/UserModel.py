# Madhavendra Thakur

import sqlite3
import random
import re
import os

class User:
    def __init__(self, db_name, table_name="users"):
        # print("########")
        # print(db_name)
        # print("###########")
        self.db_name =  db_name
        self.max_safe_id = 9007199254740991 #maximun safe Javascript integer
        self.table_name = table_name
    
    def initialize_table(self):
        db_connection = sqlite3.connect(self.db_name)
        cursor = db_connection.cursor()
        schema=f"""
                CREATE TABLE {self.table_name} (
                    id INTEGER PRIMARY KEY UNIQUE,
                    email TEXT UNIQUE,
                    username TEXT UNIQUE,
                    password TEXT
                );
                """
        cursor.execute(f"DROP TABLE IF EXISTS {self.table_name};")
        results=cursor.execute(schema)
        db_connection.close()

    def validate(self, user_info, user_id = None):

        try:      
      
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()

            if not re.search("^[a-zA-Z0-9_-]*$", user_info["username"]):
                return False
            
            if "@" not in user_info["email"] or "." not in user_info["email"] or " " in user_info["email"]:
                return False
            
            if len(user_info["password"]) < 8:
                return False
            
            if id:
                if user_id > self.max_safe_id:
                    return False
            
            if "id" in user_info.keys():
                if user_info["id"] > self.max_safe_id:
                    return False
            
            if any(cursor.execute(f"SELECT * FROM {self.table_name} WHERE username = '{user_info['username']}' OR email = '{user_info['email']}'").fetchall()):
                return False
            
            return True

        except sqlite3.Error as error:
            return {"status":"error",
                    "data":error}
        finally:
            db_connection.close()
    
    def exists(self, username=None, id=None):
        try:           

            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()
            if not username and not id:
                return {"status":"error",
                    "data":"No username or id given to search for user by."}
            elif not username and id:
                results =  cursor.execute(f"SELECT id, username FROM {self.table_name} WHERE id={id}").fetchall()
            elif username and not id:
                results =  cursor.execute(f"SELECT id, username FROM {self.table_name} WHERE username = '{username}'").fetchall()
            elif username and id:
                results =  cursor.execute(f"SELECT id, username FROM {self.table_name} WHERE id = {id} AND username = '{username}'").fetchall()
            
            return {"status" : "success", "data" : results}
        except sqlite3.Error as error:
            return {"status":"error",
                    "data":error}
        finally:
            db_connection.close()

    def create(self, user_info):
       
        db_connection = sqlite3.connect(self.db_name)
       
        try:
            cursor = db_connection.cursor()

            unique = False
            while not unique:
                user_id = random.randint(0, self.max_safe_id)
                results = cursor.execute(f"SELECT id from {self.table_name}")
                unique = not any([i[0] == user_id for i in results.fetchall()])

            if not self.validate(user_info, user_id):
                return {"status" : "error", "data" : "The format of the input data is incorrect"}
            
            user_data = (user_id, user_info["email"], user_info["username"], user_info["password"])
            #are you sure you have all data in the correct format?
            cursor.execute(f"INSERT INTO {self.table_name} VALUES (?, ?, ?, ?);", user_data)
            db_connection.commit()
            
            return {"status": "success",
                    "data": self.to_dict(user_data)
                    }
        
        except sqlite3.Error as error:
            if type(error).__name__ == "IntegrityError":
                return {"status":"error",
                    "data":"It seems like the server had an error processing the data."}            
            return {"status":"error",
                    "data":(error)}
        
        finally:
            db_connection.close()
    
    def get(self, username=None, id=None):
        global db_connection
        try: 


            
            db_connection = sqlite3.connect(self.db_name)

            if not self.exists(username = username, id = id)["data"]:
                return {"status": "error", "data" : "User does not exist."}
                        
            cursor = db_connection.cursor()
            if not username and not id:
                return {"status":"error",
                    "data":"No username or id given to search for user by."}
            elif username and not id:
                results = cursor.execute(f"SELECT * FROM {self.table_name} WHERE username = '{username}'")
            elif id:
                results = cursor.execute(f"SELECT * FROM {self.table_name} WHERE id = {id}")
            
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

    def update(self, user_info): 
        try: 
        

            db_connection = sqlite3.connect(self.db_name)

            if not self.exists(id = user_info["id"])["data"]:
                return {"status": "error", "data" : "User does not exist."}
            
            if not self.validate(user_info, user_id=user_info["id"]):
                return {"status" : "error", "data" : "The format of the input data is incorrect"}
            
            cursor = db_connection.cursor()
            execstring = f"UPDATE {self.table_name} SET username = '{user_info['username']}', email = '{user_info['email']}', password = '{user_info['password']}' WHERE id = {user_info['id']}"
            
            cursor.execute(execstring)
            
            db_connection.commit()

            return {"status": "success", "data" : self.get(id = user_info["id"])["data"]}

        
        except sqlite3.Error as error:
            return {"status":"error",
                    "data":error}
        finally:
            db_connection.close()

    def remove(self, username):
        try: 
            db_connection = sqlite3.connect(self.db_name)

            if not self.exists(username = username)["data"]:
                return {"status": "error", "data" : "User does not exist."}
        
            cursor = db_connection.cursor()
            deleted_user = self.get(username=username)["data"]
            cursor.execute(f"DELETE FROM {self.table_name} WHERE username = '{username}'")
            db_connection.commit()
            return {"status": "success", "data": deleted_user}
        except sqlite3.Error as error:
            return {"status":"error",
                    "data":error}
        finally:
            db_connection.close()

    
    def to_dict(self, user_tuple):
        '''Utility function which converts the tuple returned from a SQLlite3 database
           into a Python dictionary
        '''
        user_dict={}
        if user_tuple:
            user_dict["id"]=user_tuple[0]
            user_dict["email"]=user_tuple[1]
            user_dict["username"]=user_tuple[2]
            user_dict["password"]=user_tuple[3]
        return user_dict

if __name__ == '__main__':
    import os
    # print("Current working directory:", os.getcwd())
    DB_location=f"{os.getcwd()}/Models/yahtzeeDB.db"
    table_name = "users"
    
    Users = User(DB_location, table_name) 
    Users.initialize_table()

    user_details={
        "email":"justin.gohde@trinityschoolnyc.org",
        "username":"justingohde",
        "password":"123TriniT"
    }

    user_details_2={
        "id":5406272519923547,
        "email":"justin.gohde@trinityschoolnyc.org",
        "username":"justingohde",
        "password":"123TriniT"
    }

    user_details_3={
        "id":5406272519923547,
        "email":"justin.gohde@trinityschoolnyc.org",
        "username":"justingohde",
        "password":"secretpassword"
    }
    
    results = Users.create(user_details)

    user_details={
        "email":"bobthebuilder@gmail.com",
        "username":"bobthebuilder",
        "password":"buildWithMe"
    }
    results = Users.create(user_details)

    # print(results)

    # print("User 'justingohde' exists:", Users.exists("justingohde"))

    print(Users.get(username = "justingohde"))

    print(Users.get(id = 11235813))

    print(Users.exists("justingohde"))


    #Users.remove("justingohde")

    # print("User 'justingohde' exists:", Users.exists("justingohde"))

    # print("User 'bob' exists:", Users.exists("bob"))

    # Users.update(user_details_3)

    # print(Users.get_all())

