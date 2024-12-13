import unittest
import sqlite3
import os

#test should inhabit the same folder as User_Model.py
from UserModel import User

def ensure_data_packet_formatting(self, packet, method, status):
    if status == "success":
        #format of returned data packet
        self.assertTrue("status" in packet, f"{method} should return a data packet object in the correct format")
        self.assertEqual(packet["status"], "success", f"{method} should return success")
        self.assertTrue("data" in packet, f"{method} should return a data packet object in the correct format")
        if type(packet['data']) == dict:
            self.assertTrue("email" in packet["data"], f"{method} should return a data packet object in the correct format")
            self.assertTrue("username" in packet["data"], f"{method} should return a data packet object in the correct format")
            self.assertTrue("password" in packet["data"], f"{method} should return a data packet object in the correct format")
        elif type(packet['data']) == list:
            for user in packet['data']:
                self.assertTrue("email" in user, f"{method} should return a data packet object in the correct format")
                self.assertTrue("username" in user, f"{method} should return a data packet object in the correct format")
                self.assertTrue("password" in user, f"{method} should return a data packet object in the correct format")
    elif status  == "error":
        self.assertEqual(packet["status"], "error", f"{method} should return error")
        self.assertTrue(len(packet["data"]) > 10 , f"{method}- Data packet should return an error message of significant length")

