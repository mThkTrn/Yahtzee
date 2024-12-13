import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

import random
import json

class Gameplay_Tests(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        #Runs once, before any tests are run
        self.url='http://127.0.0.1:8080/game?username=super_mario&password=123@456!'
        self.dice_labels= ["blank","one", "two", "three", "four", "five", "six"]
        self.upper_categories= ["one", "two", "three", "four", "five", "six"]
        self.lower_categories= ["three_of_a_kind", "four_of_a_kind", "full_house", "small_straight", "large_straight", "yahtzee", "chance"]
        self.score_elements=["upper_score", "upper_bonus", "upper_total", "lower_score", "upper_total_lower", "grand_total"]
        self.score_info_finished={
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

    def setUp(self):
        options = Options()
        options.add_argument('--headless=new')
        self.browser = webdriver.Chrome(options=options)
        self.addCleanup(self.browser.quit)

    def test_player_allowed_3_rolls_max(self): 
        self.browser.get(self.url)
        try:
            roll_button = self.browser.find_element(By.ID, "roll_button")
        except:
            self.fail("roll_button element does not exist!")
        roll_button.click()
        roll_button.click()
        roll_button.click()

        current_dice=[]
        for d in range(5):
            die_el = self.browser.find_element(By.ID, f"die_{d}")
            label = die_el.get_attribute("src").split("/")[-1][:-4]
            current_dice.append(label)
        
        roll_button.click()

        for d in range(5):
            die_el = self.browser.find_element(By.ID, f"die_{d}")
            label = die_el.get_attribute("src").split("/")[-1][:-4]
            
            self.assertTrue(current_dice[d] == label)

        roll_button.click()

        for d in range(5):
            die_el = self.browser.find_element(By.ID, f"die_{d}")
            label = die_el.get_attribute("src").split("/")[-1][:-4]
            
            self.assertTrue(current_dice[d] == label)
            
        print("test_player_allowed_3_rolls_max passed")
    
    def test_player_must_enter_score_even_0(self): 
        self.browser.get(self.url)
        almost_straigt = [1, 2, 4, 5, 6]
        self.browser.execute_script(f"window.dice.set({almost_straigt}, 0);")
        try:
            roll_button = self.browser.find_element(By.ID, "roll_button")
        except:
            self.fail("roll_button element does not exist!")
        roll_button.click()

        for d in range(5):
            die_el = self.browser.find_element(By.ID, f"die_{d}")
            label = die_el.get_attribute("src").split("/")[-1][:-4]
            self.assertTrue(almost_straigt[d] == self.dice_labels.index(label))  

        roll_button.click()

        for d in range(5):
            die_el = self.browser.find_element(By.ID, f"die_{d}")
            label = die_el.get_attribute("src").split("/")[-1][:-4]
            self.assertTrue(almost_straigt[d] == self.dice_labels.index(label)) 
        
        category_input=self.browser.find_element(By.ID, f"one_input")
        category_input.send_keys(str(1)+Keys.RETURN) 
        
        for d in range(5):
            die_el = self.browser.find_element(By.ID, f"die_{d}")
            label = die_el.get_attribute("src").split("/")[-1][:-4]
            self.assertTrue(0 == self.dice_labels.index(label)) 

        print("test_player_must_enter_score_even_0 passed")
    
    def test_prevent_entry_invalid_scores(self): 
        self.browser.get(self.url)

        self.browser.execute_script(f"window.dice.set([3, 3, 6, 3, 6], 1);")

        category_input=self.browser.find_element(By.ID, f"full_house_input")
        category_input.send_keys(str(21)+Keys.RETURN)          
        self.assertTrue(category_input.is_enabled())  

        category_input=self.browser.find_element(By.ID, f"three_input")
        category_input.send_keys(str(21)+Keys.RETURN)          
        self.assertTrue(category_input.is_enabled())  

        category_input=self.browser.find_element(By.ID, f"chance_input")
        category_input.send_keys(str(21)+Keys.RETURN)          
        self.assertFalse(category_input.is_enabled()) 

        print("test_prevent_entry_invalid_scores passed")
    
    def test_prevent_dice_rolls_for_finished_games(self): 
        self.browser.get(self.url)

        self.browser.execute_script(f"window.gamecard.load_scorecard(JSON.parse('{json.dumps(self.score_info_finished)}'));")
        current_dice=[]
        for d in range(5):
            die_el = self.browser.find_element(By.ID, f"die_{d}")
            label = die_el.get_attribute("src").split("/")[-1][:-4]
            current_dice.append(label)

        try:
            roll_button = self.browser.find_element(By.ID, "roll_button")
        except:
            self.fail("roll_button element does not exist!")
        roll_button.click()

        for d in range(5):
            die_el = self.browser.find_element(By.ID, f"die_{d}")
            label = die_el.get_attribute("src").split("/")[-1][:-4]
            
            self.assertTrue(current_dice[d] == label)  
        
        roll_button.click()

        for d in range(5):
            die_el = self.browser.find_element(By.ID, f"die_{d}")
            label = die_el.get_attribute("src").split("/")[-1][:-4]
            
            self.assertTrue(current_dice[d] == label)  
            
        print("test_prevent_dice_rolls_for_finished_games passed")
    
    def test_dice_reset_after_valid_score(self): 
        # blank and unreserved
        self.browser.get(self.url)
        self.browser.execute_script(f"window.dice.set([3, 3, 6, 3, 6], 1);")
        category_input=self.browser.find_element(By.ID, f"full_house_input")
        category_input.send_keys(str(25)+Keys.RETURN) 

        for d in range(5):
            die_el = self.browser.find_element(By.ID, f"die_{d}")
            self.assertTrue("blank" in die_el.get_attribute("src"))  
            self.assertTrue("reserved" not in die_el.get_attribute("class"))  
            
        print("test_dice_reset_after_valid_score passed")
    
    def test_new_game_blank_totals_and_categories(self): 
        self.browser.get(self.url)

        for category in self.lower_categories+self.upper_categories:
            category_el = self.browser.find_element(By.ID, f"{category}_input")
            self.assertTrue(category_el.is_enabled())
            self.assertTrue(category_el.get_attribute("value")=="")       
        
        for score in self.score_elements:
            score_el = self.browser.find_element(By.ID, f"{score}")
            self.assertTrue(score_el.text=="") 

        print("test_new_game_blank_totals_and_categories passed")


if __name__ == '__main__':
    unittest.main()