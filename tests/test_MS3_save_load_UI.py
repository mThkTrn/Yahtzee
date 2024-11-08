import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import random
import json

class Save_Load_UI_Tests(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        #Runs once, before any tests are run
        self.url='http://127.0.0.1:8080/game?username=super_mario&password=123@456!'
        self.upper_categories= ["one", "two", "three", "four", "five", "six"]
        self.lower_categories= ["three_of_a_kind", "four_of_a_kind", "full_house", "small_straight", "large_straight", "yahtzee", "chance"]
        self.score_elements=["upper_score", "upper_bonus", "upper_total", "lower_score", "upper_total_lower", "grand_total"]
        self.score_info_partial_bonus={
            "rolls_remaining":1,
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
    def setUp(self):
        self.browser = webdriver.Chrome()
        self.addCleanup(self.browser.quit)

    def test_save_incomplete_game(self): 
        self.browser.get(self.url)
        self.browser.execute_script(f"localStorage.removeItem('yahtzee');")#clear any old games

        self.browser.execute_script(f"window.gamecard.load_scorecard(JSON.parse('{json.dumps(self.score_info_partial_bonus)}'));")
        load_button=self.browser.find_element(By.ID, f"save_game")
        load_button.click()

        game = self.browser.execute_script(f"return localStorage.getItem('yahtzee');")
        self.assertTrue(game is not None) #a game with key='yahtzee' should exist          
        self.assertTrue(json.loads(game) == self.score_info_partial_bonus)        
        print("test_save_incomplete_game passed")
    
    def test_only_save_scores_for_disabled_categories(self): 
        self.browser.get(self.url)
        self.browser.execute_script(f"localStorage.removeItem('yahtzee');")#clear any old games

        self.browser.execute_script(f"window.gamecard.load_scorecard(JSON.parse('{json.dumps(self.score_info_partial_bonus)}'));")
        
        #type input, but don't hit enter
        self.browser.execute_script(f"window.dice.set([3, 3, 3, 3, 3], 1);")
        category_input=self.browser.find_element(By.ID, f"three_input")
        category_input.send_keys(str(15)) 
        category_input=self.browser.find_element(By.ID, f"three_of_a_kind_input")
        category_input.send_keys(str(15))
        
        load_button=self.browser.find_element(By.ID, f"save_game")
        load_button.click()

        game = self.browser.execute_script(f"return localStorage.getItem('yahtzee');")
        self.assertTrue(game is not None) #a game with key='yahtzee' should exist          
        self.assertTrue(json.loads(game) == self.score_info_partial_bonus) #only disabled categories are saved       
        print("test_only_save_scores_for_disabled_categories passed")
    
    def test_load_and_disable_categories(self): 
        self.browser.get(self.url)
        self.browser.execute_script(f"window.gamecard.load_scorecard(JSON.parse('{json.dumps(self.score_info_partial_bonus)}'));")

        rolls = self.browser.execute_script(f"return window.dice.get_rolls_remaining();")
        self.assertTrue(rolls == self.score_info_partial_bonus["rolls_remaining"]) 
        for lower_cat in self.lower_categories:
            cat_el = self.browser.find_element(By.ID, f"{lower_cat+'_input'}")
            if self.score_info_partial_bonus["lower"][lower_cat] >= 0:
                self.assertFalse(cat_el.is_enabled())
                self.assertTrue(cat_el.get_attribute("value") == str(self.score_info_partial_bonus["lower"][lower_cat]))
            else:
                self.assertTrue(cat_el.is_enabled()) 
                self.assertTrue(cat_el.text == "")
        
        for upper_cat in self.upper_categories:
            cat_el = self.browser.find_element(By.ID, f"{upper_cat+'_input'}")
            if self.score_info_partial_bonus["upper"][upper_cat] >= 0:
                self.assertFalse(cat_el.is_enabled())
                self.assertTrue(cat_el.get_attribute("value") == str(self.score_info_partial_bonus["upper"][upper_cat]))
            else:
                self.assertTrue(cat_el.is_enabled()) 
                self.assertTrue(cat_el.text == "")

        print("test_load_and_disable_categories passed")
    
    def test_no_error_with_load_nonexistent_game(self): 
        self.browser.get(self.url)
        self.browser.execute_script(f"localStorage.removeItem('yahtzee');")#clear any old games

        self.browser.execute_script(f"window.gamecard.load_scorecard(JSON.parse('{json.dumps(self.score_info_partial_bonus)}'));")

        load_button=self.browser.find_element(By.ID, f"load_game")
        load_button.click()

        for log in self.browser.get_log('browser'): 
            if "favicon" not in log['message']:
                self.assertTrue(False)  #causes an error that isn't a missing favicon        
            
        print("test_no_error_with_load_nonexistent_game passed")

if __name__ == '__main__':
    unittest.main()