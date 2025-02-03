import unittest
import sqlite3
import os
import datetime

from Models.Game_Model import Game
from Models.User_Model import User

def ensure_data_packet_formatting(self, packet, method, status):
    if status == "success":
        #format of returned data packet
        self.assertTrue("status" in packet, f"{method} should return a data packet object in the correct format")
        self.assertEqual(packet["status"], "success", f"{method} should return success")
        self.assertTrue("data" in packet, f"{method} should return a data packet object in the correct format")
        if type(packet['data']) == dict:
            self.assertTrue("id" in packet["data"], f"{method} should return a data packet object in the correct format")
            self.assertTrue("name" in packet["data"], f"{method} should return a data packet object in the correct format")
            self.assertTrue("created" in packet["data"], f"{method} should return a data packet object in the correct format")
            self.assertTrue("finished" in packet["data"], f"{method} should return a data packet object in the correct format")
        elif type(packet['data']) == list:
            for game in packet['data']:
                self.assertTrue("id" in game, f"{method} should return a data packet object in the correct format")
                self.assertTrue("name" in game, f"{method} should return a data packet object in the correct format")
                self.assertTrue("created" in game, f"{method} should return a data packet object in the correct format")
                self.assertTrue("finished" in game, f"{method} should return a data packet object in the correct format")
    elif status  == "error":
        self.assertEqual(packet["status"], "error", f"{method} should return error")
        self.assertTrue(len(packet["data"]) > 10 , f"{method}- Data packet should return an error message of significant length")

