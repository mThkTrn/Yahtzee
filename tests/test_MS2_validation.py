import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains 

class MS2_Validation_Tests(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        #Runs once, before any tests are run
        self.url='http://127.0.0.1:8080/game?username=super_mario&password=123@456!'
        self.upper_categories= ["one", "two", "three", "four", "five", "six"]
        self.lower_categories= ["three_of_a_kind", "four_of_a_kind", "full_house", "small_straight", "large_straight", "yahtzee", "chance"]
        self.score_elements=["upper_score", "upper_bonus", "upper_total", "lower_score", "upper_total_lower", "grand_total"]
    
    def setUp(self):
        self.browser = webdriver.Chrome()
        self.addCleanup(self.browser.quit)
    
    def test_upper_categories_validation(self):
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
                if type(test[0]) is str:
                     result = self.browser.execute_script(f"return window.gamecard.is_valid_score('{category}', '{test[0]}');")
                else:
                     result = self.browser.execute_script(f"return window.gamecard.is_valid_score('{category}', {test[0]});")
                #self.browser.save_screenshot(f"{category}_input_after_enter.png")
                print(f"!!! (upper) category = {category}, test = {test} !!!")
                self.assertEqual(result, test[2])
    
    def test_lower_categories_validation(self):
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
                if type(test[0]) is str:
                     result = self.browser.execute_script(f"return window.gamecard.is_valid_score('{category}', '{test[0]}');")
                else:
                     result = self.browser.execute_script(f"return window.gamecard.is_valid_score('{category}', {test[0]});")
                #self.browser.save_screenshot(f"{category}_input_after_enter.png")
                print(f"!!! (lower) category = {category}, test = {test} !!!")
                self.assertEqual(result, test[2])

if __name__ == '__main__':
    unittest.main()