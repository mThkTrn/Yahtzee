import unittest
import sqlite3
import os
import json

#test should inhabit the same folder
from GameModel import Game
from UserModel import User
from ScorecardModel import Scorecard

def ensure_data_packet_formatting(self, packet, method, status):
    if status == "success":
        #format of returned data packet
        self.assertTrue("status" in packet, f"{method} should return a data packet object in the correct format")
        self.assertEqual(packet["status"], "success", f"{method} should return success")
        self.assertTrue("data" in packet, f"{method} should return a data packet object in the correct format")
        if type(packet['data']) == dict:
            self.assertTrue("id" in packet["data"], f"{method} should return a data packet object in the correct format")
            self.assertTrue("game_id" in packet["data"], f"{method} should return a data packet object in the correct format")
            self.assertTrue("user_id" in packet["data"], f"{method} should return a data packet object in the correct format")
            self.assertTrue("categories" in packet["data"], f"{method} should return a data packet object in the correct format")
            self.assertTrue("turn_order" in packet["data"], f"{method} should return a data packet object in the correct format")
            self.assertTrue("name" in packet["data"], f"{method} should return a data packet object in the correct format")
            self.assertTrue("|" in packet["data"]["name"], f"{method} should return a data packet object in the correct format")
            game = self.GameModel.get(id=packet["data"]["game_id"])
            game_name = game["data"]["name"]
            self.assertEqual(packet["data"]["name"].split("|")[0], game_name, f"{method} should return a data packet object in the correct format")
            user_name = self.UserModel.get(id=packet["data"]["user_id"])["data"]["username"]
            self.assertEqual(packet["data"]["name"].split("|")[1], user_name, f"{method} should return a data packet object in the correct format")
        elif type(packet['data']) == list:
            for game in packet['data']:
                self.assertTrue("id" in game, f"{method} should return a data packet object in the correct format")
                self.assertTrue("game_id" in game, f"{method} should return a data packet object in the correct format")
                self.assertTrue("user_id" in game, f"{method} should return a data packet object in the correct format")
                self.assertTrue("categories" in game, f"{method} should return a data packet object in the correct format")
                self.assertTrue("turn_order" in game, f"{method} should return a data packet object in the correct format")
                self.assertTrue("name" in game, f"{method} should return a data packet object in the correct format")
                self.assertTrue("|" in game["name"], f"{method} should return a data packet object in the correct format")
                game_name = self.GameModel.get(id=game["game_id"])["data"]["name"]
                self.assertEqual(game["name"].split("|")[0], game_name, f"{method} should return a data packet object in the correct format")
                user_name = self.UserModel.get(id=game["user_id"])["data"]["username"]
                self.assertEqual(game["name"].split("|")[1], user_name, f"{method} should return a data packet object in the correct format")
    elif status  == "error":
        self.assertEqual(packet["status"], "error", f"{method} should return error")
        self.assertTrue(len(packet["data"]) > 10 , f"{method}- Data packet should return an error message of significant length")

