import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains 

import random

class Feedback_UI_Tests(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        #Runs once, before any tests are run
        self.url='http://127.0.0.1:8080/game?username=super_mario&password=123@456!'
        self.upper_categories= ["one", "two", "three", "four", "five", "six"]
        self.lower_categories= ["three_of_a_kind", "four_of_a_kind", "full_house", "small_straight", "large_straight", "yahtzee", "chance"]
        
    def setUp(self):
        self.browser = webdriver.Chrome()
        self.addCleanup(self.browser.quit)

    def test_load_nonexistent_game_bad(self): 
        self.browser.get(self.url)

        self.browser.execute_script(f"localStorage.removeItem('yahtzee');")
        
        load_button=self.browser.find_element(By.ID, f"load_game")
        load_button.click()
        
        feedback_element = self.browser.find_element(By.ID, "feedback")
        self.assertTrue("bad" in feedback_element.get_attribute("class")) #feedback element should be styled "bad"
        self.assertFalse("good" in feedback_element.get_attribute("class")) #feedback element should not be styled "good"
        self.assertTrue( len(feedback_element.text) > 10) #checks for significant feedback        
            
        print("test_load_nonexistent_game_bad passed")
    
    def test_roll_too_many_times_bad(self): 
        self.browser.get(self.url)
        try:
            roll_button = self.browser.find_element(By.ID, "roll_button")
        except:
            self.fail("roll_button element does not exist!")

        roll_button.click()
        roll_button.click()
        roll_button.click()
        roll_button.click() #press roll 4 times

        feedback_element = self.browser.find_element(By.ID, "feedback")
        self.assertTrue("bad" in feedback_element.get_attribute("class")) #feedback element should be styled "bad"
        self.assertFalse("good" in feedback_element.get_attribute("class")) #feedback element should not be styled "good"
        self.assertTrue( len(feedback_element.text) > 10) #checks for significant feedback 
            
        print("test_roll_too_many_times_bad passed")
    
    def test_enter_score_with_blank_dice_bad(self): 
        for category in self.upper_categories +self.lower_categories :
            self.browser.get(self.url)
            #dice are blank
            category_input=self.browser.find_element(By.ID, f"{category}_input")
            category_input.send_keys("0"+Keys.RETURN)

            feedback_element = self.browser.find_element(By.ID, "feedback")
                    
            self.assertTrue("bad" in feedback_element.get_attribute("class")) #feedback element should be styled "bad"
            self.assertFalse("good" in feedback_element.get_attribute("class")) #feedback element should not be styled "good"
            self.assertTrue( len(feedback_element.text) > 10) #checks for significant feedback
                      
        print("test_enter_score_with_blank_dice_bad passed")

    def test_enter_score_upper(self): 
        self.browser.get(self.url)
        upper_tests={
            "one" : [
                [0, [6, 2, 3, 4, 5], True],
                [1,[1, 2, 3, 4, 5], True],
                [2,[1, 2, 3, 1, 5], True],
                [3,[1, 2, 1, 1, 5], True],
                [4,[1, 2, 1, 1, 1], True],
                [5,[1, 1, 1, 1, 1], True],
                [0, [0,0,0,0,0], False],
                [-4, [1, 2, 3, 4, 5], False],
                [4, [1, 2, 3, 4, 5], False],
                ["", [1, 2, 3, 4, 5], False],
                [" ", [1, 2, 3, 4, 5], False],
                ["four", [1, 2, 1, 1, 1], False]
            ],
            "two":[
                [0,[6, 1, 3, 4, 5],True],
                [2,[1, 2, 3, 4, 5],True],
                [4,[1, 2, 3, 2, 5],True],
                [6,[1, 2, 2, 2, 5],True],
                [8,[2, 2, 2, 2, 1],True],
                [10,[2, 2, 2, 2, 2],True],
                [0, [0,0,0,0,0], False],
                [4, [1, 2, 3, 4, 5], False],
                [-4, [1, 2, 3, 4, 5], False],
                ["", [1, 2, 3, 4, 5], False],
                [" ", [1, 2, 3, 4, 5], False],
                ["two", [1, 2, 1, 1, 1], False]
            ],
            "three":[
                [0,[6, 1, 2, 4, 5],True],
                [3,[1, 2, 3, 4, 5],True],
                [6,[1, 2, 3, 3, 5],True],
                [9,[3, 2, 3, 2, 3],True],
                [12,[3, 2, 3, 3, 3],True],
                [15,[3, 3, 3, 3, 3],True],
                [0, [0,0,0,0,0], False],
                [4, [1, 2, 3, 4, 5], False],
                [-4, [1, 2, 3, 4, 5], False],
                ["", [1, 2, 3, 4, 5], False],
                [" ", [1, 2, 3, 4, 5], False],
                ["three", [1, 2, 3, 1, 1], False]
            ],
            "four":[
                [0,[2, 3, 5, 6, 1],True],
                [4,[1, 2, 3, 4, 5],True],
                [8,[1, 4, 4, 2, 5],True],
                [12,[4, 4, 2, 4, 5],True],
                [16,[4, 4, 2, 4, 4],True],
                [20,[4, 4, 4, 4, 4],True],
                [0, [0,0,0,0,0], False],
                [8, [1, 2, 3, 4, 5], False],
                [-8, [1, 2, 3, 4, 5], False],
                ["", [1, 2, 3, 4, 5], False],
                [" ", [1, 2, 3, 4, 5], False],
                ["four", [1, 2, 1, 1, 1], False]
            ],
            "five":[
                [0,[1, 2, 3, 4, 6],True],
                [5,[1, 2, 3, 4, 5],True],
                [10,[1, 5, 3, 2, 5],True],
                [15,[1, 5, 5, 2, 5],True],
                [20,[5, 5, 5, 5, 1],True],
                [25,[5, 5, 5, 5, 5],True],
                [0, [0,0,0,0,0], False],
                [10, [1, 2, 3, 4, 5], False],
                [-10, [1, 2, 3, 4, 5], False],
                ["", [1, 2, 3, 4, 5], False],
                [" ", [1, 2, 3, 4, 5], False],
                ["five", [1, 2, 1, 5, 1], False]
            ],
            "six":[
                [0,[5, 5, 4, 3, 2],True],
                [6,[1, 2, 6, 4, 5],True],
                [12,[1, 6, 3, 6, 5],True],
                [18,[1, 2, 6, 6, 6],True],
                [24,[6, 6, 6, 2, 6],True],
                [30,[6, 6, 6, 6, 6],True],
                [0, [0,0,0,0,0], False],
                [6, [1, 2, 3, 4, 5], False],
                [-6, [1, 2, 3, 4, 5], False],
                ["", [1, 2, 3, 4, 5], False],
                [" ", [1, 2, 3, 4, 5], False],
                ["six", [1, 2, 6, 1, 1], False]
            ]
        }

        for category in self.upper_categories:
            for test in upper_tests[category]:
                self.browser.get(self.url)
                self.browser.execute_script(f"window.dice.set({test[1]}, 2);")
                #self.browser.save_screenshot(f"{category}_input.png")
                category_input=self.browser.find_element(By.ID, f"{category}_input")
                category_input.send_keys(str(test[0])+Keys.RETURN)
                #self.browser.save_screenshot(f"{category}_input_after_enter.png")

                feedback_element = self.browser.find_element(By.ID, "feedback")
                if not test[2]:
                    self.assertTrue("bad" in feedback_element.get_attribute("class")) #feedback element should be styled "bad"
                    self.assertFalse("good" in feedback_element.get_attribute("class")) #feedback element should not be styled "good"
                    self.assertTrue( len(feedback_element.text) > 10) #checks for significant feedback
                else:
                    self.assertTrue("good" in feedback_element.get_attribute("class")) #feedback element should be styled "good"
                    self.assertFalse("bad" in feedback_element.get_attribute("class")) #feedback element should not be styled "bad"
                    self.assertTrue( len(feedback_element.text) > 10) #checks for significant feedback
                  
        print("test_enter_score_upper passed")  

    def test_enter_score_lower(self): 
        lower_tests={
            "three_of_a_kind":[
                [7,[1, 1, 1, 2, 2],True],
                [7,[1, 1, 2, 1, 2],True],
                [7,[1, 1, 2, 2, 1],True],
                [7,[1, 2, 1, 1, 2],True],
                [11,[1, 2, 1, 6, 1],True],
                [8,[2, 1, 1, 1, 3],True],
                [7,[2, 1, 1, 2, 1],True],
                [18,[4, 5, 3, 3, 3],True],
                [18,[4, 3, 5, 3, 3],True],
                [18,[3, 4, 5, 3, 3],True],
                [27,[6, 4, 6, 5, 6],True],
                [9,[2, 2, 2, 1, 2],True],
                [16,[3, 3, 4, 3, 3],True],
                [21,[4, 5, 4, 4, 4],True],
                [26,[6, 5, 5, 5, 5],True],
                [20,[4, 4, 4, 4, 4],True],
                [25,[5, 5, 5, 5, 5],True],
                [30,[6, 6, 6, 6, 6],True],
                [0,[2, 3, 4, 4, 5],True],
                [0, [0,0,0,0,0], False],
                [6, [1, 3, 3, 3, 5], False],
                [4, [1, 2, 1, 1, 1], False],
                [-3, [1, 2, 3, 4, 5], False],
                ["", [1, 2, 3, 4, 5], False],
                [" ", [1, 2, 3, 4, 5], False],
                ["four", [1, 2, 1, 1, 1], False]
            ],
            "four_of_a_kind":[
                [6,[1, 1, 1, 1, 2],True],
                [9,[2, 2, 2, 1, 2],True],
                [16,[3, 3, 4, 3, 3],True],
                [21,[4, 5, 4, 4, 4],True],
                [26,[6, 5, 5, 5, 5],True],
                [20,[4, 4, 4, 4, 4],True],
                [25,[5, 5, 5, 5, 5],True],
                [30,[6, 6, 6, 6, 6],True],
                [0,[4, 5, 5, 5, 6],True],
                [0, [0,0,0,0,0], False],
                [12, [1, 3, 3, 3, 3], False],
                [3, [1, 2, 1, 1, 1], False],
                [-3, [1, 2, 3, 4, 5], False],
                ["", [1, 2, 3, 4, 5], False],
                [" ", [1, 2, 3, 4, 5], False],
                ["six", [1, 2, 1, 1, 1], False]
            ],
            "full_house":[
                [25,[1, 1, 1, 2, 2],True],
                [25,[1, 1, 2, 1, 2],True],
                [25,[1, 1, 2, 2, 1],True],
                [25,[1, 2, 1, 1, 2],True],
                [25,[1, 2, 1, 2, 1],True],
                [25,[3, 1, 1, 1, 3],True],
                [25,[2, 1, 1, 2, 1],True],
                [25,[5, 5, 3, 3, 3],True],
                [25,[5, 3, 5, 3, 3],True],
                [25,[3, 5, 5, 3, 3],True],
                [25,[6, 5, 6, 5, 6],True],
                [0,[3, 3, 3, 3, 3],True],
                [0, [0,0,0,0,0], False],
                [11, [1, 3, 3, 3, 1], False],
                [25, [1, 1, 1, 1, 1], False],
                [-25, [2, 2, 3, 3, 3], False],
                ["", [1, 2, 3, 4, 5], False],
                [" ", [1, 2, 3, 4, 5], False],
                ["full-house", [1, 2, 2, 1, 1], False]
            ],
            "small_straight":[
                [30,[1, 2, 3, 4, 5],True],
                [30,[1, 2, 3, 4, 6],True],
                [30,[2, 3, 4, 5, 6],True],
                [30,[2, 2, 3, 4, 5],True],
                [30,[2, 3, 4, 5, 3],True],
                [30,[1, 2, 3, 4, 5],True],
                [30,[4, 3, 4, 5, 6],True],
                [30,[2, 3, 4, 3, 1],True],
                [30,[2, 3, 4, 6, 1],True],
                [0,[1, 2, 3, 5, 6],True],
                [0, [0,0,0,0,0], False],
                [30, [1, 3, 3, 3, 1], False],
                [25, [1, 2, 3, 4, 1], False],
                [-30, [2, 3, 4, 5, 6], False],
                ["", [1, 2, 3, 4, 5], False],
                [" ", [1, 2, 3, 4, 5], False],
                ["small-straight", [1, 2, 3, 4, 1], False]
            ],
            "large_straight":[
                [40,[1, 2, 3, 4, 5],True],
                [40,[3, 2, 1, 4, 5],True],
                [40,[1, 4, 3, 5, 2],True],
                [40,[2, 3, 4, 5, 6],True],
                [40,[4, 5, 3, 2, 6],True],
                [40,[2, 5, 3, 4, 6],True],
                [0,[1, 2, 3, 4, 6],True],
                [0, [0,0,0,0,0], False],
                [40, [1, 3, 3, 3, 1], False],
                [30, [1, 2, 3, 4, 5], False],
                [-40, [2, 3, 4, 5, 6], False],
                ["", [1, 2, 3, 4, 5], False],
                [" ", [1, 2, 3, 4, 5], False],
                ["large-straight", [1, 2, 3, 4, 5], False]
            ],
            "yahtzee":[
                [50,[1, 1, 1, 1, 1],True],
                [50,[2, 2, 2, 2, 2],True],
                [50,[3, 3, 3, 3, 3],True],
                [50,[4, 4, 4, 4, 4],True],
                [50,[5, 5, 5, 5, 5],True],
                [50,[6, 6, 6, 6, 6],True],
                [0,[3, 3, 3, 4, 3],True],
                [0, [0,0,0,0,0], False],
                [50, [1, 3, 3, 3, 1], False],
                [25, [2, 2, 2, 2, 2], False],
                [-50, [4, 4, 4, 4, 4], False],
                ["", [1, 2, 3, 4, 5], False],
                [" ", [1, 2, 3, 4, 5], False],
                ["yahtzee", [2, 2, 2, 2, 2], False]
            ],
            "chance":[
                [6,[1, 1, 1, 1, 2],True],
                [9,[2, 2, 2, 1, 2],True],
                [16,[3, 3, 4, 3, 3],True],
                [21,[4, 5, 4, 4, 4],True],
                [26,[6, 5, 5, 5, 5],True],
                [0, [0,0,0,0,0], False],
                [25, [5, 5, 5, 5, 4], False],
                ["", [1, 2, 3, 4, 5], False],
                [" ", [1, 2, 3, 4, 5], False],
                ["chance", [1, 2, 3, 4, 1], False]
            ]
        }
        for category in self.lower_categories:
            for test in lower_tests[category]:
                self.browser.get(self.url)
                self.browser.execute_script(f"window.dice.set({test[1]}, 2);")
                #self.browser.save_screenshot(f"{category}_input.png")
                category_input=self.browser.find_element(By.ID, f"{category}_input")
                category_input.send_keys(str(test[0])+Keys.RETURN)
                #self.browser.save_screenshot(f"{category}_input_after_enter.png")

                feedback_element = self.browser.find_element(By.ID, "feedback")
                if not test[2]:
                    self.assertTrue("bad" in feedback_element.get_attribute("class")) #feedback element should be styled "bad"
                    self.assertFalse("good" in feedback_element.get_attribute("class")) #feedback element should not be styled "good"
                    self.assertTrue( len(feedback_element.text) > 10) #checks for significant feedback
                else:
                    self.assertTrue("good" in feedback_element.get_attribute("class")) #feedback element should be styled "good"
                    self.assertFalse("bad" in feedback_element.get_attribute("class")) #feedback element should not be styled "bad"
                    self.assertTrue( len(feedback_element.text) > 10) #checks for significant feedback
        print("test_enter_score_lower passed")

    def test_new_game_good(self): 
        self.browser.get(self.url)
        try:
            roll_button = self.browser.find_element(By.ID, "roll_button")
        except:
            self.fail("roll_button element does not exist!")

        feedback_element = self.browser.find_element(By.ID, "feedback")
        self.assertTrue("good" in feedback_element.get_attribute("class")) #feedback element should be styled "good"
        self.assertFalse("bad" in feedback_element.get_attribute("class")) #feedback element should not be styled "bad"
        self.assertTrue( len(feedback_element.text) > 10) #checks for significant feedback 
        print("test_new_game_good passed")

    def test_successful_save_good(self): 
        self.browser.get(self.url)
        feedback_element = self.browser.find_element(By.ID, "feedback")
        score_entries=[
            [[2,3,5,6,5],"two", 2],
            [[1,3,3,3,3], "three", 12],
            [[4,4,3,4,4], "four", 16],
            [[5, 5, 3, 3, 3], "full_house", 25],
            [[2, 2, 3, 4, 5], "small_straight", 30],
            [[1, 2, 6, 4, 5], "large_straight", 0],
            [[5, 5, 5, 5, 5], "yahtzee", 50]
        ]
        for entry in score_entries:
            self.browser.execute_script(f"window.dice.set({entry[0]}, 2);")
            category_input=self.browser.find_element(By.ID, f"{entry[1]}_input")
            category_input.send_keys(str(entry[2])+Keys.RETURN)
            original_feedback = feedback_element.text

        save_button=self.browser.find_element(By.ID, f"save_game")
        save_button.click()

        self.assertTrue("good" in feedback_element.get_attribute("class")) #feedback element should be styled "good"
        self.assertFalse("bad" in feedback_element.get_attribute("class")) #feedback element should not be styled "bad"
        self.assertTrue( len(feedback_element.text) > 10) #checks for significant feedback        
        self.assertTrue( original_feedback != feedback_element.text) #feedback should change  
        
        print("test_successful_save_good passed")   

    def test_successful_load_good(self): 
        self.browser.get(self.url)
        score_entries=[
            [[2,3,5,6,5],"two", 2],
            [[1,3,3,3,3], "three", 12],
            [[4,4,3,4,4], "four", 16],
            [[5, 5, 3, 3, 3], "full_house", 25],
            [[2, 2, 3, 4, 5], "small_straight", 30],
            [[1, 2, 6, 4, 5], "large_straight", 0],
            [[5, 5, 5, 5, 5], "yahtzee", 50]
        ]
        for entry in score_entries:
            self.browser.execute_script(f"window.dice.set({entry[0]}, 2);")
            category_input=self.browser.find_element(By.ID, f"{entry[1]}_input")
            category_input.send_keys(str(entry[2])+Keys.RETURN)        
        
        self.browser.execute_script(f"localStorage.setItem('yahtzee', JSON.stringify(window.gamecard.to_object()));")
        
        feedback_element = self.browser.find_element(By.ID, "feedback")
        original_feedback = feedback_element.text
        load_button=self.browser.find_element(By.ID, f"load_game")
        load_button.click()

        self.assertTrue("good" in feedback_element.get_attribute("class")) #feedback element should be styled "good"
        self.assertFalse("bad" in feedback_element.get_attribute("class")) #feedback element should not be styled "bad"
        self.assertTrue( len(feedback_element.text) > 10) #checks for significant feedback  
        self.assertTrue( original_feedback != feedback_element.text) #feedback should change  

        print("test_successful_load_good passed")   
    
    def test_finish_game_good(self): 
        self.browser.get(self.url)
        feedback_element = self.browser.find_element(By.ID, "feedback")
        score_entries=[
            [[2,3,5,6,5],"one", 0],
            [[2,3,5,6,5],"two", 2],
            [[1,3,3,3,3], "three", 12],
            [[4,4,3,4,4], "four", 16],
            [[1,6,5,6,5],"five", 10],
            [[6,6,6,6,5],"six", 24],
            [[5, 2, 5, 5, 3],"three_of_a_kind", 20],
            [[5, 2, 5, 5, 3],"four_of_a_kind", 0],
            [[5, 5, 3, 3, 3], "full_house", 25],
            [[2, 2, 3, 4, 5], "small_straight", 30],
            [[1, 2, 6, 4, 5], "large_straight", 0],
            [[5, 5, 5, 5, 5], "yahtzee", 50],
            [[5, 2, 5, 5, 3],"chance", 20]
        ]
        for entry in score_entries:
            self.browser.execute_script(f"window.dice.set({entry[0]}, 2);")
            category_input=self.browser.find_element(By.ID, f"{entry[1]}_input")
            self.browser.save_screenshot(f"pre_completed_game.png")
            original_feedback = feedback_element.text
            category_input.send_keys(str(entry[2])+Keys.RETURN)        
        
        self.browser.save_screenshot(f"completed_game.png")

        self.assertTrue("good" in feedback_element.get_attribute("class")) #feedback element should be styled "good"
        self.assertFalse("bad" in feedback_element.get_attribute("class")) #feedback element should not be styled "bad"
        self.assertTrue( len(feedback_element.text) > 10) #checks for significant feedback  
        self.assertTrue( original_feedback != feedback_element.text) #feedback should change after game is completed
        print("test_finish_game_good passed")  

    def test_feedback_cleared_with_new_roll(self): 
        self.browser.get(self.url)
        feedback_element = self.browser.find_element(By.ID, "feedback")
        score_entries=[
            [[2,3,5,6,5],"one", 0],
            [[1,6,5,6,5],"five", 10],
            [[6,6,6,6,5],"six", 24],
            [[5, 2, 5, 5, 3],"three_of_a_kind", 20],
            [[1, 2, 6, 4, 5], "large_straight", 0],
            [[5, 5, 5, 5, 5], "yahtzee", 50],
            [[5, 2, 5, 5, 3],"chance", 20]
        ]
        for entry in score_entries:
            self.browser.execute_script(f"window.dice.set({entry[0]}, 2);")
            category_input=self.browser.find_element(By.ID, f"{entry[1]}_input")
            original_feedback = feedback_element.text
            category_input.send_keys(str(entry[2])+Keys.RETURN)        
        
        self.browser.save_screenshot(f"completed_game.png")

        try:
            roll_button = self.browser.find_element(By.ID, "roll_button")
        except:
            self.fail("roll_button element does not exist!")
        roll_button.click()

        self.assertFalse("good" in feedback_element.get_attribute("class")) #feedback element should not be styled "good"
        self.assertFalse("bad" in feedback_element.get_attribute("class")) #feedback element should not be styled "bad"
        self.assertTrue( len(feedback_element.text) == 0) #checks for significant feedback  
        self.assertTrue( original_feedback != feedback_element.text) #feedback should change after game is completed
            
        print("test_feedback_cleared_with_new_roll passed")    

if __name__ == '__main__':
    unittest.main()