class Game_Model_Tests(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        #Runs once, before any tests are run
        self.yahtzee_db_name=f"{os.getcwd()}/Models/yahtzeeDB.db"
        self.games_table_name = "games"
        self.users_table_name = "users"
        self.UserModel = User(self.yahtzee_db_name, self.users_table_name)
        self.GameModel = Game(self.yahtzee_db_name, self.games_table_name)
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
        self.games =[]
        for i in range(5):
            self.games.append({"name":f"ourGame{i}"})

    def setUp(self):
        #Runs before every test
        self.UserModel.initialize_table() #start with a fresh database for every test
        self.GameModel.initialize_table() #start with a fresh database for every test

        self.user_ids={} #add 4 users and keep track of their ids
        for i in range(len(self.users)):
            user_info = self.UserModel.create(self.users[i])
            self.user_ids[self.users[i]['email']] = user_info["data"]["id"]

    def test_create_1_game(self):
        method = "games.create"
        #invoke method
        returned_game=self.GameModel.create(self.games[0])
        #check returned object
        ensure_data_packet_formatting(self, returned_game, method, "success")
        self.assertEqual(returned_game["data"]["name"], self.games[0]["name"])
        
        try:  #check DB state
            db_connection = sqlite3.connect(self.yahtzee_db_name)
            cursor = db_connection.cursor()
            query = f"SELECT * from {self.games_table_name};"
            results = cursor.execute(query)
            DB_game = results.fetchall()
            self.assertTrue(len(DB_game)==1, f"{method} should add exactly 1 new game")
            self.assertEqual(DB_game[0][1], returned_game["data"]["name"], f"{method} DB game data should match returend game")
            self.assertEqual(DB_game[0][2], returned_game["data"]["created"], f"{method} DB game data should match returend game")
            self.assertEqual(DB_game[0][3], returned_game["data"]["finished"], f"{method} DB game data should match returend game")
            print("test_create_1_game passed!")
        except sqlite3.Error as error:
            print(error)
        finally:
            db_connection.close()
    
    def test_create_many_games(self):
        method = "games.create"
        
        returned_games = {}
        for i in range(4):
            game = self.GameModel.create(self.games[i])
            ensure_data_packet_formatting(self, game, method, "success")
            returned_games[game['data']["name"]] = game["data"] #game name maps to game object
       
        for i in range(4): #game_name is a key in the returned games ditionary
            self.assertTrue(self.games[i]['name'] in returned_games)
        
        try:  #check DB state
            db_connection = sqlite3.connect(self.yahtzee_db_name)
            cursor = db_connection.cursor()
            query = f"SELECT * from {self.games_table_name};"
            results = cursor.execute(query)
            DB_games = results.fetchall()
            self.assertTrue(len(DB_games)==4, f"{method} should add exactly 4 new games")
            for DB_game in DB_games:
                name = DB_game[1]
                self.assertEqual(DB_game[0], returned_games[name]["id"], f"{method} DB game data should match returend game")
                self.assertEqual(DB_game[1], returned_games[name]["name"], f"{method} DB game data should match returend game")
                self.assertEqual(DB_game[2], returned_games[name]["created"], f"{method} DB game data should match returend game")
                self.assertEqual(DB_game[3], returned_games[name]["finished"], f"{method} DB game data should match returend game")
            print("\ntest_create_many_games passed!")
        except sqlite3.Error as error:
            print(error)
        finally:
            db_connection.close()
    
    def test_create_game_already_taken_name(self):
        method = "games.create"
        #setup - Create 4 games
        returned_games = {}
        for i in range(4):
            game = self.GameModel.create(self.games[i])
            returned_games[game['data']["name"]] = game["data"] #game name maps to game object
       
        #invoke method
        new_game={"name":self.games[2]['name']}
        returned_game = self.GameModel.create(new_game)
        #check returned object
        ensure_data_packet_formatting(self, returned_game, method, "error")

        #check DB state
        try: 
            db_connection = sqlite3.connect(self.yahtzee_db_name)
            cursor = db_connection.cursor()
            query = f"SELECT * from {self.games_table_name};"
            results = cursor.execute(query)
            all_games = results.fetchall()
            self.assertTrue(len(all_games)==4)
            print("test_create_game_already_taken_name passed!")        
        except sqlite3.Error as error:
            print(error)
        finally:
            db_connection.close()
    
    def test_create_game_incorrect_format(self):
        method = "games.create"
        #setup
        #setup - Create 4 games
        returned_games = {}
        for i in range(4):
            game = self.GameModel.create(self.games[i])
            returned_games[game['data']["name"]] = game["data"] #game name maps to game object
       
        bad_game_data = [{"name": "hi.com"}, 
                         {"name": "hi com"}, 
                         {"name": "hi!com"}, 
                         {"name": "hi@haveaniceday"}]
        #invoke method
        for game in bad_game_data:
            #invoke method
            new_game={"name":game['name']}
            returned_game = self.GameModel.create(new_game)
            #check returned object
            ensure_data_packet_formatting(self, returned_game, method, "error")
        
            #check DB state
            try: 
                db_connection = sqlite3.connect(self.yahtzee_db_name)
                cursor = db_connection.cursor()
                query = f"SELECT * from {self.games_table_name};"
                results = cursor.execute(query)
                all_games = results.fetchall()
                self.assertTrue(len(all_games)==4)
            except sqlite3.Error as error:
                print(error)
            finally:
                db_connection.close()
        print("test_create_game_incorrect_format passed!")  

    def test_game_exists(self):
        method = "games.exist"
        #setup - Create 4 games
        returned_games = {}
        for i in range(len(self.games)):
            game = self.GameModel.create(self.games[i])
            returned_games[game['data']["name"]] = game["data"] #game name maps to game object
       
        for game in self.games:
            returned_game = self.GameModel.exists(game["name"])
            ensure_data_packet_formatting(self, returned_game, method, "success")
            self.assertTrue(returned_game["data"])
        
        print("test_game_exists passed!") 
               
    def test_game_exists_DNE(self):
        method = "games.exist"
        #setup - Create 4 games
        for game in self.games:
            returned_game = self.GameModel.exists(game["name"])
            ensure_data_packet_formatting(self, returned_game, method, "success")
            self.assertFalse(returned_game["data"])
        
        print("test_game_exists_DNE passed!") 
    
    def test_get_game_exists_id(self):
        method = "games.get"
        #setup - Create 4 games
        original_games = {}
        for i in range(len(self.games)):
            game = self.GameModel.create(self.games[i])
            original_games[game['data']["name"]] = game["data"] #game name maps to game object
       
        for game in self.games:
            returned_game = self.GameModel.get(id = original_games[game["name"]]["id"])

            game_name = returned_game['data']['name']
            ensure_data_packet_formatting(self, returned_game, method, "success")
            self.assertEqual(returned_game["data"], original_games[game_name])
        
        print("test_get_game_exists_id passed!") 

    def test_get_game_exists_game_name(self):
        method = "games.get"
        #setup - Create 4 games
        original_games = {}
        for i in range(len(self.games)):
            game = self.GameModel.create(self.games[i])
            original_games[game['data']["name"]] = game["data"] #game name maps to game object
       
        for game in self.games:
            returned_game = self.GameModel.get(game_name = game["name"])
            game_name = returned_game['data']['name']
            ensure_data_packet_formatting(self, returned_game, method, "success")
            self.assertEqual(returned_game["data"],original_games[game_name])
        
        print("test_get_game_exists_name passed!") 

    def test_get_game_DNE(self):
        method = "games.get"
        for game in self.games:
            returned_game = self.GameModel.get(game_name=game["name"])
            ensure_data_packet_formatting(self, returned_game, method, "error")
        print("test_get_game_DNE passed!") 

    def test_get_all_games_no_games(self):
        method = "games.get_all"
        
        returned_games = self.GameModel.get_all()
        ensure_data_packet_formatting(self, returned_games, method, "success")
        self.assertTrue(len(returned_games["data"])==0)
        print("test_get_all_games_no_games passed!")
    
    def test_get_all_games_1_game(self):
        method = "games.get_all"
        #setup
        original_game = self.GameModel.create(self.games[1])
        #invoke method
        returned_games = self.GameModel.get_all()
        ensure_data_packet_formatting(self, returned_games, method, "success")
        self.assertTrue(len(returned_games["data"])==1)
        self.assertEqual(returned_games["data"][0], original_game["data"])
        print("test_get_all_games_1_game passed!")

    def test_get_all_games_many_games(self):
        method = "games.get_all"
        #setup
        original_games = {}
        for i in range(len(self.games)):
            game = self.GameModel.create(self.games[i])
            original_games[game['data']["name"]] = game["data"] #game name maps to game object
               
        returned_games = self.GameModel.get_all()
        ensure_data_packet_formatting(self, returned_games, method, "success")
        self.assertTrue(len(returned_games["data"])==len(self.games))

        for game in returned_games['data']:
            self.assertEqual(game, original_games[game["name"]])
        
        print("test_get_all_games_many_games passed!")

    def test_update_game_name_change(self):
        method = "games.update"
        original_games = {}
        for i in range(len(self.games)):
            game = self.GameModel.create(self.games[i])
            original_games[game['data']["name"]] = game["data"] #game name maps to game object
              
        updated_game = original_games[self.games[3]["name"]]
        updated_game["name"]="my_new_game_name"
        returned_games = self.GameModel.update(updated_game)

        ensure_data_packet_formatting(self, returned_games, method, "success")
        self.assertEqual(returned_games["data"], updated_game)
        
        #check DB state
        try: 
            db_connection = sqlite3.connect(self.yahtzee_db_name)
            cursor = db_connection.cursor()
            query = f"SELECT * from {self.games_table_name} WHERE id={updated_game['id']};"
            results = cursor.execute(query)
            game = results.fetchone()
            self.assertEqual(game[1],updated_game['name'] )
            self.assertEqual(game[2],updated_game['created'])
            self.assertEqual(game[3],updated_game['finished'])
            print("test_update_game_name_change passed!")          
        except sqlite3.Error as error:
            print(error)
        finally:
            db_connection.close()
    
    def test_update_game_name_change_already_taken(self):
        method = "games.update"
        original_games = {}
        for i in range(len(self.games)):
            game = self.GameModel.create(self.games[i])
            original_games[game['data']["name"]] = game["data"] #game name maps to game object
              
        original_game = original_games[self.games[3]["name"]]
        updated_game = original_game.copy()
        updated_game["name"]=self.games[2]["name"] #already exists
        returned_games = self.GameModel.update(updated_game)
        ensure_data_packet_formatting(self, returned_games, method, "error")
        
        #check DB state
        try: 
            db_connection = sqlite3.connect(self.yahtzee_db_name)
            cursor = db_connection.cursor()
            query = f"SELECT * from {self.games_table_name} WHERE id={updated_game['id']};"
            results = cursor.execute(query)
            game = results.fetchone()
            self.assertEqual(game[1],original_game['name'] )
            self.assertEqual(game[2],original_game['created'])
            self.assertEqual(game[3],original_game['finished'])
            print("test_update_game_name_change_already_taken passed!")          
        except sqlite3.Error as error:
            print(error)
        finally:
            db_connection.close()

    def test_update_game_finish_change(self):
        method = "games.update"
        original_games = {}
        for i in range(len(self.games)):
            game = self.GameModel.create(self.games[i])
            original_games[game['data']["name"]] = game["data"] #game name maps to game object
              
        updated_game = original_games[self.games[3]["name"]]
        updated_game["finished"]=str(datetime.datetime.now())
         
        returned_game = self.GameModel.update(updated_game)
         
        print(returned_game)

        ensure_data_packet_formatting(self, returned_game, method, "success")
        self.assertEqual(returned_game["data"], updated_game)
        
        #check DB state
        try: 
            db_connection = sqlite3.connect(self.yahtzee_db_name)
            cursor = db_connection.cursor()
            query = f"SELECT * from {self.games_table_name} WHERE id={updated_game['id']};"
            results = cursor.execute(query)
            game = results.fetchone()
            self.assertEqual(game[1],updated_game['name'] )
            self.assertEqual(game[2],updated_game['created'])
            self.assertEqual(game[3],updated_game['finished'])
            print("test_update_game_finish_change passed!")          
        except sqlite3.Error as error:
            print(error)
        finally:
            db_connection.close()
    
    def test_update_game_DNE(self):
        method = "games.update"
        
        updated_game = {
            "id": 1,
            "name": "game_that_DNE",
            "created":str(datetime.datetime.now()),
            "finished":str(datetime.datetime.now())
        }
        returned_games = self.GameModel.update(updated_game) #no games in table
        ensure_data_packet_formatting(self, returned_games, method, "error")
        
        #check DB state
        try: 
            db_connection = sqlite3.connect(self.yahtzee_db_name)
            cursor = db_connection.cursor()
            query = f"SELECT * from {self.games_table_name} WHERE id={updated_game['id']};"
            results = cursor.execute(query)
            game = results.fetchall()
            self.assertTrue(len(game)==0) #DB is still empty
            print("test_update_game_DNE passed!")          
        except sqlite3.Error as error:
            print(error)
        finally:
            db_connection.close()
    
    def test_remove_game_DNE(self):
        method = "games.remove"
        
        returned_games = self.GameModel.remove("game_that_DNE") #no games in table
        ensure_data_packet_formatting(self, returned_games, method, "error")
        print("test_remove_game_DNE passed!")
    
    def test_remove_game_exists(self):
        method = "games.remove"
        
        returned_games = {}
        for i in range(len(self.games)):
            game = self.GameModel.create(self.games[i])
            ensure_data_packet_formatting(self, game, method, "success")
            returned_games[game['data']["name"]] = game["data"] #game name maps to game object
       
        deleted_game = self.GameModel.remove(self.games[0]["name"])
         
        ensure_data_packet_formatting(self, deleted_game, method, "success")
        self.assertEqual(deleted_game["data"]["name"], returned_games[self.games[0]["name"]]["name"])

        try:  #check DB state
            db_connection = sqlite3.connect(self.yahtzee_db_name)
            cursor = db_connection.cursor()
            query = f"SELECT * from {self.games_table_name};"
            results = cursor.execute(query)
            DB_games = results.fetchall()
            self.assertEqual(len(DB_games), len(self.games)-1, f"{method} should add exactly {len(self.games)-1} new games")
            for DB_game in DB_games:
                self.assertNotEqual(DB_game[1], deleted_game["data"]["name"], f"{method} DB game data should not match deleted game name")

            print("test_remove_game_exists passed!")
        except sqlite3.Error as error:
            print(error)
        finally:
            db_connection.close()

    def test_is_finished_with_finished_game(self):
        method = "games.is_finished"
        
        original_games = {}
        for i in range(len(self.games)):
            game = self.GameModel.create(self.games[i])
            original_games[game['data']["name"]] = game["data"] #game name maps to game object
            
        updated_game = original_games[self.games[3]["name"]]
        updated_game["finished"]=str(datetime.datetime.now())

         
        returned_game = self.GameModel.update(updated_game)
        print("testing game finished")
        print(game, returned_game)
        
        packet = self.GameModel.is_finished(updated_game["name"])
        self.assertTrue("status" in packet, f"{method} should return a data packet object in the correct format")
        self.assertEqual(packet["status"], "success", f"{method} should return success")
        self.assertTrue("data" in packet, f"{method} should return a data packet object in the correct format")
        self.assertTrue(packet["data"]) # game is finished
    
        print("test_is_finished_with_finished_game passed!")

    def test_is_finihed_with_unfinished_game(self):
        method = "games.is_finished"
        
        games = []
        for i in range(4):
            game = self.GameModel.create(self.games[i])
            games.append(game["data"]) 
       
        for game in games: 
            packet = self.GameModel.is_finished(game["name"])
            self.assertTrue("status" in packet, f"{method} should return a data packet object in the correct format")
            self.assertEqual(packet["status"], "success", f"{method} should return success")
            self.assertTrue("data" in packet, f"{method} should return a data packet object in the correct format")
            self.assertFalse(packet["data"]) # game is not finished
        
        print("test_is_finihed_with_unfinished_game passed!")

if __name__ == '__main__':
    unittest.main() 