class User_Model_Tests(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        #Runs once, before any tests are run
        self.yahtzee_db_name=f"{os.getcwd()}/Models/yahtzeeDB.db"
        self.table_name = "users"
        self.UserModel = User(self.yahtzee_db_name, self.table_name)
        self.users=[{"email":"cookie.monster@trinityschoolnyc.org",
                    "username":"cookieM",
                    "password":"123TriniT"},
                    {"email":"justin.gohde@trinityschoolnyc.org",
                    "username":"justingohde",
                    "password":"123TriniT"},
                    {"email":"zelda@trinityschoolnyc.org",
                    "username":"princessZ",
                    "password":"123TriniT"},
                    {"email":"test.user@trinityschoolnyc.org",
                    "username":"testuser",
                    "password":"123TriniT"}]
        self.users_tuples = [(user["email"], user["username"], user["password"]) for user in self.users]
        self.users_tuples.sort(key=lambda user: user[0])

    def setUp(self):
        #Runs before every test
        self.UserModel.initialize_table() #start with a fresh database for every test
        try:  #check DB state
            db_connection = sqlite3.connect(self.yahtzee_db_name)
            cursor = db_connection.cursor()
            query = f"SELECT * from {self.table_name};"
            results = cursor.execute(query)
            for r in results:
                print(r)
            
        except sqlite3.Error as error:
            print(error)
        finally:
            db_connection.close()
     
    def test_create_1_user(self):
        method = "users.create"
        results = self.UserModel.create(self.users[0]) #add 1 user to the database

        #check method input/output
        ensure_data_packet_formatting(self, results, method, "success")
        self.assertEqual(results["data"]["email"], self.users[0]["email"], f"{method} - Data of returned user should match data of added user")
        self.assertEqual(results["data"]["username"], self.users[0]["username"], f"{method} - Data of returned user should match data of added user")    
        self.assertEqual(results["data"]["password"], self.users[0]["password"], f"{method} - Data of returned user should match data of added user")

        try:  #check DB state
            db_connection = sqlite3.connect(self.yahtzee_db_name)
            cursor = db_connection.cursor()
            query = f"SELECT * from {self.table_name};"
            results = cursor.execute(query)

            all_users = []
            for user in results.fetchall():
                all_users.append(user)

            self.assertEqual(len(all_users), 1, f"{method} a single user should result in a table with exactly 1 user")
            self.assertEqual(all_users[0][1], self.users[0]["email"], f"{method}- Data of returned user should match data of added user")
            self.assertEqual(all_users[0][2], self.users[0]["username"], f"{method}- Data of returned user should match data of added user")    
            self.assertEqual(all_users[0][3], self.users[0]["password"], f"{method}- Data of returned user should match data of added user")
            print("test_create_1_user passed!")
        except sqlite3.Error as error:
            print(error)
        finally:
            db_connection.close()

    def test_create_4_users(self):
        method = "users.create"
        results = []
        for i in range(len(self.users)):
            results.append(self.UserModel.create(self.users[i]))

        for i in range(len(results)):
            ensure_data_packet_formatting(self, results[i], method, "success")
            self.assertEqual(results[i]["data"]["email"], self.users[i]["email"], f"{method} - Data of returned user should match data of added user")
            self.assertEqual(results[i]["data"]["username"], self.users[i]["username"], f"{method} - Data of returned user should match data of added user")    
            self.assertEqual(results[i]["data"]["password"], self.users[i]["password"], f"{method} - Data of returned user should match data of added user")

        try:  #check DB state
            db_connection = sqlite3.connect(self.yahtzee_db_name)
            cursor = db_connection.cursor()
            query = f"SELECT * from {self.table_name};"
            results = cursor.execute(query)

            all_users = []
            for user in results.fetchall():
                all_users.append((user[1], user[2], user[3]))
            #users won't necessarialy be in order because id's are randomly generated
            #the DB keeps entities in sorted order via the id

            all_users.sort(key=lambda user: user[0])#sort by email to match test data
            
            self.assertEqual(len(all_users), 4, "Creating a single user should result in a table with exactly 1 user")
            self.assertEqual(all_users, self.users_tuples, "Data of returned users should match data of added users")
            print("test_create_4_users passed!")
        except sqlite3.Error as error:
            print(error)
        finally:
            db_connection.close()
    
    def test_create_user_with_duplicate_username_or_email(self):
       method = "users.create"
       for i in range(len(self.users)):
          self.UserModel.create(self.users[i]) # 4 users in DB
    
       new_user ={"email":self.users[2]["email"], #email is duplicate
                    "username":"somethingdifferent",
                    "password":"12345678920"}
       returned_user = self.UserModel.create(new_user)
       ensure_data_packet_formatting(self, returned_user, method, "error")
       try:  #check DB state
            db_connection = sqlite3.connect(self.yahtzee_db_name)
            cursor = db_connection.cursor()
            query = f"SELECT * from {self.table_name};"
            results = cursor.execute(query)
            all_users = results.fetchall()
            self.assertEqual(len(all_users), len(self.users), f"{method}-  {len(self.users)} users should be returned")
       except sqlite3.Error as error:
            print(error)
       finally:
            db_connection.close()

       new_user ={"email":"hello_hello_@haveaniceday.com", 
                    "username":self.users[1]["username"],#email is duplicate
                    "password":"12345678920"}
       returned_user = self.UserModel.create(new_user)
       ensure_data_packet_formatting(self, returned_user, method, "error")
       try:  #check DB state
            db_connection = sqlite3.connect(self.yahtzee_db_name)
            cursor = db_connection.cursor()
            query = f"SELECT * from {self.table_name};"
            results = cursor.execute(query)
            all_users = results.fetchall()
            self.assertEqual(len(all_users), len(self.users), f"{method}-  {len(self.users)} users should be returned")
            print("test_create_user_with_duplicate_username_or_email passed!")
       except sqlite3.Error as error:
            print(error)
       finally:
            db_connection.close()

    def test_create_user_with_incorrect_data_format(self):
       method = "users.create"
       for i in range(len(self.users)):
          self.UserModel.create(self.users[i]) # 4 users in DB
    
       bad_user_data = [{"email": "hi.com", 
                    "username":"somethingdifferent",
                    "password":"12345678920"}, # bad email
                    {"email": "hi@com", 
                    "username":"somethingdifferent",
                    "password":"12345678920"},# bad email
                    {"email": "hey_hey", 
                    "username":"somethingdifferent",
                    "password":"12345678920"},# bad email
                    {"email": "hey hey", 
                    "username":"somethingdifferent",
                    "password":"12345678920"}, # bad email
                    {"email": "hey_hey@haveaniceday.com", 
                    "username":"somethingdifferent",
                    "password":"123"}, # password too short
                    {"email": "hey_hey@haveaniceday.com", 
                    "username":"something different",  # bad username
                    "password":"123456789"},
                    {"email": "hey_hey@haveaniceday.com", 
                    "username":"something@different",  # bad username
                    "password":"123456789"},
                    {"email": "hey_hey@haveaniceday.com", 
                    "username":"!something@different<>",  # bad username
                    "password":"123456789"}
                    ]
       for bad_user in bad_user_data:
            returned_user = self.UserModel.create(bad_user)
       
            ensure_data_packet_formatting(self, returned_user, method, "error")
            try:  #check DB state
                db_connection = sqlite3.connect(self.yahtzee_db_name)
                cursor = db_connection.cursor()
                query = f"SELECT * from {self.table_name};"
                results = cursor.execute(query)
                all_users = results.fetchall()
                self.assertEqual(len(all_users), len(self.users), f"{method}-  {len(self.users)} users should be returned")
            except sqlite3.Error as error:
                print(error)
            finally:
                db_connection.close()
       print("test_create_user_with_incorrect_data_format passed!")

    def test_exists_id(self):
       method = "users.exists"
       user_ids={}
       for i in range(len(self.users)):
            user_ids[self.users[i]['email']] = self.UserModel.create(self.users[i])["data"]["id"]

       packet = self.UserModel.exists(id=user_ids[self.users[1]['email']]) 
       self.assertTrue("status" in packet, f"{method} should return a data packet object in the correct format")
       self.assertEqual(packet["status"], "success", f"{method} should return success")
       self.assertTrue("data" in packet, f"{method} should return a data packet object in the correct format")
       self.assertTrue(packet["data"], f"{method} should return True for a user that does exist")
       print("test_exists_id passed!")

    def test_exists_username(self):
       method = "users.exists"
       
       for i in range(len(self.users)):
            self.UserModel.create(self.users[i])

       packet = self.UserModel.exists(username=self.users[1]['username']) 
       self.assertTrue("status" in packet, f"{method} should return a data packet object in the correct format")
       self.assertEqual(packet["status"], "success", f"{method} should return success")
       self.assertTrue("data" in packet, f"{method} should return a data packet object in the correct format")
       self.assertTrue(packet["data"], f"{method} should return True for a user that does exist")
       print("test_exists_username passed!")
       
    def test_exists_user_DNE(self):
       method = "users.exists"
       user_DNE = "apples"
       packet = self.UserModel.exists(user_DNE) 
       self.assertTrue("status" in packet, f"{method} should return a data packet object in the correct format")
       self.assertEqual(packet["status"], "success", f"{method} should return success")
       self.assertTrue("data" in packet, f"{method} should return a data packet object in the correct format")
       self.assertFalse(packet["data"], f"{method} should return False for a user that does not exist")
       print("test_exists_user_DNE passed!")

    def test_get_user_exists_username(self):
       method = "users.get"

       user_ids={}
       for i in range(len(self.users)):
            user_ids[self.users[i]['email']] = self.UserModel.create(self.users[i])["data"]["id"]
  
       returned_user_packet= self.UserModel.get(username=self.users[0]['username'])
       ensure_data_packet_formatting(self, returned_user_packet, method, "success")
       returned_user = returned_user_packet['data']
       self.assertEqual(returned_user["id"], user_ids[returned_user["email"]], f"{method}- returned email should match data of original info")
       self.assertEqual(returned_user["email"], self.users[0]["email"], f"{method}- returned email should match data of original info")
       self.assertEqual(returned_user["username"], self.users[0]["username"], f"{method}- returned username should match data of original infor")    
       self.assertEqual(returned_user["password"], self.users[0]["password"], f"{method}- returned password should match data of original info")
       print("test_get_user_exists_username passed!")
      
    def test_get_user_exists_id(self):
       method = "users.get"

       user_ids={}
       for i in range(len(self.users)):
            user_ids[self.users[i]['email']] = self.UserModel.create(self.users[i])["data"]["id"]
  
       returned_user_packet= self.UserModel.get(id=user_ids[self.users[0]['email']])
       ensure_data_packet_formatting(self, returned_user_packet, method, "success")
       returned_user = returned_user_packet['data']
       self.assertEqual(returned_user["id"], user_ids[returned_user["email"]], f"{method}- returned email should match data of original info")
       self.assertEqual(returned_user["email"], self.users[0]["email"], f"{method}- returned email should match data of original info")
       self.assertEqual(returned_user["username"], self.users[0]["username"], f"{method}- returned username should match data of original infor")    
       self.assertEqual(returned_user["password"], self.users[0]["password"], f"{method}- returned password should match data of original info")
       print("test_get_user_exists_id passed!")
      
    def test_get_user_DNE(self):
       method = "users.get"
       user_DNE = "oranges"
       results = self.UserModel.get(user_DNE) 
       ensure_data_packet_formatting(self, results, method, "error")
       print("test_get_user_DNE passed!")
    
    def test_get_all_many_users(self):
       method = "users.get_all"
       user_ids={}
       for i in range(len(self.users)):
            user_ids[self.users[i]['email']] = self.UserModel.create(self.users[i])["data"]["id"]

       all_users_info = self.UserModel.get_all()
       ensure_data_packet_formatting(self, all_users_info, method, "success")
       self.assertTrue(len(all_users_info['data'])==len(self.users), f"{method} - should return a list of length {len(self.users)} for many users")
       
       returned_users = all_users_info['data']
       returned_users.sort(key=lambda user: user['username']) #ensure both lists are sorted alphabetically by username

       for i in range(len(returned_users)):
            self.assertEqual(returned_users[i]["id"], user_ids[self.users[i]["email"]], f"{method}- returned id should match id of original user")
            self.assertEqual(returned_users[i]["email"], self.users[i]["email"], f"{method}- returned email should match id of original user")
            self.assertEqual(returned_users[i]["username"], self.users[i]["username"], f"{method}- returned username should match id of original user")    
            self.assertEqual(returned_users[i]["password"], self.users[i]["password"], f"{method}- returned password should match id of original user")
       
       #DB entity correctly updated
       try:  #check DB state
            db_connection = sqlite3.connect(self.yahtzee_db_name)
            cursor = db_connection.cursor()
            query = f"SELECT * from {self.table_name};"
            results = cursor.execute(query)
            all_users = results.fetchall()
           
            self.assertEqual(len(all_users), len(self.users), f"{method} a {len(self.users)} users should be returned")
            print("test_get_all_many_users passed!")
       except sqlite3.Error as error:
            print(error)
       finally:
            db_connection.close()
       
    def test_get_all_one_user(self):
       method = "users.get_all"
       original_user = self.users[3]
       original_user_in_DB = self.UserModel.create(original_user)["data"]
       all_users_info = self.UserModel.get_all()
       ensure_data_packet_formatting(self, all_users_info, method, "success")
       self.assertTrue(len(all_users_info['data'])==1, f"{method} - should return a list of length 1 for one users")
       
       returned_user = all_users_info['data'][0]
       self.assertEqual(returned_user["email"], original_user["email"], f"{method}- returned email should match data of original info")
       self.assertEqual(returned_user["username"], original_user["username"], f"{method}- returned username should match data of original infor")    
       self.assertEqual(returned_user["password"], original_user["password"], f"{method}- returned password should match data of original info")
       #DB entity correctly updated
       try:  #check DB state
            db_connection = sqlite3.connect(self.yahtzee_db_name)
            cursor = db_connection.cursor()
            query = f"SELECT * from {self.table_name};"
            results = cursor.execute(query)
            all_users = results.fetchall()
           
            self.assertEqual(len(all_users), 1, f"{method} a single user should be returned")
            self.assertEqual(all_users[0][1], returned_user["email"], f"{method}- Data of DB user should match data of added user")
            self.assertEqual(all_users[0][2], returned_user["username"], f"{method}- Data of DB user should match data of added user")    
            self.assertEqual(all_users[0][3], returned_user["password"], f"{method}- Data of DB user should match data of added user")
            print("test_get_all_one user passed!")
       
       except sqlite3.Error as error:
            print(error)
       finally:
            db_connection.close()

    def test_get_all_no_users(self):
       method = "users.get_all"
       all_users_info = self.UserModel.get_all()
       ensure_data_packet_formatting(self, all_users_info, method, "success")
       self.assertTrue(len(all_users_info['data'])==0, f"{method} - should return a list of length 0 for no users")
       try:  #check DB state
            db_connection = sqlite3.connect(self.yahtzee_db_name)
            cursor = db_connection.cursor()
            query = f"SELECT * from {self.table_name};"
            results = cursor.execute(query)
            all_users = results.fetchall()
           
            self.assertEqual(len(all_users), 0, f"{method} a no users should be returned")
            print("test_get_all_no_user passed!")
      
       except sqlite3.Error as error:
            print(error)
       finally:
            db_connection.close()

    def test_update_1_change(self):
        method = "users.update"
        
        results = []
        for i in range(len(self.users)):#add 4 users to the DB
            results.append(self.UserModel.create(self.users[i])["data"]["username"])
        
        '''{"email":"zelda@trinityschoolnyc.org",
            "username":"princessZ",
            "password":"123TriniT"}'''
        original_user_info = self.UserModel.get(username=self.users[2]["username"])
        
        updated_user_info = {
            "id":original_user_info["data"]["id"],
            "email":"zelda@trinityschoolnyc.org", 
            "username":"princessZzzzzzz", #only change
            "password":"123TriniT"
        }
        returned_user = self.UserModel.update(updated_user_info)

        print(updated_user_info, returned_user)
        
        ensure_data_packet_formatting(self, returned_user, method, "success")
        #returned object matches update information
        self.assertEqual(returned_user["data"]["email"], updated_user_info["email"], f"{method}- returned email should match data of updated info")
        self.assertEqual(returned_user["data"]["username"], updated_user_info["username"], f"{method}- returned username should match data of updated infor")    
        self.assertEqual(returned_user["data"]["password"], updated_user_info["password"], f"{method}- returned password should match data of updated info")
        #DB entity correctly updated
        try:  #check DB state
            db_connection = sqlite3.connect(self.yahtzee_db_name)
            cursor = db_connection.cursor()
            query = f"SELECT * from {self.table_name} WHERE id = {original_user_info['data']['id']};"
            results = cursor.execute(query)
            all_users = results.fetchall()
           
            self.assertEqual(len(all_users), 1, f"{method} a single user should be returned")
            self.assertEqual(all_users[0][1], updated_user_info["email"], f"{method}- Data of DB user should match data of added user")
            self.assertEqual(all_users[0][2], updated_user_info["username"], f"{method}- Data of DB user should match data of added user")    
            self.assertEqual(all_users[0][3], updated_user_info["password"], f"{method}- Data of DB user should match data of added user")
            print("test_update_1_change passed!")
        
        except sqlite3.Error as error:
            print(error)
        finally:
            db_connection.close()
       
    def test_update_many_changes(self):
        method = "users.update"
        
        results = []
        for i in range(len(self.users)):#add 4 users to the DB
            results.append(self.UserModel.create(self.users[i])["data"]["username"])

        '''{"email":"zelda@trinityschoolnyc.org",
            "username":"princessZ",
            "password":"123TriniT"}'''
        original_user_info = self.UserModel.get(username=self.users[2]["username"])
        
        updated_user_info = {
            "id":original_user_info["data"]["id"],
            "email":"princessZ@trinityschoolnyc.org", 
            "username":"princessZzzzzzz", 
            "password":"123TriniTy"
        }
        returned_user = self.UserModel.update(updated_user_info)
        
        ensure_data_packet_formatting(self, returned_user, method, "success")
        #returned object matches update information
        self.assertEqual(returned_user["data"]["email"], updated_user_info["email"], f"{method}- returned email should match data of updated info")
        self.assertEqual(returned_user["data"]["username"], updated_user_info["username"], f"{method}- returned username should match data of updated infor")    
        self.assertEqual(returned_user["data"]["password"], updated_user_info["password"], f"{method}- returned password should match data of updated info")
        #DB entity correctly updated
        try:  #check DB state
            db_connection = sqlite3.connect(self.yahtzee_db_name)
            cursor = db_connection.cursor()
            query = f"SELECT * from {self.table_name} WHERE id = {original_user_info['data']['id']};"
            results = cursor.execute(query)
            all_users = results.fetchall()
           
            self.assertEqual(len(all_users), 1, f"{method} a single user should be returned")
            self.assertEqual(all_users[0][1], updated_user_info["email"], f"{method}- Data of DB user should match data of added user")
            self.assertEqual(all_users[0][2], updated_user_info["username"], f"{method}- Data of DB user should match data of added user")    
            self.assertEqual(all_users[0][3], updated_user_info["password"], f"{method}- Data of DB user should match data of added user")
            print("test_update_many_changes passed!")
        
        except sqlite3.Error as error:
            print(error)
        finally:
            db_connection.close()
    
    def test_update_user_DNE(self):
        method = "users.update"
        new_user = {
            "id":8,
            "email":"asdfasdf@trinityschoolnyc.org", 
            "username":"asdfasdf", 
            "password":"123Trasdfasdf"
        }

        results = self.UserModel.update(new_user) # DB is empty
        ensure_data_packet_formatting(self, results, method, "error")
        print("test_update_user_DNE passed!")
    
    def test_update_username_email_already_exists(self):
        method = "users.update"
        
        results = []
        for i in range(len(self.users)):#add 4 users to the DB
            results.append(self.UserModel.create(self.users[i])["data"]["username"])
        
        '''{"email":"zelda@trinityschoolnyc.org",
            "username":"princessZ",
            "password":"123TriniT"}'''
        original_user_info = self.UserModel.get(username=self.users[2]["username"])
        
        updated_user_info = {
            "id":original_user_info["data"]["id"],
            "email":"zelda@trinityschoolnyc.org", 
            "username":self.users[0]["username"], #only change- username already exists
            "password":"123TriniT"
        }
        returned_user = self.UserModel.update(updated_user_info)
        ensure_data_packet_formatting(self, returned_user, method, "error")

        try:  #check DB state
            db_connection = sqlite3.connect(self.yahtzee_db_name)
            cursor = db_connection.cursor()
            query = f"SELECT * from {self.table_name} WHERE id = {original_user_info['data']['id']};"
            results = cursor.execute(query)
            all_users = results.fetchall()
           
            self.assertEqual(len(all_users), 1, f"{method} a single user should be returned")
            self.assertEqual(all_users[0][1], original_user_info["data"]["email"], f"{method}- Data of DB user should match data of added user")
            self.assertEqual(all_users[0][2], original_user_info["data"]["username"], f"{method}- Data of DB user should match data of added user")    
            self.assertEqual(all_users[0][3], original_user_info["data"]["password"], f"{method}- Data of DB user should match data of added user")
        
        except sqlite3.Error as error:
            print(error)
        finally:
            db_connection.close()
        
        updated_user_info = {
            "id":original_user_info["data"]["id"],
            "email":self.users[0]["email"], #only change- username already exists
            "username":"princessZ",
            "password":"123TriniT"
        }
        returned_user = self.UserModel.update(updated_user_info)
        ensure_data_packet_formatting(self, returned_user, method, "error")
        try:  #check DB state
            db_connection = sqlite3.connect(self.yahtzee_db_name)
            cursor = db_connection.cursor()
            query = f"SELECT * from {self.table_name} WHERE id = {original_user_info['data']['id']};"
            results = cursor.execute(query)
            all_users = results.fetchall()
           
            self.assertEqual(len(all_users), 1, f"{method} a single user should be returned")
            self.assertEqual(all_users[0][1], original_user_info["data"]["email"], f"{method}- Data of DB user should match data of added user")
            self.assertEqual(all_users[0][2], original_user_info["data"]["username"], f"{method}- Data of DB user should match data of added user")    
            self.assertEqual(all_users[0][3], original_user_info["data"]["password"], f"{method}- Data of DB user should match data of added user")
            print("test_update_username_email_already_exists passed!")
        
        except sqlite3.Error as error:
            print(error)
        finally:
            db_connection.close()
    
    def test_update_user_with_incorrect_data_format(self):
       method = "users.update"
       results = []
       for i in range(len(self.users)):#add 5 users to the DB
            results.append(self.UserModel.create(self.users[i])["data"]["username"])
        
       '''{"email":"zelda@trinityschoolnyc.org",
            "username":"princessZ",
            "password":"123TriniT"}'''
       original_user_info = self.UserModel.get(username=self.users[2]["username"])
    
       bad_user_data = [{"id":original_user_info["data"]["id"],
                        "email": "hi.com", 
                        "username":original_user_info["data"]["username"],
                        "password":original_user_info["data"]["password"]}, # bad email
                        {"id":original_user_info["data"]["id"],
                         "email": "hi@com", 
                        "username":original_user_info["data"]["username"],
                        "password":original_user_info["data"]["password"]},# bad email
                        {"id":original_user_info["data"]["id"],
                         "email": "hey_hey", 
                        "username":original_user_info["data"]["username"],
                        "password":original_user_info["data"]["password"]},# bad email
                        {"id":original_user_info["data"]["id"],
                         "email": "hey hey", 
                        "username":original_user_info["data"]["username"],
                        "password":original_user_info["data"]["password"]}, # bad email
                        {"id":original_user_info["data"]["id"],
                         "email": original_user_info["data"]["email"], 
                        "username":original_user_info["data"]["username"],
                        "password":"123"}, # password too short
                        {"id":original_user_info["data"]["id"],
                         "email": original_user_info["data"]["email"], 
                        "username":"something different",  # bad username
                        "password":original_user_info["data"]["password"]},
                        {"id":original_user_info["data"]["id"],
                         "email": original_user_info["data"]["email"], 
                        "username":"something@different",  # bad username
                        "password":original_user_info["data"]["password"]},
                        {"id":original_user_info["data"]["id"],
                         "email": original_user_info["data"]["email"], 
                        "username":"!something@different<>",  # bad username
                        "password":original_user_info["data"]["password"]}
                        ]
       for bad_user in bad_user_data:
            returned_user = self.UserModel.update(bad_user)
       
            ensure_data_packet_formatting(self, returned_user, method, "error")
            try:  #check DB state
                db_connection = sqlite3.connect(self.yahtzee_db_name)
                cursor = db_connection.cursor()
                query = f"SELECT * from {self.table_name} where id = {original_user_info['data']['id']};"
                results = cursor.execute(query)
                all_users = results.fetchall()
                self.assertEqual(all_users[0][1], original_user_info["data"]["email"], f"{method}- Data of DB user should match data of added user")
                self.assertEqual(all_users[0][2], original_user_info["data"]["username"], f"{method}- Data of DB user should match data of added user")    
                self.assertEqual(all_users[0][3], original_user_info["data"]["password"], f"{method}- Data of DB user should match data of added user")        
            except sqlite3.Error as error:
                print(error)
            finally:
                db_connection.close()
       print("test_create_user_with_incorrect_data_format passed!")
       
    def test_delete_user_exists(self):
        method = "users.remove"
        #add 4 users to the DB
        results = []
        for i in range(len(self.users)):
            results.append(self.UserModel.create(self.users[i])["data"]["username"])

        for username in results:
            results = self.UserModel.remove(username) 

            ensure_data_packet_formatting(self, results, method, "success")

            self.assertEqual(results["status"], "success", f"{method} should return error")
            self.assertEqual(results["data"]["username"], username, f"{method}- Data packet should of return user who was deleted")

            deleted_id = results["data"]["id"]
            try:  #check DB state
                db_connection = sqlite3.connect(self.yahtzee_db_name)
                cursor = db_connection.cursor()
                query = f"SELECT * from {self.table_name};"
                results = cursor.execute(query)

                for user in results.fetchall():
                    self.assertFalse(username==user[2], "Deleted username should not be present in the DB")
                    self.assertFalse(deleted_id==user[0], "Deleted user id should not be present in the DB")
            except sqlite3.Error as error:
                print(error)
            finally:
                db_connection.close()
        print("test_delete_user_exists passed!")
    
    def test_delete_user_DNE(self):
        method = "users.remove"
        user_DNE = "bananas"
        results = self.UserModel.remove(user_DNE) 
        ensure_data_packet_formatting(self, results, method, "error")
        print("test_delete_user_DNE passed!")
   
if __name__ == '__main__':
    unittest.main() 