#python3 -m pip install selenium pytest
import os
import sys
import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC

from DB_Helper import wipe_and_clean_tables

fpath = os.path.join(os.path.dirname(__file__), '../Models') #Assumes this file lives in a tests folder next to the Models folder
sys.path.append(fpath)
import User_Model, Game_Model, Scorecard_Model

'''
Tests Create, Get, Delete via the user_games.html page
'''
class Basic_User_Games_Tests(unittest.TestCase):

    def enter_and_submit_user_info(self, game_name, context):
        """Helper method"""
        game_name_element = self.browser.find_element(By.ID, "game_name_input")
        game_name_element.clear()
        game_name_element.send_keys(game_name)

        if context == "create":
            submit_button=self.browser.find_element(By.ID, 'create_submit')
            submit_button.click()
        else:
            submit_button=self.browser.find_element(By.ID, 'join_submit')
            submit_button.click()
    
    @classmethod
    def setUpClass(self):
        #Runs once, before any tests are run
        self.url='http://127.0.0.1:8080/games'
        self.login_requirements={
            "title": 'Yahtzee: User Games',
            "elements":{
                "feedback":"SECTION",
                "games_list":"OL",
                "high_scores_list":"OL",
                "game_name_input":"INPUT",
                "create_submit": "INPUT", 
                "join_submit": "INPUT"
            }
        }
        
        self.valid_users=[{"email":"cookie.monster@trinityschoolnyc.org",
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
        
        self.valid_games=[]
        for i in range(5):
            self.valid_games.append({"name":f"my_Game_{i}"})
        
        self.valid_scorecards=[
            {"score":181,
             "categories":{"rolls_remaining":1,
                            "upper":{
                                "one":4,
                                "two":8,
                                "three":-1,
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
            },
            {"score":288,
             "categories":{
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
            },
            {"score":204,
             "categories":{
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
            },
            {"score":110,
             "categories":{
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
            }
        ]
                   
    def setUp(self):
        #Runs before every test
        self.browser = webdriver.Chrome()
        self.addCleanup(self.browser.quit)

        self.DB_location=f"{os.getcwd()}/../Models/yahtzeeDB.db" #Assumes DB lives in the Models folder which is right next to the tests folder
        self.user_table_name = "users"
        self.game_table_name = "games"
        self.scorecard_table_name = "scorecards"
        wipe_and_clean_tables(self.DB_location, self.user_table_name, self.game_table_name, self.scorecard_table_name)
        self.User_Model = User_Model.User(self.DB_location, self.user_table_name)
        self.Game_Model = Game_Model.Game(self.DB_location, self.game_table_name)
        self.Scorecard_Model = Scorecard_Model.Scorecard(self.DB_location, self.scorecard_table_name, self.user_table_name, self.game_table_name)

    
    def test_game_required_elements(self):
        """user_games.html contains all required elements/id's"""
        user = self.valid_users[0]
        self.User_Model.create(user)
        self.browser.get(f"{self.url}/{user['username']}")
        expected = self.login_requirements['title']
        actual = self.browser.title
        self.assertEqual(actual, expected, f"The page title for user_games.html should be {expected}")
        
        for expected_id in self.login_requirements['elements']:
            try:
                actual_element = self.browser.find_element(By.ID, expected_id)
            except:
                self.fail(f"#{expected_id} element does not exist!")
        
            expected_type = self.login_requirements['elements'][expected_id].lower()
            actual_type = actual_element.tag_name
            self.assertEqual(actual_type.lower(), expected_type, f"The type of element should be {expected_type}")
        
        print("test_game_required_elements... test passed!")
   
    def test_game_links_1_game(self):
        user = self.valid_users[0]
        user = self.User_Model.create(user)["data"]
        game = self.Game_Model.create(self.valid_games[0])["data"]
        new_game_name=game["name"]
        scorecard = self.Scorecard_Model.create(game["id"], user["id"], f"{game['name']}|{user['username']}")
        self.browser.get(f"{self.url}/{user['username']}")
        el_id = "games_list"
        games_list = self.browser.find_element(By.ID, el_id)
        games_list_games = games_list.find_elements(By.TAG_NAME, 'li')
        self.assertTrue(len(games_list_games)==1, f"{el_id} should have 1 game <li>")
        game_link = games_list_games[0].find_elements(By.TAG_NAME, 'a')
        self.assertEqual(game_link[0].text, game['name'], f"Link text should be {game['name']}")
        game_href = game_link[0].get_attribute("href")
        link = f"/games/{new_game_name}/{user['username']}"
        valid_game_link =  (game_href==link) or (game_href==f"http://127.0.0.1:8080{link}")
        self.assertTrue(valid_game_link, f"game link href should be /games/{new_game_name}/{user['username']}")
        delete_href = game_link[1].get_attribute("href")
        link = f"/games/delete/{new_game_name}/{user['username']}"
        valid_game_link =  (delete_href==link) or (delete_href==f"http://127.0.0.1:8080{link}")
        self.assertTrue(valid_game_link, f"game link href should be /games/{new_game_name}/{user['username']}")

        print("test_game_links_1_game... test passed!")
    
    
    def test_game_links_many_game(self):
        user = self.valid_users[0]
        user = self.User_Model.create(user)["data"]
        all_game_names = set()
        for game in self.valid_games:
            new_game = self.Game_Model.create(game)["data"]
            game_name=f"{new_game['name']}|{user['username']}"
            self.Scorecard_Model.create(new_game["id"], user["id"], game_name)
            all_game_names.add(new_game['name'])
        
        self.browser.get(f"{self.url}/{user['username']}")
        el_id = "games_list"
        games_list = self.browser.find_element(By.ID, el_id)
        games_list_games = games_list.find_elements(By.TAG_NAME, 'li')
        self.assertEqual(len(games_list_games),len(self.valid_games), f"{el_id} should have {len(self.valid_games)} game <li>")
       
        for game in games_list_games: 
            game_link = game.find_elements(By.TAG_NAME, 'a')
            game_name = game_link[0].text
            self.assertTrue(game_name in all_game_names, f"{game_name} should be an actual game name.")
            all_game_names.remove(game_name)
            game_href = game_link[0].get_attribute("href")
            link = f"/games/{game_name}/{user['username']}"
            valid_game_link =  (game_href==link) or (game_href==f"http://127.0.0.1:8080{link}")
            self.assertTrue(valid_game_link, f"game link href should be /games/{game_name}/{user['username']}")
            delete_href = game_link[1].get_attribute("href")
            link = f"/games/delete/{game_name}/{user['username']}"
            valid_game_link =  (delete_href==link) or (delete_href==f"http://127.0.0.1:8080{link}")
            self.assertTrue(valid_game_link, f"game link href should be /games/{game_name}/{user['username']}")

        print("test_game_links_many_game... test passed!")
    
    def test_game_links_0_games(self):
        user = self.valid_users[0]
        self.User_Model.create(user)
        self.browser.get(f"{self.url}/{user['username']}")
        el_id = "games_list"
        games_list = self.browser.find_element(By.ID, el_id)
        games_list_games = games_list.find_elements(By.TAG_NAME, 'li')
        self.assertTrue(len(games_list_games)==0, f"{el_id} should not have any games <li>")
        print("test_game_links_0_games... test passed!")
    
    
    def test_game_username_DNE(self):
        for i in range(1, len(self.valid_users)):
            self.User_Model.create(self.valid_users[i])

        link = f"{self.url}/{self.valid_users[0]['username']}" # user DNE
        self.browser.get(link)

        self.assertEqual(self.browser.title, "Yahtzee: Login", f"The page should redirect to login.html")
        feedback_element = self.browser.find_element(By.ID, "feedback")
        self.assertTrue(len(feedback_element.text)>10, "Substantial feedback should be provided.")
        print("test_game_username_DNE... test passed!")
   
    
    def test_create_game_start_with_0_games(self):
        user = self.valid_users[2]
        self.User_Model.create(user)
        link = f"{self.url}/{user['username']}" 
        self.browser.get(link)

        new_game_name = self.valid_games[0]["name"]
        self.enter_and_submit_user_info(new_game_name, "create")
        el_id = "games_list"
        games_list = self.browser.find_element(By.ID, el_id)
        games_list_games = games_list.find_elements(By.TAG_NAME, 'li')
        game_link = games_list_games[0].find_elements(By.TAG_NAME, 'a')
        self.assertEqual(game_link[0].text, new_game_name, f"Link text should be {new_game_name}")
        game_href = game_link[0].get_attribute("href")
        link = f"/games/{new_game_name}/{user['username']}"
        valid_game_link =  (game_href==link) or (game_href==f"http://127.0.0.1:8080{link}")
        self.assertTrue(valid_game_link, f"game link href should be /games/{new_game_name}/{user['username']}")
        delete_href = game_link[1].get_attribute("href")
        link = f"/games/delete/{new_game_name}/{user['username']}"
        valid_game_link =  (delete_href==link) or (delete_href==f"http://127.0.0.1:8080{link}")
        self.assertTrue(valid_game_link, f"game link href should be /games/{new_game_name}/{user['username']}")

        #Check DB
        game=self.Game_Model.get(game_name=new_game_name)
        self.assertTrue(game, f"New game should exist in the DB")

        print("test_create_game_start_with_0_games... test passed!")
    
    
    def test_create_game_start_with_4_games(self):
        user = self.valid_users[2]
        user=self.User_Model.create(user)["data"]
        all_game_names=set()
        for i in range(4):
            new_game=self.Game_Model.create(self.valid_games[i])['data']
            game_name=f"{new_game['name']}|{user['username']}"
            self.Scorecard_Model.create(new_game["id"], user["id"], game_name)
            all_game_names.add(self.valid_games[i]['name'])
        link = f"{self.url}/{user['username']}" 
        self.browser.get(link)

        new_game_name = self.valid_games[4]["name"]
        all_game_names.add(new_game_name)
        self.enter_and_submit_user_info(new_game_name, "create")

        el_id = "games_list"
        games_list = self.browser.find_element(By.ID, el_id)
        games_list_games = games_list.find_elements(By.TAG_NAME, 'li')
        self.assertEqual(len(games_list_games),5, f"{el_id} should have 5 game <li>")
        
        for game in games_list_games:
            game_name=self.valid_games[i]['name']
            game_link = game.find_elements(By.TAG_NAME, 'a')
            game_name = game_link[0].text
            self.assertTrue(game_name in all_game_names, f"{game_name} should be an actual game name.")
            all_game_names.remove(game_name)
            game_href = game_link[0].get_attribute("href")
            link = f"/games/{game_name}/{user['username']}"
            valid_game_link =  (game_href==link) or (game_href==f"http://127.0.0.1:8080{link}")
            self.assertTrue(valid_game_link, f"game link href should be /games/{game_name}/{user['username']}")
            delete_href = game_link[1].get_attribute("href")
            link = f"/games/delete/{game_name}/{user['username']}"
            valid_game_link =  (delete_href==link) or (delete_href==f"http://127.0.0.1:8080{link}")
            self.assertTrue(valid_game_link, f"game link href should be /games/{game_name}/{user['username']}")

        #Check DB
        game=self.Game_Model.get(game_name=new_game_name)
        self.assertTrue(game, f"New game should exist in the DB")
        print("test_create_game_start_with_4_games... test passed!")
    
    def test_create_game_duplicate(self):
        user = self.valid_users[1]
        user=self.User_Model.create(user)["data"]
        all_game_names=set()
        for i in range(4):
            new_game=self.Game_Model.create(self.valid_games[i])['data']
            game_name=f"{new_game['name']}|{user['username']}"
            self.Scorecard_Model.create(new_game["id"], user["id"], game_name)
            all_game_names.add(self.valid_games[i]['name'])
        link = f"{self.url}/{user['username']}" 
        self.browser.get(link)

        self.enter_and_submit_user_info(self.valid_games[2]['name'], "create")

        feedback_element = self.browser.find_element(By.ID, "feedback")
        self.assertTrue(len(feedback_element.text)>10, "Substantial feedback should be provided.")

        el_id = "games_list"
        games_list = self.browser.find_element(By.ID, el_id)
        games_list_games = games_list.find_elements(By.TAG_NAME, 'li')
        self.assertEqual(len(games_list_games),4, f"{el_id} should have original 4 game <li>")

        #Check DB
        games=self.Game_Model.get_all()["data"]
        self.assertTrue(len(games)==4, f"Only original 4 games should exist in the DB")
        print("test_create_game_duplicate... test passed!")
    
    def test_login_user_with_multiple_games(self):
        user = self.valid_users[1]
        user=self.User_Model.create(user)["data"]
        all_game_names=set()
        for i in range(4):
            new_game=self.Game_Model.create(self.valid_games[i])['data']
            game_name=f"{new_game['name']}|{user['username']}"
            self.Scorecard_Model.create(new_game["id"], user["id"], game_name)
            all_game_names.add(self.valid_games[i]['name'])
        self.browser.get('http://127.0.0.1:8080')

        username_element = self.browser.find_element(By.ID, "username_input")
        username_element.clear()
        username_element.send_keys(user['username'])
        password_element = self.browser.find_element(By.ID, "password_input")
        password_element.clear()
        password_element.send_keys(user['password'])
        submit_button=self.browser.find_element(By.ID, 'login_submit')
        submit_button.click()

        el_id = "games_list"
        games_list = self.browser.find_element(By.ID, el_id)
        games_list_games = games_list.find_elements(By.TAG_NAME, 'li')
        self.assertEqual(len(games_list_games), 4, f"{el_id} should have 4 game <li>")
        
        for game in games_list_games:
            game_link = game.find_elements(By.TAG_NAME, 'a')
            game_name = game_link[0].text
            self.assertTrue(game_name in all_game_names, f"{game_name} should be an actual game name.")
            all_game_names.remove(game_name)
            game_href = game_link[0].get_attribute("href")
            link = f"/games/{game_name}/{user['username']}"
            valid_game_link =  (game_href==link) or (game_href==f"http://127.0.0.1:8080{link}")
            self.assertTrue(valid_game_link, f"game link href should be /games/{game_name}/{user['username']}")
            delete_href = game_link[1].get_attribute("href")
            link = f"/games/delete/{game_name}/{user['username']}"
            valid_game_link =  (delete_href==link) or (delete_href==f"http://127.0.0.1:8080{link}")
            self.assertTrue(valid_game_link, f"game link href should be /games/{game_name}/{user['username']}")

        print("test_login_user_with_multiple_games... test passed!")
        
    
    def test_delete_game(self):
        user = self.valid_users[2]
        user=self.User_Model.create(user)["data"]
        all_game_names=list()
        for i in range(5):
            new_game=self.Game_Model.create(self.valid_games[i])['data']
            game_name=f"{new_game['name']}|{user['username']}"
            self.Scorecard_Model.create(new_game["id"], user["id"], game_name)
            all_game_names.append(self.valid_games[i]['name'])

        self.browser.get(f"{self.url}/{user['username']}")

        el_id = "games_list"
        games_list = self.browser.find_element(By.ID, el_id)
        games_list_games = games_list.find_elements(By.TAG_NAME, 'li')
        self.assertEqual(len(games_list_games), 5, f"{el_id} should have 5 game <li>")
        
        game_name_to_delete = all_game_names[len(all_game_names)-2] #Delete 2nd from last game
        print("game_name_to_delete",game_name_to_delete)

        for game in games_list_games:
            game_link = game.find_elements(By.TAG_NAME, 'a')
            game_name = game_link[0].text
            if game_name == game_name_to_delete:
                delete_href = game_link[1]
                delete_href.click()
                break
        
        el_id = "games_list"
        games_list = self.browser.find_element(By.ID, el_id)
        games_list_games = games_list.find_elements(By.TAG_NAME, 'li')
        self.assertEqual(len(games_list_games), 4, f"{el_id} should have 5 game <li>")

        for game in games_list_games:
            game_link = game.find_elements(By.TAG_NAME, 'a')
            game_name = game_link[0].text
            self.assertNotEqual(game_name, game_name_to_delete, f"{game_name_to_delete} should not have a game <li>")

        result = self.Game_Model.get(game_name=game_name_to_delete)
        self.assertEqual(result['status'], "error", f".get() should return error for the deleted game name")

        # check for deleting associated scorecards
        print("test_delete_game... test passed!")

    ''' 
    def test_join_game(self):
        self.browser.get(self.url)
        self.assertEqual(True, False, f"Test not yet implemented")
        print("test_join_game... test passed!")
    
    def test_join_game_DNE(self):
        self.browser.get(self.url)
        self.assertEqual(True, False, f"Test not yet implemented")
        print("test_join_game_DNE... test passed!")
    '''
    
    def test_player_scores_1_game(self):
        user = self.valid_users[1]
        user=self.User_Model.create(user)["data"]
        new_game=self.Game_Model.create(self.valid_games[2])['data']
        game_name=f"{new_game['name']}|{user['username']}"
        new_scorecard=self.Scorecard_Model.create(new_game["id"], user["id"], game_name)['data']
        updated_card = self.valid_scorecards[0]
        self.Scorecard_Model.update(new_scorecard['id'], new_scorecard['name'], updated_card['categories'])
        
        self.browser.get(f"{self.url}/{user['username']}")

        el_id = "high_scores_list"
        games_list = self.browser.find_element(By.ID, el_id)
        games_list_games = games_list.find_elements(By.TAG_NAME, 'li')
        self.assertEqual(len(games_list_games), 1, f"{el_id} should have 1 high score <li>")
        text = games_list_games[0].text
        self.assertEqual(text, f"{new_game['name']} : {updated_card['score']}", f"The high score label should be: {new_game['name']} : {updated_card['score']}")
        print("test_player_scores_1_game... test passed!")

    def test_player_scores_many_games(self):
        user = self.valid_users[1]
        user=self.User_Model.create(user)["data"]

        all_score_labels = []
        for i in range(len(self.valid_scorecards)):
            new_game=self.Game_Model.create(self.valid_games[i])['data']
            game_name=f"{new_game['name']}|{user['username']}"
            valid_card= self.valid_scorecards[i]
            new_scorecard=self.Scorecard_Model.create(new_game["id"], user["id"], game_name)['data']
            self.Scorecard_Model.update(new_scorecard['id'], new_scorecard['name'], valid_card['categories'])
            all_score_labels.append(f"{new_game['name']} : {valid_card['score']}")
        
        self.browser.get(f"{self.url}/{user['username']}")

        all_score_labels.sort(key=lambda label: int(label.split(" : ")[1]), reverse=True)

        el_id = "high_scores_list"
        games_list = self.browser.find_element(By.ID, el_id)
        games_list_games = games_list.find_elements(By.TAG_NAME, 'li')
        self.assertEqual(len(games_list_games), len(all_score_labels), f"{el_id} should have {len(all_score_labels)} high score <li>")
        for i in range(len(games_list_games)):
            score_li_el = games_list_games[i]
            text = score_li_el.text
            self.assertEqual(text, all_score_labels[i], f"The sorted high score label should be: {all_score_labels[i]}")
        
        print("test_player_scores_many_games... test passed!")

    
    def test_player_scores_0_games(self):
        user = self.valid_users[1]
        user=self.User_Model.create(user)["data"]
        self.browser.get(f"{self.url}/{user['username']}")

        el_id = "high_scores_list"
        games_list = self.browser.find_element(By.ID, el_id)
        games_list_games = games_list.find_elements(By.TAG_NAME, 'li')
        self.assertTrue(len(games_list_games)==0, f"There should be no high score <li> elements")
        print("test_player_scores_0_games... test passed!")
   

if __name__ == '__main__':
    unittest.main()