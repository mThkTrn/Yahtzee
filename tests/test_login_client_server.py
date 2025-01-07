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

fpath = os.path.join(os.path.dirname(__file__), '/Models') #Assumes this file lives in a tests folder next to the Models folder
sys.path.append(fpath)

import UserModel as User_Model

'''
Tests login via the login.html page
'''
class Basic_Login_Tests(unittest.TestCase):

    def enter_and_submit_user_info(self, username, password):
        """Helper method"""
        username_element = self.browser.find_element(By.ID, "username_input")
        username_element.clear()
        username_element.send_keys(username)
        password_element = self.browser.find_element(By.ID, "password_input")
        password_element.clear()
        password_element.send_keys(password)
       
        submit_button=self.browser.find_element(By.ID, 'login_submit')
        submit_button.click()
    
    @classmethod
    def setUpClass(self):
        #Runs once, before any tests are run
        self.url='http://127.0.0.1:8080'
        self.login_requirements={
            "title": 'Yahtzee: Login',
            "elements":{
                "feedback":"SECTION",
                "username_input":"INPUT",
                "password_input":"INPUT",
                "login_submit": "INPUT", 
                "create_submit": "INPUT"
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
    
    def setUp(self):
        #Runs before every test
        self.browser = webdriver.Chrome()
        self.addCleanup(self.browser.quit)

        self.DB_location=f"{os.getcwd()}/Models/yahtzeeDB.db" #Assumes DB lives in the Models folder which is right next to the tests folder
        self.user_table_name = "users"
        self.game_table_name = "games"
        self.scorecard_table_name = "scorecard"
        wipe_and_clean_tables(self.DB_location, self.user_table_name, self.game_table_name, self.scorecard_table_name)
        self.User_Model = User_Model.User(self.DB_location, self.user_table_name)

        self.users={} #add 4 users and keep track of their ids
        for i in range(len(self.valid_users)):
            user = self.User_Model.create(self.valid_users[i])
            self.users[self.valid_users[i]['email']] = user["data"]

    def test_login_required_elements(self):
        """login.html contains all required elements/id's"""
        self.browser.get(self.url)
        expected = self.login_requirements['title']
        actual = self.browser.title
        self.assertEqual(actual, expected, f"The page title for user_details.html should be {expected}")
        
        for expected_id in self.login_requirements['elements']:
            try:
                actual_element = self.browser.find_element(By.ID, expected_id)
                if expected_id=="user_details_submit":
                    self.assertEqual(actual_element.get_attribute("value").lower(), "CREATE".lower(), f"The form button should say CREATE")
            except:
                self.fail(f"#{expected_id} element does not exist!")
            expected_type = self.login_requirements['elements'][expected_id].lower()
            actual_type = actual_element.tag_name
            self.assertEqual(actual_type.lower(), expected_type, f"The type of element should be {expected_type}")
        
        print("test_login_required_elements... test passed!")
    
    def test_login_legit(self):
        for user in self.valid_users:
            self.browser.get(self.url)
            self.enter_and_submit_user_info(user["username"], user["password"])
            wait(self.browser, 2)
            self.assertEqual(self.browser.title, "Yahtzee: User Games", f"Should redirect to user_games.html")

        print("test_login_legit... test passed!")
    
    def test_login_user_DNE(self):
        for user in self.valid_users:
            self.browser.get(self.url)
            self.enter_and_submit_user_info(user["username"]+"_xxx", user["password"])
            wait(self.browser, 2)
            self.assertEqual(self.browser.title, self.login_requirements['title'], f"Should redirect to login.html")

            feedback_element = self.browser.find_element(By.ID, "feedback")
            self.assertTrue(len(feedback_element.text)>10, "Substantial feedback should be provided.")

        print("test_login_user_DNE... test passed!")

    
    def test_login_invalid_password(self):
        for user in self.valid_users:
            self.browser.get(self.url)
            self.enter_and_submit_user_info(user["username"], user["password"]+"_xxx")
            wait(self.browser, 2)
            self.assertEqual(self.browser.title, self.login_requirements['title'], f"Should redirect to login.html")

            feedback_element = self.browser.find_element(By.ID, "feedback")
            self.assertTrue(len(feedback_element.text)>10, "Substantial feedback should be provided.")
        print("test_login_invalid_password... test passed!")
    
    def test_create_user_button(self):
        self.browser.get(self.url)
        submit_button=self.browser.find_element(By.ID, 'create_submit')
        submit_button.click()
        
        self.assertEqual(self.browser.title, "Yahtzee: User Details", f"Should redirect to login.html")
        print("test_create_user_button... test passed!")
    
if __name__ == '__main__':
    unittest.main()