class Scorecard_Model_Tests(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        #Runs once, before any tests are run
        self.yahtzee_db_name=f"{os.getcwd()}/Models/yahtzeeDB.db"
        self.scorecard_table_name = "scorecards"
        self.user_table_name = "users"
        self.game_table_name = "games"
        self.UserModel = User(self.yahtzee_db_name, self.user_table_name)
        self.GameModel = Game(self.yahtzee_db_name, self.game_table_name)   
        self.ScorecardModel = Scorecard(self.yahtzee_db_name, self.scorecard_table_name, self.user_table_name, self.game_table_name)     
        self.users_info=[{"email":"cookie.monster@trinityschoolnyc.org",
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
        self.users_tuples = [(user["email"], user["username"], user["password"]) for user in self.users_info]
        self.users_tuples.sort(key=lambda user: user[0])
        self.games_info =[]
        for i in range(12):
            self.games_info.append({"name":f"test_Game_{i}"})

    def setUp(self):
        #Runs before every test
        self.UserModel.initialize_table() #start with a fresh database for every test
        self.GameModel.initialize_table() #start with a fresh database for every test    
        self.ScorecardModel.initialize_table() #start with a fresh database for every test
        
        self.users={} #add 4 users and keep track of their ids
        for i in range(len(self.users_info)):
            user = self.UserModel.create(self.users_info[i])
            self.users[self.users_info[i]['email']] = user["data"]

        self.games={} #add 4 users and keep track of their ids
        for i in range(len(self.games_info)):
            game = self.GameModel.create(self.games_info[i])
            self.games[self.games_info[i]['name']] = game["data"]
        
        self.blank_scorecard ={
            "dice_rolls":0,
            "upper":{
                "ones":-1,
                "twos":-1,
                "threes":-1,
                "fours":-1,
                "fives":-1,
                "sixes":-1
            },
            "lower":{
                "three_of_a_kind":-1,
                "four_of_a_kind":-1,
                "full_house":-1,
                "small_straight":-1,
                "large_straight":-1,
                "yahtzee":-1,
                "chance":-1
            }
        }
        self.partial_card={
            "rolls_remaining":2,
            "upper":{
                "one":4,
                "two":8,
                "three":-1,
                "four":-1,
                "five":-1,
                "six":24
            },
            "lower":{
                "three_of_a_kind":-1,
                "four_of_a_kind":26,
                "full_house":-1,
                "small_straight":0,
                "large_straight":40,
                "yahtzee":0,
                "chance":8
            }
        }

    def test_create_1_scorecard(self):
        method = "scorecard.create"
        user = list(self.users.values())[0]
        game = list(self.games.values())[0]
        new_scorecard = self.ScorecardModel.create(game["id"], user["id"], game["name"]+"|"+user["username"])
        ensure_data_packet_formatting(self, new_scorecard, method, "success")
        self.assertEqual(new_scorecard["data"]["user_id"], user["id"])
        self.assertEqual(new_scorecard["data"]["game_id"], game["id"])
        self.assertEqual(new_scorecard["data"]["categories"], self.blank_scorecard)
        self.assertEqual(new_scorecard["data"]["turn_order"], 1)
        
        try: 
            db_connection = sqlite3.connect(self.yahtzee_db_name)
            cursor = db_connection.cursor()
            query = f"SELECT * from {self.scorecard_table_name};"
            results = cursor.execute(query)
            scorecards = results.fetchall()
            # print("Scorecards:")
            # print(scorecards)
            # print("___")
            self.assertTrue(len(scorecards)==1)
            self.assertEqual(scorecards[0][0], new_scorecard["data"]["id"])
            self.assertEqual(scorecards[0][1], game["id"])
            self.assertEqual(scorecards[0][2], user["id"])
            self.assertEqual(scorecards[0][3], json.dumps(self.blank_scorecard))
            self.assertEqual(scorecards[0][4], 1)
            self.assertEqual(scorecards[0][5], game["name"]+"|"+user["username"])
            print("test_create_1_scorecard passed!")  
        except sqlite3.Error as error:
            print(error)
        finally:
            db_connection.close()
    
    def test_create_many_scorecards_different_games(self):
        method="scorecard.create"
        all_scorecards = []
        for i in range(len(self.users)):
            user = list(self.users.values())[i]
            game = list(self.games.values())[i]
 
            new_scorecard = self.ScorecardModel.create(game["id"], user["id"], game["name"]+"|"+user["username"])
             
            ensure_data_packet_formatting(self, new_scorecard, method, "success")
            self.assertEqual(new_scorecard["data"]["user_id"], user["id"])
            self.assertEqual(new_scorecard["data"]["game_id"], game["id"])
            self.assertEqual(new_scorecard["data"]["categories"], self.blank_scorecard)
            self.assertEqual(new_scorecard["data"]["turn_order"], 1)
            all_scorecards.append(new_scorecard["data"])
        all_scorecards.sort(key=lambda scorecard: scorecard["id"])

        try: 
            db_connection = sqlite3.connect(self.yahtzee_db_name)
            cursor = db_connection.cursor()
            query = f"SELECT * from {self.scorecard_table_name};"
            results = cursor.execute(query)
            scorecards = results.fetchall()

            self.assertTrue(len(scorecards)==len(self.users))
            for i in range(len(self.users)):
                self.assertEqual(scorecards[i][1], all_scorecards[i]["game_id"])
                self.assertEqual(scorecards[i][2], all_scorecards[i]["user_id"])
                self.assertEqual(scorecards[i][3], json.dumps(self.blank_scorecard))
                self.assertEqual(scorecards[i][4], 1)
                self.assertEqual(scorecards[i][5], all_scorecards[i]["name"])
            print("test_create_many_scorecards_different_games passed!")  
        except sqlite3.Error as error:
            print(error)
        finally:
            db_connection.close()
    
    def test_create_many_scorecards_same_game(self):
        method="scorecard.create"
        all_scorecards = []
        game = list(self.games.values())[0]

        for i in range(len(self.users)):
            user = list(self.users.values())[i]
            new_scorecard = self.ScorecardModel.create(game["id"], user["id"], game["name"]+"|"+user["username"])
             
            ensure_data_packet_formatting(self, new_scorecard, method, "success")
            self.assertEqual(new_scorecard["data"]["user_id"], user["id"])
            self.assertEqual(new_scorecard["data"]["game_id"], game["id"])
            self.assertEqual(new_scorecard["data"]["categories"], self.blank_scorecard)
            self.assertEqual(new_scorecard["data"]["turn_order"], i+1)
            all_scorecards.append(new_scorecard["data"])
        all_scorecards.sort(key=lambda scorecard: scorecard["id"])

        try: 
            db_connection = sqlite3.connect(self.yahtzee_db_name)
            cursor = db_connection.cursor()
            query = f"SELECT * from {self.scorecard_table_name};"
            results = cursor.execute(query)
            scorecards = results.fetchall()

            self.assertTrue(len(scorecards)==len(self.users))
            for i in range(len(self.users)):
                self.assertEqual(scorecards[i][1], all_scorecards[i]["game_id"])
                self.assertEqual(scorecards[i][2], all_scorecards[i]["user_id"])
                self.assertEqual(scorecards[i][3], json.dumps(self.blank_scorecard))
                self.assertEqual(scorecards[i][4], all_scorecards[i]["turn_order"])
                self.assertEqual(scorecards[i][5], all_scorecards[i]["name"])
            print("test_create_many_scorecards_same_game passed!")  
        except sqlite3.Error as error:
            print(error)
        finally:
            db_connection.close()
    
    def test_create_too_many_scorecards_same_game_different_users(self):
        method="scorecard.create"
        all_scorecards = []
        game = list(self.games.values())[0]

        for i in range(len(self.users)):
            user = list(self.users.values())[i]
            new_scorecard = self.ScorecardModel.create(game["id"], user["id"], game["name"]+"|"+user["username"])
            all_scorecards.append(new_scorecard["data"])
        all_scorecards.sort(key=lambda scorecard: scorecard["id"])
        
        new_user_info ={"email":"bowser_official@trinityschoolnyc.org",
                        "username":"bowser_official",
                        "password":"IamBOWSER4Real"}
        new_user = self.UserModel.create(new_user_info)['data']
        new_scorecard = self.ScorecardModel.create(game["id"], new_user["id"], game["name"]+"|"+new_user["username"])
        ensure_data_packet_formatting(self, new_scorecard, method, "error") #max of 4 players per game
        
        all_scorecards_returned = self.ScorecardModel.get_all()['data']
        self.assertTrue(len(all_scorecards_returned)==len(all_scorecards)) #scorecard has not been added to DB
        print("test_create_too_many_scorecards_same_game_different_users passed!")  

    def test_create_too_many_scorecards_same_game_same_user(self):
        method = "scorecard.create"
        user = list(self.users.values())[0]
        game = list(self.games.values())[0]
        new_scorecard_1 = self.ScorecardModel.create(game["id"], user["id"], game["name"]+"|"+user["username"])
        ensure_data_packet_formatting(self, new_scorecard_1, method, "success")
        #add new scorecard to same game with same user
        new_scorecard_2 = self.ScorecardModel.create(game["id"], user["id"], game["name"]+"|"+user["username"])
        ensure_data_packet_formatting(self, new_scorecard_2, method, "error")

        all_scorecards_returned = self.ScorecardModel.get_all()['data']
        self.assertTrue(len(all_scorecards_returned)==1) #scorecard has not been added to DB
        print("test_create_too_many_scorecards_same_game_same_user passed!")  
    
    def test_get_scorecard_exists_id(self):
        method = "scorecard.get"
        all_scorecards = []
        for i in range(len(self.users)):
            user = list(self.users.values())[i]
            game = list(self.games.values())[i]
            new_scorecard = self.ScorecardModel.create(game["id"], user["id"], game["name"]+"|"+user["username"])
            all_scorecards.append(new_scorecard["data"]) 

        for card in all_scorecards:
            returned_scorecard = self.ScorecardModel.get(id=card["id"])
            ensure_data_packet_formatting(self, returned_scorecard, method, "success")
            self.assertEqual(returned_scorecard["data"]["id"], card["id"])
            self.assertEqual(returned_scorecard["data"]["user_id"], card["user_id"])
            self.assertEqual(returned_scorecard["data"]["game_id"], card["game_id"])
            self.assertEqual(returned_scorecard["data"]["categories"], card["categories"])
            self.assertEqual(returned_scorecard["data"]["turn_order"], card["turn_order"])
        print("test_get_scorecard_exists_id passed!") 
    
    def test_get_scorecard_exists_name(self):
        method = "scorecard.get"
        all_scorecards = []
        for i in range(len(self.users)):
            user = list(self.users.values())[i]
            game = list(self.games.values())[i]
            new_scorecard = self.ScorecardModel.create(game["id"], user["id"], game["name"]+"|"+user["username"])
            all_scorecards.append(new_scorecard["data"]) 
        
        for card in all_scorecards:
            returned_scorecard = self.ScorecardModel.get(name=card["name"])
            ensure_data_packet_formatting(self, returned_scorecard, method, "success")
            self.assertEqual(returned_scorecard["data"]["id"], card["id"])
            self.assertEqual(returned_scorecard["data"]["user_id"], card["user_id"])
            self.assertEqual(returned_scorecard["data"]["game_id"], card["game_id"])
            self.assertEqual(returned_scorecard["data"]["categories"], card["categories"])
            self.assertEqual(returned_scorecard["data"]["turn_order"], card["turn_order"])
        print("test_get_scorecard_exists_name passed!") 
    
    def test_get_scorecard_DNE(self):
        method = "scorecard.get"
        returned_scorecard = self.ScorecardModel.get(name="hello|Tigers")
        ensure_data_packet_formatting(self, returned_scorecard, method, "error")
        returned_scorecard = self.ScorecardModel.get(id=1234567)
        ensure_data_packet_formatting(self, returned_scorecard, method, "error")
        print("test_get_scorecard_DNE passed!") 
    
    def test_get_all_no_scorecards(self):
        method = "scorecard.get_all"
        returned_scorecards = self.ScorecardModel.get_all()
        ensure_data_packet_formatting(self, returned_scorecards, method, "success")
        self.assertEqual(len(returned_scorecards["data"]), 0)

        print("test_get_all_no_scorecards passed!") 
    
    def test_get_all_1_scorecard(self):
        method = "scorecard.get_all"
        user = list(self.users.values())[0]
        game = list(self.games.values())[0]
        new_scorecard = self.ScorecardModel.create(game["id"], user["id"], game["name"]+"|"+user["username"])["data"]
        
        returned_scorecards = self.ScorecardModel.get_all()
        ensure_data_packet_formatting(self, returned_scorecards, method, "success")
        self.assertEqual(len(returned_scorecards["data"]), 1)
        self.assertEqual(returned_scorecards["data"][0]["id"], new_scorecard["id"])
        self.assertEqual(returned_scorecards["data"][0]["user_id"], new_scorecard["user_id"])
        self.assertEqual(returned_scorecards["data"][0]["game_id"], new_scorecard["game_id"])
        self.assertEqual(returned_scorecards["data"][0]["categories"], new_scorecard["categories"])
        self.assertEqual(returned_scorecards["data"][0]["turn_order"], new_scorecard["turn_order"])
        print("test_get_all_1_scorecard passed!") 
        
    def test_get_all_many_scorecards(self):
        method = "scorecard.get_all"
        all_scorecards=[]
        game = list(self.games.values())[0]
        for i in range(len(self.users)):
            user = list(self.users.values())[i]
            new_scorecard = self.ScorecardModel.create(game["id"], user["id"], game["name"]+"|"+user["username"])
            all_scorecards.append(new_scorecard["data"])  
        all_scorecards.sort(key=lambda card: card["id"])

        returned_scorecards = self.ScorecardModel.get_all()
        ensure_data_packet_formatting(self, returned_scorecards, method, "success")
        self.assertEqual(len(returned_scorecards["data"]), len(all_scorecards))
        
        returned_scorecards["data"].sort(key=lambda card: card["id"])
        for i in range(len(returned_scorecards["data"])):
            self.assertEqual(returned_scorecards["data"][i]["id"], all_scorecards[i]["id"])
            self.assertEqual(returned_scorecards["data"][i]["user_id"], all_scorecards[i]["user_id"])
            self.assertEqual(returned_scorecards["data"][i]["game_id"], all_scorecards[i]["game_id"])
            self.assertEqual(returned_scorecards["data"][i]["categories"], all_scorecards[i]["categories"])
            self.assertEqual(returned_scorecards["data"][i]["turn_order"], all_scorecards[i]["turn_order"])
        print("test_get_all_many_scorecards passed!")  

    def test_get_all_game_scorecards_no_scorecards(self):
        method = "scorecard._game_scorecards"
        #no games
        all_game_scorecards = self.ScorecardModel.get_all_game_scorecards(game_name='fake_game_DNE')
        ensure_data_packet_formatting(self, all_game_scorecards, method, "success")
        self.assertEqual(len(all_game_scorecards["data"]), 0)
        #4 games
        for i in range(len(self.users)):
            user = list(self.users.values())[i]
            game = list(self.games.values())[i]
            new_scorecard = self.ScorecardModel.create(game["id"], user["id"], game["name"]+"|"+user["username"])
        all_game_usernames = self.ScorecardModel.get_all_game_scorecards(game_name='fake_game_DNE')
        print(all_game_usernames)
        ensure_data_packet_formatting(self, all_game_usernames, method, "success")
        self.assertEqual(len(all_game_usernames["data"]), 0)
        print("test_get_all_game_scorecards_no_scorecards passed!") 
           
    def test_get_all_game_scorecards_1_scorecard(self):
        method = "scorecard._game_scorecards"
        all_scorecards = {}
        for i in range(len(self.users)):
            user = list(self.users.values())[i]
            game = list(self.games.values())[i]
            new_scorecard = self.ScorecardModel.create(game["id"], user["id"], game["name"]+"|"+user["username"])
            all_scorecards[game["name"]] = new_scorecard["data"]
        
        game_name_to_get = list(self.games.values())[0]["name"]
        all_game_scorecards = self.ScorecardModel.get_all_game_scorecards(game_name=game_name_to_get)
        ensure_data_packet_formatting(self, all_game_scorecards, method, "success")
        self.assertEqual(len(all_game_scorecards["data"]), 1)
        self.assertEqual(all_game_scorecards["data"][0]["id"], all_scorecards[game_name_to_get]["id"])
        self.assertEqual(all_game_scorecards["data"][0]["user_id"], all_scorecards[game_name_to_get]["user_id"])
        self.assertEqual(all_game_scorecards["data"][0]["game_id"], all_scorecards[game_name_to_get]["game_id"])
        self.assertEqual(all_game_scorecards["data"][0]["categories"], all_scorecards[game_name_to_get]["categories"])
        self.assertEqual(all_game_scorecards["data"][0]["turn_order"], all_scorecards[game_name_to_get]["turn_order"])
        print("test_get_all_game_scorecards_1_scorecard passed!") 
        
    def test_get_all_game_scorecards_many_scorecards(self):
        method = "scorecard.get_all_game_scorecards"
        #add 4 scorecards to the same game
        all_scorecards=[]
        game = list(self.games.values())[2]
        for i in range(len(self.users)):
            user = list(self.users.values())[i]
            new_scorecard = self.ScorecardModel.create(game["id"], user["id"], game["name"]+"|"+user["username"])
            all_scorecards.append(new_scorecard["data"])
        all_scorecards.sort(key=lambda card: card["id"])

        #create a game/scorecard for a game with a name that is a substring of the above name
        sneaky_game_info={"name":game["name"][:-3]}
        returned_sneaky_game = self.GameModel.create(sneaky_game_info)
        sneaky_game_id = returned_sneaky_game["data"]["id"]
        sneaky_game_user_id = list(self.users.values())[1]["id"]
        sneaky_game_name = sneaky_game_info["name"]+"|"+list(self.users.values())[1]["username"]
        self.ScorecardModel.create(sneaky_game_id, sneaky_game_user_id, sneaky_game_name)

        all_game_scorecards = self.ScorecardModel.get_all_game_scorecards(game_name=game['name'])
        ensure_data_packet_formatting(self, all_game_scorecards, method, "success")
        self.assertEqual(len(all_scorecards), len(all_game_scorecards["data"])) #sneaky game should not be included
        all_game_scorecards["data"].sort(key=lambda card: card["id"])
        for i in range(len(all_game_scorecards["data"])):
            self.assertEqual(all_game_scorecards["data"][i]["id"], all_scorecards[i]["id"])
            self.assertEqual(all_game_scorecards["data"][i]["user_id"], all_scorecards[i]["user_id"])
            self.assertEqual(all_game_scorecards["data"][i]["game_id"], all_scorecards[i]["game_id"])
            self.assertEqual(all_game_scorecards["data"][i]["categories"], all_scorecards[i]["categories"])
            self.assertEqual(all_game_scorecards["data"][i]["turn_order"], all_scorecards[i]["turn_order"])

        print("test_get_all_game_scorecards_many_scorecards passed!") 
        
    def test_get_all_game_usernames_no_scorecards(self):
        method = "scorecard.get_all_game_usernames"
        # no games
        all_game_usernames = self.ScorecardModel.get_all_game_usernames(game_name='fake_game_DNE')
        ensure_data_packet_formatting(self, all_game_usernames, method, "success")
        self.assertEqual(len(all_game_usernames["data"]), 0)
        # 4 games w/ no scorecards
        for i in range(len(self.users)):
            user = list(self.users.values())[i]
            game = list(self.games.values())[i]
            all_game_usernames = self.ScorecardModel.get_all_game_usernames(game_name=game['name'])
            self.assertEqual(len(all_game_usernames["data"]), 0)
        print("test_get_all_game_usernames_no_scorecards passed!")  
           
    def test_get_all_game_usernames_1_scorecard(self):
        method = "scorecard.get_all_game_usernames"
        user = list(self.users.values())[3]
        game = list(self.games.values())[3]
        new_scorecard = self.ScorecardModel.create(game["id"], user["id"], game["name"]+"|"+user["username"])

        all_game_usernames = self.ScorecardModel.get_all_game_usernames(game_name=game['name'])
        self.assertEqual(len(all_game_usernames["data"]), 1)
        self.assertEqual(all_game_usernames["data"][0], user["username"])
        print("test_get_all_game_usernames_1_scorecard passed!") 
    
    def test_get_all_game_usernames_many_scorecards(self):
        method = "scorecard.et_all_game_usernames"
        game = list(self.games.values())[1]
        all_users =[]
        for i in range(len(self.users)-1): # creates a game w/ len(self.users)-1 scorecards
            user = list(self.users.values())[i]
            all_users.append(user["username"])
            new_scorecard = self.ScorecardModel.create(game["id"], user["id"], game["name"]+"|"+user["username"])
       
        all_game_usernames = self.ScorecardModel.get_all_game_usernames(game_name=game['name'])
        self.assertEqual(len(all_game_usernames["data"]), len(self.users)-1)
        for username in all_users:
            self.assertIn(username, all_game_usernames["data"])
            
        print("test_get_all_game_usernames_many_scorecards passed!") 
        
    def test_get_all_user_game_names_no_games(self):
        method = "scorecard.get_all_user_game_names"
        # no scorecards or games
        all_user_games = self.ScorecardModel.get_all_user_game_names(username='fake_username_DNE')
        self.assertEqual(len(all_user_games["data"]), 0)

        for i in range(len(self.games)):
            user = list(self.users.values())[0] 
            game = list(self.games.values())[i]
            new_scorecard = self.ScorecardModel.create(game["id"], user["id"], game["name"]+"|"+user["username"])
        
        all_user_games = self.ScorecardModel.get_all_user_game_names(username=list(self.users.values())[1]['username'])
        ensure_data_packet_formatting(self, all_user_games, method, "success")
        self.assertEqual(len(all_user_games["data"]), 0)

        print("test_get_all_user_game_names_no_games passed!")  
          
    def test_get_all_user_game_names_1_game(self):
        method = "scorecard.get_all_user_game_names"
        for i in range(len(self.users)):
            user = list(self.users.values())[i]  
            game = list(self.games.values())[i]
            new_scorecard = self.ScorecardModel.create(game["id"], user["id"], game["name"]+"|"+user["username"])
            print(f"new scorecard user games: {new_scorecard}")
        
        username_to_check = list(self.users.values())[1]['username']
        game_name_to_check = list(self.games.values())[1]['name']
        all_user_game_names = self.ScorecardModel.get_all_user_game_names(username=username_to_check)
        self.assertEqual(len(all_user_game_names["data"]), 1)
        self.assertIn(game_name_to_check, all_user_game_names['data'])
        print("test_get_all_user_game_names_1_game passed!") 
  
    def test_get_all_user_game_names_many_games(self):
        method = "scorecard.get_all_user_game_names"
        user = list(self.users.values())[2] #same user for len(self.games) games
        all_game_names = []
        for i in range(len(self.games)):
            game = list(self.games.values())[i]
            all_game_names.append(game["name"])
            new_scorecard = self.ScorecardModel.create(game["id"], user["id"], game["name"]+"|"+user["username"])
        
        username_to_check = user['username']
        all_user_game_names = self.ScorecardModel.get_all_user_game_names(username=username_to_check)
        self.assertEqual(len(all_user_game_names["data"]), len(self.games))
        for game_name_to_check in all_game_names:
            self.assertIn(game_name_to_check, all_user_game_names['data'])
        print("test_get_all_user_game_names_many_games passed!") 
        
    def test_update_scorecard_exists(self):
        #only tests updating categories since that will be the way we use update in pur project
        method = "scorecard.update"
        all_scorecards=[]
        for i in range(len(self.users)): #4 games with 1 scorecard each
            user = list(self.users.values())[i]
            game = list(self.games.values())[i]
 
            new_scorecard = self.ScorecardModel.create(game["id"], user["id"], game["name"]+"|"+user["username"])
            all_scorecards.append(new_scorecard["data"])
        all_scorecards.sort(key=lambda scorecard: scorecard["id"])
        
        returned_card = self.ScorecardModel.update(id=all_scorecards[0]["id"], name=all_scorecards[0]["name"], categories=self.partial_card)
        
        ensure_data_packet_formatting(self, returned_card, method, "success")
        self.assertEqual(returned_card['data']['id'],all_scorecards[0]['id'])
        self.assertEqual(returned_card['data']['game_id'],all_scorecards[0]['game_id'])
        self.assertEqual(returned_card['data']['user_id'],all_scorecards[0]['user_id'])
        self.assertEqual(returned_card['data']['name'],all_scorecards[0]['name'])
        self.assertEqual(returned_card['data']['turn_order'],all_scorecards[0]['turn_order'])
        self.assertEqual(returned_card['data']['categories'],self.partial_card)
        #check DB state
        try: 
            db_connection = sqlite3.connect(self.yahtzee_db_name)
            cursor = db_connection.cursor()
            query = f"SELECT * from {self.scorecard_table_name} WHERE id = {all_scorecards[0]['id']};"
            results = cursor.execute(query)
            result = results.fetchall()[0]

            self.assertEqual(result[0],all_scorecards[0]['id'])
            self.assertEqual(result[1],all_scorecards[0]['game_id'])
            self.assertEqual(result[2],all_scorecards[0]['user_id'])
            self.assertEqual(result[3],json.dumps(self.partial_card))
            self.assertEqual(result[4],all_scorecards[0]['turn_order'])
            self.assertEqual(result[5],all_scorecards[0]['name'])
            
            print("test_update_scorecard_exists passed!")  
        except sqlite3.Error as error:
            print(error)
        finally:
            db_connection.close()
    
    def test_update_scorecard_DNE(self):
        method = "scorecard.update"
        
        scorecard_name=self.games_info[0]['name']+'|'+self.users_info[0]['username']
       
        returned_scorecard=self.ScorecardModel.update(id=12345, name=scorecard_name,  categories=self.partial_card)
        ensure_data_packet_formatting(self, returned_scorecard, method, "error")
        returned_scorecards = self.ScorecardModel.get_all()
        self.assertTrue(len(returned_scorecards['data'])==0)
        print("test_update_scorecard_DNE passed!")
    
    def test_remove_scorecard_DNE(self):
        method = "scorecard.remove"
        #empty DB
        removed_card = self.ScorecardModel.remove(id=1234567)
        ensure_data_packet_formatting(self, removed_card, method, "error")
        #DB w/ 1 element
        user = list(self.users.values())[0]
        game = list(self.games.values())[0]
        new_scorecard = self.ScorecardModel.create(game["id"], user["id"], game["name"]+"|"+user["username"])
        removed_card = self.ScorecardModel.remove(id=new_scorecard['data']['id']+1)
        ensure_data_packet_formatting(self, removed_card, method, "error")
        print("test_remove_scorecard_DNE passed!")

    def test_remove_scorecard_exists(self):
        method = "scorecard.remove"
        all_scorecards = []
        for i in range(len(self.users)):
            user = list(self.users.values())[i]
            game = list(self.games.values())[i]
            new_scorecard = self.ScorecardModel.create(game["id"], user["id"], game["name"]+"|"+user["username"])
            all_scorecards.append(new_scorecard['data'])
            if i%2 == 1: #some games have multiple scorecards
              user = list(self.users.values())[i-1]
              new_scorecard = self.ScorecardModel.create(game["id"], user["id"], game["name"]+"|"+user["username"])
              all_scorecards.append(new_scorecard)

        scorecard_to_remove_0 = all_scorecards[0] # only scorecard for game 0
        scorecard_to_remove_1 = all_scorecards[1] # one of two scorecards for game 1
        removed_card_0 = self.ScorecardModel.remove(id=scorecard_to_remove_0['id'])
        self.assertEqual(removed_card_0["data"]["id"], scorecard_to_remove_0["id"])
        self.assertEqual(removed_card_0["data"]["user_id"], scorecard_to_remove_0["user_id"])
        self.assertEqual(removed_card_0["data"]["game_id"], scorecard_to_remove_0["game_id"])
        
        removed_card_1 = self.ScorecardModel.remove(id=scorecard_to_remove_1['id'])
        self.assertEqual(removed_card_1["data"]["id"], scorecard_to_remove_1["id"])
        self.assertEqual(removed_card_1["data"]["user_id"], scorecard_to_remove_1["user_id"])
        self.assertEqual(removed_card_1["data"]["game_id"], scorecard_to_remove_1["game_id"])
        
        try: 
            db_connection = sqlite3.connect(self.yahtzee_db_name)
            cursor = db_connection.cursor()
            query = f"SELECT * from {self.scorecard_table_name};"
            results = cursor.execute(query)
            DB_cards = results.fetchall()
            self.assertEqual(len(DB_cards), len(all_scorecards)-2)
            for DB_card in DB_cards:#verify removed cards not in all scorecards
                self.assertNotEqual(scorecard_to_remove_0['id'], DB_card[0])
                self.assertNotEqual(scorecard_to_remove_1['id'], DB_card[0])
            print("test_remove_scorecard_exists passed!")  
        except sqlite3.Error as error:
            print(error)
        finally:
            db_connection.close()
        
    def test_tally_score_with_scores(self):
        score_info_finished={
            "rolls_remaining":0,
            "upper":{
                "one":4,
                "two":8,
                "three":12,
                "four":16,
                "five":20,
                "six":24
                },
                "lower":{
                    "three_of_a_kind":20,
                    "four_of_a_kind":26,
                    "full_house":25,
                    "small_straight":0,
                    "large_straight":40,
                    "yahtzee":50,
                    "chance":8
                }
            }
        score_info_finished_no_bonus={
            "rolls_remaining":0,
            "upper":{
                "one":4,
                "two":8,
                "three":12,
                "four":16,
                "five":20,
                "six":0
            },
            "lower":{
                "three_of_a_kind":20,
                "four_of_a_kind":26,
                "full_house":0,
                "small_straight":0,
                "large_straight":40,
                "yahtzee":50,
                "chance":8
            }
        }
        score_info_partial={
            "rolls_remaining":2,
            "upper":{
                "one":4,
                "two":8,
                "three":-1,
                "four":-1,
                "five":-1,
                "six":24
            },
            "lower":{
                "three_of_a_kind":-1,
                "four_of_a_kind":26,
                "full_house":-1,
                "small_straight":0,
                "large_straight":40,
                "yahtzee":0,
                "chance":8
            }
        }
        score_info_partial_bonus={
            "rolls_remaining":2,
            "upper":{
                "one":4,
                "two":8,
                "three":12,
                "four":16,
                "five":20,
                "six":24
            },
            "lower":{
                "three_of_a_kind":-1,
                "four_of_a_kind":26,
                "full_house":-1,
                "small_straight":0,
                "large_straight":40,
                "yahtzee":0,
                "chance":8
            }
        }
        
        scorecards=[
            (score_info_finished, 288),
            (score_info_finished_no_bonus, 204),
            (score_info_partial, 110),
            (score_info_partial_bonus, 193)
        ]
        for card in scorecards:
            score = self.ScorecardModel.tally_score(card[0])
            self.assertEqual(score, card[1])
        print("test_tally_score_with_scores passed!")  

    def test_tally_score_blank(self):
        score = self.ScorecardModel.tally_score(self.blank_scorecard)
        self.assertEqual(score, 0)
        print("test_tally_score_blank passed!")  
 
if __name__ == '__main__':
    unittest.main() 