import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains 
import json

def get_current_category_values(browser, upper_categories, lower_categories):
   curr_values={};

   curr_values["rolls_remaining"] = browser.execute_script(f"return parseInt(document.getElementById('rolls_remaining').innerText);")
    
   for category in upper_categories+lower_categories:
     curr_values[category] = browser.execute_script(f'return parseInt(document.getElementById("{category}_input").value);');
     if curr_values[category] == None:
        curr_values[category] = -1

   return curr_values;

def get_current_score_values(browser, score_elements):
   curr_values={};
    
   for category in score_elements:
     curr_values[category] = browser.execute_script(f'return parseInt(document.getElementById("{category}").innerHTML);');
   
   return curr_values;

class MS2_Gamecard_Tests(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        #Runs once, before any tests are run
        self.url='http://127.0.0.1:8080/game?username=super_mario&password=123@456!'
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
        self.score_info_finished_no_bonus={
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
        self.score_info_partial={
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
        self.score_info_partial_bonus={
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
        self.score_info_empty={
            "rolls_remaining":3,
            "upper":{
                "one":-1,
                "two":-1,
                "three":-1,
                "four":-1,
                "five":-1,
                "six":-1
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
        self.maxDiff = None
        
    def setUp(self):
        self.browser = webdriver.Chrome()
        self.addCleanup(self.browser.quit)
    
    def test_load_full_scorecard(self):
        self.browser.get(self.url)
        scorecard_info = self.score_info_finished
        self.browser.execute_script(f"window.gamecard.load_scorecard(JSON.parse('{json.dumps(scorecard_info)}'));")
        all_scorecard_values =  get_current_category_values(self.browser, self.upper_categories, self.lower_categories)
    
        for upper_category in self.upper_categories:
            self.assertEqual(all_scorecard_values[upper_category], scorecard_info["upper"][upper_category])
        for lower_category in self.lower_categories:
            self.assertEqual(all_scorecard_values[lower_category], scorecard_info["lower"][lower_category])

        self.assertEqual(all_scorecard_values["rolls_remaining"], scorecard_info["rolls_remaining"])

    def test_load_partial_bonus_scorecard(self):
        self.browser.get(self.url)
        scorecard_info = self.score_info_partial_bonus
        self.browser.execute_script(f"window.gamecard.load_scorecard(JSON.parse('{json.dumps(scorecard_info)}'));")
        all_scorecard_values =  get_current_category_values(self.browser, self.upper_categories, self.lower_categories)
        for upper_category in self.upper_categories:
            self.assertEqual(all_scorecard_values[upper_category], scorecard_info["upper"][upper_category])
        for lower_category in self.lower_categories:
            self.assertEqual(all_scorecard_values[lower_category], scorecard_info["lower"][lower_category])

        self.assertEqual(all_scorecard_values["rolls_remaining"], scorecard_info["rolls_remaining"])
    
    def test_load_empty_scorecard(self):
        self.browser.get(self.url)
        scorecard_info = self.score_info_empty
        self.browser.execute_script(f"window.gamecard.load_scorecard(JSON.parse('{json.dumps(scorecard_info)}'));")
        all_scorecard_values =  get_current_category_values(self.browser, self.upper_categories, self.lower_categories)
    
        for upper_category in self.upper_categories:
            self.assertEqual(all_scorecard_values[upper_category], scorecard_info["upper"][upper_category])
        for lower_category in self.lower_categories:
            self.assertEqual(all_scorecard_values[lower_category], scorecard_info["lower"][lower_category])

        self.assertEqual(all_scorecard_values["rolls_remaining"], scorecard_info["rolls_remaining"])
    
    def test_load_multiple_scorecards(self):
        self.browser.get(self.url)
        scorecard_info = self.score_info_finished
        self.browser.execute_script(f"window.gamecard.load_scorecard(JSON.parse('{json.dumps(scorecard_info)}'));")
        scorecard_info = self.score_info_partial #should erase the previous scorecard
        self.browser.execute_script(f"window.gamecard.load_scorecard(JSON.parse('{json.dumps(scorecard_info)}'));")
        all_scorecard_values =  get_current_category_values(self.browser, self.upper_categories, self.lower_categories)
    
        for upper_category in self.upper_categories:
            self.assertEqual(all_scorecard_values[upper_category], scorecard_info["upper"][upper_category])
        for lower_category in self.lower_categories:
            self.assertEqual(all_scorecard_values[lower_category], scorecard_info["lower"][lower_category])

        self.assertEqual(all_scorecard_values["rolls_remaining"], scorecard_info["rolls_remaining"])
    
    def test_to_object_full_scorecard(self):
        self.browser.get(self.url)
        scorecard_info = self.score_info_finished
        self.browser.execute_script(f"window.gamecard.load_scorecard(JSON.parse('{json.dumps(scorecard_info)}'));")
        scorecard_object = self.browser.execute_script(f"return window.gamecard.to_object();")
        self.assertEqual(scorecard_object, scorecard_info)

    def test_to_object_partial_scorecard(self):
        self.browser.get(self.url)
        scorecard_info = self.score_info_partial_bonus
        self.browser.execute_script(f"window.gamecard.load_scorecard(JSON.parse('{json.dumps(scorecard_info)}'));")
        scorecard_object = self.browser.execute_script(f"return window.gamecard.to_object();")
        self.assertEqual(scorecard_object, scorecard_info)
    
    def test_to_object_empty_scorecard(self):
        self.browser.get(self.url)
        scorecard_info = self.score_info_empty
        self.browser.execute_script(f"window.gamecard.load_scorecard(JSON.parse('{json.dumps(scorecard_info)}'));")
        scorecard_object = self.browser.execute_script(f"return window.gamecard.to_object();")
        self.assertEqual(scorecard_object, scorecard_info)
   
    def test_to_object_extra_scores(self):
        self.browser.get(self.url)
        scorecard_info = self.score_info_partial_bonus
        self.browser.execute_script(f"window.gamecard.load_scorecard(JSON.parse('{json.dumps(scorecard_info)}'));")
        category = self.browser.find_element(By.ID, f"three_of_a_kind_input")

        #Fill in empty categories but don't hit ENTER
        category.send_keys("30") #not entered, just contains text 
        category = self.browser.find_element(By.ID, f"full_house_input")
        category.send_keys("25") #not entered, just contains text

        scorecard_object = self.browser.execute_script(f"return window.gamecard.to_object();")
        self.assertEqual(scorecard_object, scorecard_info)
    
    def test_is_finished_full_scorecard(self):
        self.browser.get(self.url)
        scorecard_info = self.score_info_finished
        self.browser.execute_script(f"window.gamecard.load_scorecard(JSON.parse('{json.dumps(scorecard_info)}'));")
        is_finished = self.browser.execute_script(f"return window.gamecard.is_finished();")
        self.assertTrue(is_finished)    
    
    def test_is_finished_partial_scorecard(self):
        self.browser.get(self.url)
        scorecard_info = self.score_info_partial
        self.browser.execute_script(f"window.gamecard.load_scorecard(JSON.parse('{json.dumps(scorecard_info)}'));")
        is_finished = self.browser.execute_script(f"return window.gamecard.is_finished();")
        self.assertFalse(is_finished)
    
    def test_get_score_full_scorecard(self):
        self.browser.get(self.url)
        scorecard_info = self.score_info_finished
        self.browser.execute_script(f"window.gamecard.load_scorecard(JSON.parse('{json.dumps(scorecard_info)}'));")
        score = self.browser.execute_script(f"return window.gamecard.get_score();")
        self.assertEqual(score, 288)
    
    def test_get_score_full_scorecard_no_bonus(self):
        self.browser.get(self.url)
        scorecard_info = self.score_info_finished_no_bonus
        self.browser.execute_script(f"window.gamecard.load_scorecard(JSON.parse('{json.dumps(scorecard_info)}'));")
        score = self.browser.execute_script(f"return window.gamecard.get_score();")
        self.assertEqual(score, 204)

    def test_get_score_partial_scorecard(self):
        self.browser.get(self.url)
        scorecard_info = self.score_info_partial_bonus
        self.browser.execute_script(f"window.gamecard.load_scorecard(JSON.parse('{json.dumps(scorecard_info)}'));")
        score = self.browser.execute_script(f"return window.gamecard.get_score();")
        self.assertEqual(score, 193)
    
    def test_get_score_partial_scorecard_no_bonus(self):
        self.browser.get(self.url)
        scorecard_info = self.score_info_partial
        self.browser.execute_script(f"window.gamecard.load_scorecard(JSON.parse('{json.dumps(scorecard_info)}'));")
        score = self.browser.execute_script(f"return window.gamecard.get_score();")
        self.assertEqual(score, 110)
    
    def test_get_score_empty_scorecard(self):
        self.browser.get(self.url)
        scorecard_info = self.score_info_empty
        self.browser.execute_script(f"window.gamecard.load_scorecard(JSON.parse('{json.dumps(scorecard_info)}'));")
        score = self.browser.execute_script(f"return window.gamecard.get_score();")
        self.assertEqual(score, 0)
    
    def test_update_scores_full_scorecard(self):
        self.browser.get(self.url)
        scorecard_info = self.score_info_finished
        self.browser.execute_script(f"window.gamecard.load_scorecard(JSON.parse('{json.dumps(scorecard_info)}'));")
        self.browser.execute_script(f"window.gamecard.update_scores();")
        score_values = get_current_score_values(self.browser, self.score_elements)
        self.assertEqual(score_values["upper_score"], 84)
        self.assertEqual(score_values["upper_bonus"], 35)
        self.assertEqual(score_values["upper_total"], 119)
        self.assertEqual(score_values["upper_total_lower"], 119)
        self.assertEqual(score_values["lower_score"], 169)
        self.assertEqual(score_values["grand_total"], 288)
    
    def test_update_scores_full_scorecard_no_bonus(self):
        self.browser.get(self.url)
        scorecard_info = self.score_info_finished_no_bonus
        self.browser.execute_script(f"window.gamecard.load_scorecard(JSON.parse('{json.dumps(scorecard_info)}'));")
        self.browser.execute_script(f"window.gamecard.update_scores();")
        score_values = get_current_score_values(self.browser, self.score_elements)
        self.assertEqual(score_values["upper_score"], 60)
        self.assertEqual(score_values["upper_bonus"], None)
        self.assertEqual(score_values["upper_total"], 60)
        self.assertEqual(score_values["upper_total_lower"], 60)
        self.assertEqual(score_values["lower_score"], 144)
        self.assertEqual(score_values["grand_total"], 204)

    def test_update_scores_partial_scorecard(self):
        self.browser.get(self.url)
        scorecard_info = self.score_info_partial_bonus
        self.browser.execute_script(f"window.gamecard.load_scorecard(JSON.parse('{json.dumps(scorecard_info)}'));")
        self.browser.execute_script(f"window.gamecard.update_scores();")
        score_values = get_current_score_values(self.browser, self.score_elements)
        self.assertEqual(score_values["upper_score"], 84)
        self.assertEqual(score_values["upper_bonus"], 35)
        self.assertEqual(score_values["upper_total"], 119)
        self.assertEqual(score_values["upper_total_lower"], 119)
        self.assertEqual(score_values["lower_score"], 74)
        self.assertEqual(score_values["grand_total"], 193)
    
    def test_update_scores_partial_scorecard_no_bonus(self):
        self.browser.get(self.url)
        scorecard_info = self.score_info_partial
        self.browser.execute_script(f"window.gamecard.load_scorecard(JSON.parse('{json.dumps(scorecard_info)}'));")
        self.browser.execute_script(f"window.gamecard.update_scores();")
        score_values = get_current_score_values(self.browser, self.score_elements)
        self.assertEqual(score_values["upper_score"], 36)
        self.assertEqual(score_values["upper_bonus"], None)
        self.assertEqual(score_values["upper_total"], 36)
        self.assertEqual(score_values["upper_total_lower"], 36)
        self.assertEqual(score_values["lower_score"], 74)
        self.assertEqual(score_values["grand_total"], 110)
    
    def test_update_scores_empty_scorecard(self):
        self.browser.get(self.url)
        scorecard_info = self.score_info_empty
        self.browser.execute_script(f"window.gamecard.load_scorecard(JSON.parse('{json.dumps(scorecard_info)}'));")
        self.browser.execute_script(f"window.gamecard.update_scores();")
        score_values = get_current_score_values(self.browser, self.score_elements)
        self.assertEqual(score_values["upper_score"], 0)
        self.assertEqual(score_values["upper_bonus"], None)
        self.assertEqual(score_values["upper_total"], 0)
        self.assertEqual(score_values["upper_total_lower"], 0)
        self.assertEqual(score_values["lower_score"], 0)
        self.assertEqual(score_values["grand_total"], 0)
    
if __name__ == '__main__':
    unittest.main()