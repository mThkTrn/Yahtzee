import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains 
from selenium.webdriver.support.ui import WebDriverWait
import random



class Dice_Helper_Function_Tests(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        #Runs once, before any tests are run
        self.url='http://127.0.0.1:8080/game?username=super_mario&password=123@456!'
        self.image_names = ["blank.svg", "one.svg", "two.svg", "three.svg", "four.svg", "five.svg", "six.svg"]
        self.trials = 20

    def setUp(self):
        self.browser = webdriver.Chrome()
        self.addCleanup(self.browser.quit)
    
    def test_set(self):
        new_values = [[5, 4, 3, 2, 2], [0,0,0,0,0], [6, -1, 1, -1, 6], [-1, -1, -1, -1, -1]]
        new_rolls_remaining = ["3", "2", "1", "0"]

        for blank_dice in [True, False]: #once for blank dice, once for non-blank dice
            for i in range(4):
                self.browser.get(self.url)

                if not blank_dice: #roll for non-blank dice tests
                    try:
                        roll_button = self.browser.find_element(By.ID, "roll_button")
                    except:
                        self.fail("roll_button element does not exist!")
                    roll_button.click()

                original_order=[]
                for d in range(5):
                    die_element = self.browser.find_element(By.ID, f"die_{d}")
                    original_order.append(die_element.get_attribute("src").split("/")[-1])
            
                self.browser.execute_script(f"window.dice.set({new_values[i]}, {new_rolls_remaining[i]});")
                rolls_remaining = self.browser.find_element(By.ID, "rolls_remaining").text
                self.assertEqual(rolls_remaining, new_rolls_remaining[i])

                #check dice values
                for d in range(5):
                    die_element = self.browser.find_element(By.ID, f"die_{d}")
                    die_element_image_name = die_element.get_attribute("src").split("/")[-1]
                    if new_values[i][d] > -1: 
                        self.assertTrue(die_element_image_name == self.image_names[ new_values[i][d] ])
                    else:
                        self.assertTrue(die_element_image_name == original_order[d]) 

        print("set() behavior passed")   

    def test_get_rolls_remaining(self):
            self.browser.get(self.url)
            actual_rolls_remaining = self.browser.execute_script(f"return window.dice.get_rolls_remaining();");
            self.assertEqual(actual_rolls_remaining, 3)
            self.assertEqual(type(actual_rolls_remaining), int)

            try:
                rolls_remaining_element = self.browser.find_element(By.ID, "rolls_remaining")
            except:
                self.fail("rolls_remaining element does not exist!")
            
            for value in ["2", "0", "1", "3"]:
                self.browser.execute_script(f"document.getElementById('rolls_remaining').innerHTML = '{value}';")
                actual_rolls_remaining = self.browser.execute_script(f"return window.dice.get_rolls_remaining();");
                self.browser.save_screenshot('rolls_remaining.png')
                self.assertEqual(actual_rolls_remaining, int(value)) #check that the value is updated
                self.assertEqual(type(actual_rolls_remaining), int) #check that the type is correct
           
            print("get_rolls_remaining() behavior passed")
    
    def test_get_values(self):
        self.browser.get(self.url) #blank dice check
        actual_values= self.browser.execute_script(f"return window.dice.get_values();");
        self.assertEqual(type(actual_values), list)
        self.assertEqual(actual_values, [0, 0, 0, 0, 0])
        self.assertEqual(len(actual_values), 5)
        for i in range(5):
            self.assertEqual(type(actual_values[i]), int)

        for _ in range(self.trials):
            self.browser.get(self.url) #new window

            new_values = []
            for i in range(5):
                new_values.append(random.choice([1,2,3,4,5,6])) #random dice values
            
            self.browser.execute_script(f"window.dice.set({new_values}, {random.choice([2,1,0])});");
            
            actual_values= self.browser.execute_script(f"return window.dice.get_values();");
            self.assertEqual(type(actual_values), list)
            self.assertEqual(len(actual_values), 5)
            for i in range(5):
                value = actual_values[i]
                self.assertEqual(type(value), int)
                die_element = self.browser.find_element(By.ID, f"die_{i}")
                die_element_image_name = die_element.get_attribute("src").split("/")[-1]
                UI_value = self.image_names.index(die_element_image_name)
                self.assertEqual(value, UI_value)

        print("get_values() behavior passed")

    def test_get_sum(self):
        self.browser.get(self.url) #blank dice check
        actual_sum = self.browser.execute_script(f"return window.dice.get_sum();");
        self.assertEqual(type(actual_sum), int)
        self.assertEqual(actual_sum, 0)

        for _ in range(self.trials):
            self.browser.get(self.url) #new window

            new_values = []
            for i in range(5):
                new_values.append(random.choice([1,2,3,4,5,6])) #random dice values
            
            self.browser.execute_script(f"window.dice.set({new_values}, {random.choice([2,1,0])});");

            for i in range(5): #randomly reserve some collection of dice
                die_element = self.browser.find_element(By.ID, f"die_{i}")
                should_reserve = random.choice([True, False])
                if should_reserve:
                    ActionChains(self.browser).double_click(die_element).perform()
                    #reserving shouldn't affect sum
       
            actual_sum = self.browser.execute_script(f"return window.dice.get_sum();");
            self.assertEqual(type(actual_sum), int)
            self.assertEqual(actual_sum, sum(new_values))
     
        print("get_sum_behavior passed")
    
    def test_get_counts(self):
        self.browser.get(self.url)
        actual_counts = self.browser.execute_script(f"return window.dice.get_counts();");
        self.assertEqual(actual_counts, [0, 0, 0, 0, 0, 0])
        self.assertEqual(type(actual_counts), list)
        self.assertEqual(len(actual_counts), 6)
        for i in range(5):
            self.assertEqual(type(actual_counts[i]), int)
        
        test_cases = [
            ([1, 2, 3, 4, 5], [1, 1, 1, 1, 1, 0]),
            ([6, 2, 3, 3, 6], [0, 1, 2, 0, 0, 2]),
            ([0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]),
            ([1, 1, 1, 1, 1], [5, 0, 0, 0, 0, 0]),
            ([6, 6, 6, 6, 6], [0, 0, 0, 0, 0, 5]),
            ([ 2, 3, 4, 5, 6], [0, 1, 1, 1, 1, 1]),
            ([6, 5, 4, 2, 1], [1, 1, 0, 1, 1, 1]),
            ([3, 2, 2, 3, 3], [0, 2, 3, 0, 0, 0])
        ]

        for values, expected_counts in test_cases:
            self.browser.get(self.url) #resets reserved dice
            self.browser.execute_script(f"window.dice.set({values}, {random.choice([2,1,0])});");

            for i in range(5): #randomly reserve some collection of dice
                die_element = self.browser.find_element(By.ID, f"die_{i}")
                should_reserve = random.choice([True, False])
                if should_reserve:
                    ActionChains(self.browser).double_click(die_element).perform()
                    #reserving shouldn't affect counts
            
            actual_counts = self.browser.execute_script(f"return window.dice.get_counts();");
            self.assertEqual(actual_counts, expected_counts)
        
        print("get_counts() behavior passed")
    
    def test_roll(self): 
       dice_counts={name:0 for name in self.image_names}      

       for _ in range(self.trials): #random dice values
            self.browser.get(self.url) 
    
            for i in range(3):
                self.browser.execute_script(f"window.dice.roll();");
            
                for i in range(5):
                    die_element = self.browser.find_element(By.ID, f"die_{i}")
                    die_element_image_name = die_element.get_attribute("src").split("/")[-1]
                    dice_counts[die_element_image_name]+=1
        
       self.assertTrue(dice_counts["blank.svg"] == 0) #no blank dice should be rolled
       for i in range(1,7): #loose bounds on counts
            self.assertTrue(dice_counts[self.image_names[i]] > 0.08*self.trials*3*5)#EV: ~0.17
            self.assertTrue(dice_counts[self.image_names[i]] <= self.trials*3*5)

       for _ in range(self.trials): #rolling with reserved dice       
            new_values=[]          
            for i in range(5):
                new_values.append(random.choice([1,2,3,4,5,6])) #random dice values
            self.browser.execute_script(f"window.dice.set({new_values}, {random.choice([2,1])});");

            original_order=[]
            for i in range(5):
                die_element = self.browser.find_element(By.ID, f"die_{i}")
                
                should_reserve = random.choice([True, False])
                if should_reserve:
                    ActionChains(self.browser).double_click(die_element).perform()
                original_order.append((die_element.get_attribute("src").split("/")[-1], should_reserve))
           
            self.browser.execute_script(f"window.dice.roll();");
            
            for i in range(5):#reserved dice should match original image names and still be reserved
                die_element = self.browser.find_element(By.ID, f"die_{i}")
                die_element_image_name = die_element.get_attribute("src").split("/")[-1]
                if original_order[i][1]:
                    self.assertTrue(die_element_image_name == original_order[i][0]) 
                    self.assertTrue("reserved" in die_element.get_attribute("class"))
                else:
                    self.assertFalse("reserved" in die_element.get_attribute("class"))
    
       print("get_roll() behavior passed")

    def test_reset(self):   
        test_cases = [
            ([1, 2, 3, 4, 5], [1, 1, 1, 1, 1, 0]),
            ([6, 2, 3, 3, 6], [0, 1, 2, 0, 0, 2]),
            ([0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]),
            ([1, 1, 1, 1, 1], [5, 0, 0, 0, 0, 0]),
            ([6, 6, 6, 6, 6], [0, 0, 0, 0, 0, 5]),
            ([ 2, 3, 4, 5, 6], [0, 1, 1, 1, 1, 1]),
            ([6, 5, 4, 2, 1], [1, 1, 0, 1, 1, 1]),
            ([3, 2, 2, 3, 3], [0, 2, 3, 0, 0, 0])
        ]

        for values, expected_counts in test_cases:
            self.browser.get(self.url)
            self.browser.execute_script(f"window.dice.set({values}, {random.choice([2,1,0])});");

            for i in range(5): #randomly reserve some collection of dice
                die_element = self.browser.find_element(By.ID, f"die_{i}")
                should_reserve = random.choice([True, False])
                if should_reserve:
                    ActionChains(self.browser).double_click(die_element).perform()
            
            self.browser.execute_script(f"window.dice.reset();");
            
            self.assertEqual(self.browser.execute_script(f"return window.dice.get_rolls_remaining();"), 3)
            for i in range(5):
                die_element = self.browser.find_element(By.ID, f"die_{i}")
                die_element_image_name = die_element.get_attribute("src").split("/")[-1]
                self.assertTrue(die_element_image_name == self.image_names[0]) #all blank
                self.assertFalse("reserved" in die_element.get_attribute("class")) #all unreserved
                    
        print("reset() behavior passed")    
    
    def test_reserve(self):
        self.browser.get(self.url)
        
        #shouldn't reserve blank dice
        for i in range(5):#reserved dice should match original image names and still be reserved
            die_element = self.browser.find_element(By.ID, f"die_{i}")
            self.browser.execute_script(f"window.dice.reserve(die_{i});")
            self.assertFalse("reserved" in die_element.get_attribute("class"))
            self.browser.execute_script(f"window.dice.reserve(die_{i});")
            self.assertFalse("reserved" in die_element.get_attribute("class"))
        
        self.browser.execute_script(f"window.dice.roll();");

        #should reserve/unreserve non-blank dice
        for i in range(5):
            die_element = self.browser.find_element(By.ID, f"die_{i}")
            self.browser.execute_script(f"window.dice.reserve(die_{i});")#dbl click to make reserved
            self.assertTrue("reserved" in die_element.get_attribute("class"))
            self.browser.execute_script(f"window.dice.reserve(die_{i});")#dbl click to unreserve    
            self.assertFalse("reserved" in die_element.get_attribute("class"))
            self.browser.execute_script(f"window.dice.reserve(die_{i});")#dbl click to make reserved again
            self.assertTrue("reserved" in die_element.get_attribute("class"))

        print("reserve() behavior passed")  

if __name__ == '__main__':
    unittest.main()