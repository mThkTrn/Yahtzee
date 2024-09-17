#python3 -m pip install selenium pytest

import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

class Basic_Web_Tests(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        #Runs once, before any tests are run
        self.url='127.0.0.1:8000'
        #self.url='http://127.0.0.1:8080'
        self.login_info={
            "title": 'Yahtzee: Login',
            "username_element": "username_input",
            "username":"super_mario",
            "password_element": "password_input",
            "password":"123@456!",
            "submit_element":"login_submit"
        }

    def setUp(self):
        #Runs before every test
        self.browser = webdriver.Chrome()
        self.addCleanup(self.browser.quit)

    def test_0(self):
        """login.html page title says 'Yahtzee: Login'."""
        self.browser.get(self.url)
        expected = self.login_info['title']
        actual = self.browser.title
        self.assertEqual(actual, expected, f"The page title for login.html should be {expected}")
    
    def test_1(self):
        """Submit username, password information"""
        self.browser.get(self.url)

        #footer of login page
        try:
            footer_element_login = self.browser.find_element(By.TAG_NAME, "footer")
        except:
            self.fail(f"<footer> element does not exist!")

        #Username input exists
        try:
            username_element = self.browser.find_element(By.ID, self.login_info["username_element"])
        except:
            self.fail(f"{self.login_info['username_element']} element does not exist!")
        username_element.send_keys(self.login_info["username"])

        #Password input exists
        try:
            password_element = self.browser.find_element(By.ID,self.login_info["password_element"])
        except:
            self.fail(f"{self.login_info['password_element']} element does not exist!")
        password_element.send_keys(self.login_info["password"])

        #Submit Button exists
        try:
            login_submit_button=self.browser.find_element(By.ID,'login_submit')
        except:
            self.fail(f"{self.login_info['submit_element']} element does not exist!")
        self.browser.save_screenshot('login_input.png') #for debugging purposes
        login_submit_button.click()

        #Title of new page
        self.browser.save_screenshot('game_page.png') #for debugging purposes
        expected = f'Yahtzee: {self.login_info["username"]}'
        actual = self.browser.title
        self.assertEqual(actual, expected, f"The page title for game.html should be {expected}")

        #<h1> of new page
        try:
            h1_element = self.browser.find_element(By.TAG_NAME, "h1")
        except:
            self.fail(f"<h1> element does not exist!")
        expected = f'Yahtzee: {self.login_info["username"]}'
        self.assertEqual(expected, h1_element.text, f"The <h1> for game.html should be {expected}")
    
    def test_2(self):
        """Footer information"""
        self.browser.get(self.url)

        #footer of login page
        try:
            footer_element_login = self.browser.find_element(By.TAG_NAME, "footer")
        except:
            self.fail(f"<footer> element in login page does not exist!")
        login_text = footer_element_login.text
        #Username input exists
        try:
            username_element = self.browser.find_element(By.ID, self.login_info["username_element"])
        except:
            self.fail(f"{self.login_info['username_element']} element does not exist!")
        username_element.send_keys(self.login_info["username"])

        #Password input exists
        try:
            password_element = self.browser.find_element(By.ID,self.login_info["password_element"])
        except:
            self.fail(f"{self.login_info['password_element']} element does not exist!")
        password_element.send_keys('123@456!')

        #Submit Button exists
        try:
            login_submit_button=self.browser.find_element(By.ID,'login_submit')
        except:
            self.fail(f"{self.login_info['submit_element']} element does not exist!")
        login_submit_button.click()

        #footer of new page
        try:
            footer_element_next = self.browser.find_element(By.TAG_NAME, "footer")
        except:
            self.fail(f"<footer> element in next page does not exist!")
       
        self.assertEqual(login_text, footer_element_next.text, "footer text should be the same on login and game page.")


if __name__ == '__main__':
    unittest.main()