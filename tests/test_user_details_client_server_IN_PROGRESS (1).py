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
import UserModel

'''
Tests Create, Update, Delete user via the user_details.html page
'''
class Basic_Web_Tests(unittest.TestCase):

    def enter_and_submit_user_info(self, username, password, email):
        """Helper method"""
        username_element = self.browser.find_element(By.ID, "username_input")
        username_element.clear()
        username_element.send_keys(username)
        password_element = self.browser.find_element(By.ID, "password_input")
        password_element.clear()
        password_element.send_keys(password)
        email_element = self.browser.find_element(By.ID, "email_input")
        email_element.clear()
        email_element.send_keys(email)

        submit_button=self.browser.find_element(By.ID, 'user_details_submit')
        submit_button.click()

    @classmethod
    def setUpClass(self):
        #Runs once, before any tests are run
        self.url='http://127.0.0.1:8080/users'
        self.user_details_create_requirements={
            "title": 'Yahtzee: User Details',
            "elements":{
                "feedback":"SECTION",
                "username_input":"INPUT",
                "password_input":"INPUT",
                "email_input":"INPUT",
                "user_details_submit": "INPUT"
            }
        }
        self.user_details_update_requirements={
            "title": 'Yahtzee: User Details',
            "elements":{
                "feedback":"SECTION",
                "username_input":"INPUT",
                "password_input":"INPUT",
                "email_input":"INPUT",
                "user_details_submit": "INPUT",
                "user_details_delete_submit": "INPUT"
            }
        }
        self.invalid_usernames={
            "hey_hey!!":"Contains non-alphanumeric character",
            "hey.hey!!":"Contains non-alphanumeric character"
        }
        self.invalid_passwords={
            "abcde":"Too short. Must be at least 8 charcters",
            "1234567":"Too short. Must be at least 8 charcters"
        }
        self.invalid_emails={
            "abcde@google":"Must contain a .",
            "abcde.google":"Must contain an @",
            "abcdegoogle":"Must contain an @ and an .",
            "ab cde@google.com":"Cannot contain a ' '"
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

        self.DB_location=f"{os.getcwd()}/../Models/yahtzeeDB.db" #Assumes DB lives in the Models folder which is right next to the tests folder
        self.user_table_name = "users"

        wipe_and_clean_tables(self.DB_location) # All tables in DB are wiped and recreated to start each test
        self.UserModel = UserModel.User(self.DB_location, self.user_table_name)

    #------------------CREATE tests-----------------
    
    def test_required_elements_create(self):
        """user_details.html contains all required elements/id's"""
        self.browser.get(self.url)
        expected = self.user_details_create_requirements['title']
        actual = self.browser.title
        self.assertEqual(actual, expected, f"The page title for user_details.html should be {expected}")
        
        for expected_id in self.user_details_create_requirements['elements']:
            try:
                actual_element = self.browser.find_element(By.ID, expected_id)
                if expected_id=="user_details_submit":
                    self.assertEqual(actual_element.get_attribute("value").lower(), "CREATE".lower(), f"The form button should say CREATE")
            except:
                self.fail(f"#{expected_id} element does not exist!")
            expected_type = self.user_details_create_requirements['elements'][expected_id].lower()
            actual_type = actual_element.tag_name
            self.assertEqual(actual_type.lower(), expected_type, f"The type of element should be {expected_type}")
        
        print("test_required_elements_create... test passed!")
    
    def test_create_user(self):
        """Submit user information - Correct data format"""
        for user in self.valid_users:
            self.browser.get(self.url)
            self.enter_and_submit_user_info(user["username"], user["password"], user["email"])
            wait(self.browser, 2).until_not(EC.title_is(self.user_details_create_requirements["title"]))

            #Correctly redirects to user_games.html
            self.assertEqual(self.browser.title, "Yahtzee: User Games", f"Should redirect to user_games.html")
        
        #Correctly modifies DB
        all_users = self.UserModel.get_all()
        all_usernames = [user["username"] for user in all_users["data"]]
        self.assertEqual(len(self.valid_users), len(all_usernames), f"DB should have same number of valid users")
        for user in self.valid_users:
            self.assertIn(user["username"], all_usernames, f"DB should have user with username {user['username']}")
        print("test_create_user... test passed!")
   
    def test_create_user_invalid_info(self):
        """Submit user information - Incorrect data format produces feedback"""
        for username in self.invalid_usernames:
            self.browser.get(self.url)
            self.enter_and_submit_user_info(username, "12345_abcde", "hi@gmail.com")
            wait(self.browser, 0.5)

            self.assertEqual(self.browser.title, "Yahtzee: User Details", f"Should redirect to user_details.html")
            feedback_element = self.browser.find_element(By.ID, "feedback")
            self.assertTrue(len(feedback_element.text)>10, "Substantial feedback should be provided.")

            new_user = self.UserModel.get(username=username)
            self.assertEqual(new_user["status"], "error", "Invalid username should not be added to DB.")

        for password in self.invalid_passwords:
            self.browser.get(self.url)
            username = "hey_yo_lets_go123"
            self.enter_and_submit_user_info(username, password, "hi@gmail.com")
            wait(self.browser, 0.5)

            self.assertEqual(self.browser.title, "Yahtzee: User Details", f"Should redirect to user_details.html")
            feedback_element = self.browser.find_element(By.ID, "feedback")
            self.assertTrue(len(feedback_element.text)>10, "Substantial feedback should be provided.")

            new_user = self.UserModel.get(username=username)
            self.assertEqual(new_user["status"], "error", "Invalid passowrd should not be added to DB.")

        for email in self.invalid_emails:
            self.browser.get(self.url)
            username = "hey_yo_lets_go123"
            self.enter_and_submit_user_info(username, "12345_abscd", email)
            wait(self.browser, 1)

            self.assertEqual(self.browser.title, "Yahtzee: User Details", f"Should redirect to user_details.html")

            #type='email' prevents bad emails from being used
            #feedback_element = self.browser.find_element(By.ID, "feedback")
            #self.assertTrue(len(feedback_element.text)>10, "Substantial feedback should be provided.")

            new_user = self.UserModel.get(username=username)
            self.assertEqual(new_user["status"], "error", "Invalid email should not be added to DB.")

        print("test_create_user_invalid_info... test passed!")
   
    def test_create_user_duplicate_username_email(self):
        """Submit user information - Username or email already exists"""
        for user in self.valid_users:
            self.browser.get(self.url)
            self.enter_and_submit_user_info(user["username"], user["password"], user["email"])
            wait(self.browser, 2).until_not(EC.title_is(self.user_details_create_requirements["title"]))
       
        self.browser.get(self.url)
        duplicate_username = self.valid_users[0]["username"]
        self.enter_and_submit_user_info(duplicate_username, "12345_abdf", "new_email@gmail.com")

        self.assertEqual(self.browser.title, "Yahtzee: User Details", f"Should redirect to user_details.html")
        feedback_element = self.browser.find_element(By.ID, "feedback")
        self.assertTrue(len(feedback_element.text)>10, "Substantial feedback should be provided.")
        all_users = self.UserModel.get_all()
        self.assertEqual(len(self.valid_users), len(all_users["data"]), f"DB should have same number of valid users")

        self.browser.get(self.url)
        duplicate_email = self.valid_users[1]["email"]
        self.enter_and_submit_user_info("brand_new_username", "12345_abdf", duplicate_email)

        self.assertEqual(self.browser.title, "Yahtzee: User Details", f"Should redirect to user_details.html")
        feedback_element = self.browser.find_element(By.ID, "feedback")
        self.assertTrue(len(feedback_element.text)>10, "Substantial feedback should be provided.")
        all_users = self.UserModel.get_all()
        self.assertEqual(len(self.valid_users), len(all_users["data"]), f"DB should have same number of valid users")

        print("test_create_user_duplicate_username_email... test passed!")

    #------------------UPDATE tests-----------------
    def test_required_elements_update(self):
        """user_details.html contains all required elements/id's"""
        for user in self.valid_users:
            self.browser.get(self.url)
            self.enter_and_submit_user_info(user["username"], user["password"], user["email"])
            wait(self.browser, 2).until_not(EC.title_is(self.user_details_update_requirements["title"]))

        self.browser.get(f"{self.url}/{self.valid_users[2]['username']}")
        expected = self.user_details_update_requirements['title']
        actual = self.browser.title
        self.assertEqual(actual, expected, f"The page title for user_details.html should be {expected}")

        for expected_id in self.user_details_update_requirements['elements']:
            try:
                actual_element = self.browser.find_element(By.ID, expected_id)
                if expected_id=="user_details_submit":
                    self.assertEqual(actual_element.get_attribute("value").lower(), "UPDATE".lower(), f"The form button should say UPDATE")
            except:
                self.fail(f"#{expected_id} element does not exist!")
            expected_type = self.user_details_update_requirements['elements'][expected_id].lower()
            actual_type = actual_element.tag_name
            self.assertEqual(actual_type.lower(), expected_type, f"The type of element should be {expected_type}")
        
        print("test_required_elements_update... test passed!")

    
    def test_update_user_exits(self):
        """Delete user - Username exists"""
        for user in self.valid_users:
            self.browser.get(self.url)
            self.enter_and_submit_user_info(user["username"], user["password"], user["email"])
            wait(self.browser, 2).until_not(EC.title_is(self.user_details_create_requirements["title"]))
        
        user_to_update = self.valid_users[0]
        orig_user = self.UserModel.get(username=user_to_update["username"])

        new_username = user_to_update["username"]+"2"
        new_password = user_to_update["password"]+"2"
        new_email = "2"+user_to_update["email"]
        self.browser.get(f"{self.url}/{user_to_update['username']}")

        self.enter_and_submit_user_info(new_username, new_password, new_email)
        wait(self.browser, 1)

        updated_user = self.UserModel.get(id=orig_user["data"]["id"])
        self.assertEqual(updated_user["status"], "success", "Original user should still exist.")
        self.assertEqual(updated_user["data"]["username"], new_username, f"Original user should have username updated to {new_username}.")
        self.assertEqual(updated_user["data"]["email"], new_email, f"Original user should have username updated to {new_email}.")
        self.assertEqual(updated_user["data"]["password"], new_password, f"Original user should have username updated to {new_password}.")

        print("test_update_user_exits... test passed!")
    
    
    def test_update_user_DNE(self):
        """Delete user - Username doesn't exist"""
        #bad id
        username_DNE = "nope_not_a_user"
        self.browser.get(f"{self.url}/{username_DNE}")

        username_element = self.browser.find_element(By.ID, "username_input")
        self.assertEqual(username_element.text, "", "Username should be blank")
        password_element = self.browser.find_element(By.ID, "password_input")
        self.assertEqual(password_element.text, "", "Password should be blank")
        email_element = self.browser.find_element(By.ID, "email_input")
        self.assertEqual(email_element.text, "", "Email should be blank")

        feedback_element = self.browser.find_element(By.ID, "feedback")
        self.assertTrue(len(feedback_element.text)>10, "Substantial feedback should be provided.")

        print("test_update_user_DNE... test passed!")

    
    def test_update_user_invalid_info(self):
        """update user - Invalid info"""
        for user in self.valid_users:
            self.browser.get(self.url)
            self.enter_and_submit_user_info(user["username"], user["password"], user["email"])
            wait(self.browser, 2).until_not(EC.title_is(self.user_details_create_requirements["title"]))
        
        for username in self.invalid_usernames:
            self.browser.get(f"{self.url}/{self.valid_users[2]['username']}")
            self.enter_and_submit_user_info(username, "12345_abcde", "hi@gmail.com")
            wait(self.browser, 0.5)

            self.assertEqual(self.browser.title, "Yahtzee: User Details", f"Should redirect to user_details.html")
            feedback_element = self.browser.find_element(By.ID, "feedback")
            print(username, feedback_element.text)
            self.assertTrue(len(feedback_element.text)>10, "Substantial feedback should be provided.")

            new_user = self.UserModel.get(username=username)
            self.assertEqual(new_user["status"], "error", "Invalid username should not be added to DB.")

        for password in self.invalid_passwords:
            self.browser.get(f"{self.url}/{self.valid_users[2]['username']}")
            username = "hey_yo_lets_go123"
            self.enter_and_submit_user_info(username, password, "hi@gmail.com")
            wait(self.browser, 0.5)

            self.assertEqual(self.browser.title, "Yahtzee: User Details", f"Should redirect to user_details.html")
            feedback_element = self.browser.find_element(By.ID, "feedback")
            print(password, feedback_element.text)
            self.assertTrue(len(feedback_element.text)>10, "Substantial feedback should be provided.")

            new_user = self.UserModel.get(username=username)
            self.assertEqual(new_user["status"], "error", "Invalid passowrd should not be added to DB.")

        for email in self.invalid_emails:
            self.browser.get(f"{self.url}/{self.valid_users[2]['username']}")
            username = "hey_yo_lets_go123"
            self.enter_and_submit_user_info(username, "12345_abscd", email)
            wait(self.browser, 1)

            self.assertEqual(self.browser.title, "Yahtzee: User Details", f"Should redirect to user_details.html")

            #type='email' prevents bad emails from being used
            #feedback_element = self.browser.find_element(By.ID, "feedback")
            #self.assertTrue(len(feedback_element.text)>10, "Substantial feedback should be provided.")

            new_user = self.UserModel.get(username=username)
            self.assertEqual(new_user["status"], "error", "Invalid email should not be added to DB.")

        print("test_update_user_invalid_info... test passed!")

    def test_update_user_duplicate_info(self):
        """update user - Invalid info"""
        for user in self.valid_users:
            self.browser.get(self.url)
            self.enter_and_submit_user_info(user["username"], user["password"], user["email"])
            wait(self.browser, 2).until_not(EC.title_is(self.user_details_create_requirements["title"]))
        
        #Duplicate username
        self.browser.get(f"{self.url}/{self.valid_users[2]['username']}")
        duplicate_username= self.valid_users[1]['username']
        self.enter_and_submit_user_info(duplicate_username, "12345_abcde", "hi@gmail.com")
        wait(self.browser, 0.5)

        self.assertEqual(self.browser.title, "Yahtzee: User Details", f"Should redirect to user_details.html")
        feedback_element = self.browser.find_element(By.ID, "feedback")
        self.assertTrue(len(feedback_element.text)>10, "Substantial feedback should be provided.")

        #Duplicate email
        self.browser.get(f"{self.url}/{self.valid_users[2]['username']}")
        duplicate_email= self.valid_users[0]['email']
        self.enter_and_submit_user_info(self.valid_users[2]['username'], duplicate_email, "hi@gmail.com")
        wait(self.browser, 0.5)

        self.assertEqual(self.browser.title, "Yahtzee: User Details", f"Should redirect to user_details.html")
        feedback_element = self.browser.find_element(By.ID, "feedback")
        self.assertTrue(len(feedback_element.text)>10, "Substantial feedback should be provided.")

        print("test_update_user_duplicate_info... test passed!")
    
    #------------------DELETE tests-----------------
    def test_delete_user_exits(self):
        """Delete user - Username exists"""
        for user in self.valid_users:
            self.browser.get(self.url)
            self.enter_and_submit_user_info(user["username"], user["password"], user["email"])
            wait(self.browser, 2).until_not(EC.title_is(self.user_details_update_requirements["title"]))

        username_to_delete= self.valid_users[1]["username"]
        self.browser.get(f"{self.url}/{username_to_delete}")
        submit_button=self.browser.find_element(By.ID, 'user_details_delete_submit')
        submit_button.click()
        wait(self.browser, 1)

        user = self.UserModel.get(username=username_to_delete)
        self.assertEqual(user["status"], "error", f"{username_to_delete} should no longer exist in DB.")

        print("test_delete_user_exits... test passed!")
  
    def test_delete_user_DNE(self):
        """Delete user - Username doesn't exist"""
        self.browser.get(self.url+"/hello_hello")
        bad_username = "fake_username"
        wait(self.browser, 1)

        feedback_element = self.browser.find_element(By.ID, "feedback")
        self.assertTrue(len(feedback_element.text)>10, "Substantial feedback should be provided.")

        user = self.UserModel.get(username=bad_username)
        self.assertEqual(user["status"], "error", "Invalid user_info should not be added to DB.")

        print("test_delete_user_DNE... test passed!")
   
    
if __name__ == '__main__':
    unittest.main()