import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains 

import random

class Dice_UI_Tests(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        #Runs once, before any tests are run
        self.url='http://127.0.0.1:8080/game?username=super_mario&password=123@456!'
        self.image_names = ["blank.svg", "one.svg", "two.svg", "three.svg", "four.svg", "five.svg", "six.svg"]
    
    def setUp(self):
        self.browser = webdriver.Chrome()
        self.addCleanup(self.browser.quit)

    def test_blank_die_elements_on_page_load(self): 
        self.browser.get(self.url)
        for i in range(5):
            try:
                die_element = self.browser.find_element(By.ID, f"die_{i}")
            except:
                self.fail(f"die_{i} element does not exist!")
            die_element_image_name = die_element.get_attribute("src").split("/")[-1]
            self.assertTrue(self.image_names.index(die_element_image_name)==0) #0: blank.svg         
            
        print("blank_die_elements_on_page_load passed")

    def test_roll_button_UI_basics(self):
        self.browser.get(self.url)
        try:
            roll_button = self.browser.find_element(By.ID, "roll_button")
        except:
            self.fail("roll_button element does not exist!")
        self.assertEqual(roll_button.text, "Roll the Dice!")
        roll_button.click()
        self.browser.save_screenshot('roll_button_UI_basics.png') #for debugging purposes

        for roll in range(2): #roll 2 more times
            for i in range(5):
                die_element = self.browser.find_element(By.ID, f"die_{i}")
                die_element_image_name = die_element.get_attribute("src").split("/")[-1]
                #die_element_image_name is an allowed image name
                self.assertTrue(self.image_names.index(die_element_image_name)>0) #0: blank.svg
  
        print("test_roll_button_UI_basics passed")


    def test_reserving_unreserving_dice(self):
        self.browser.get(self.url)
  
        for i in range(5):
            die_element = self.browser.find_element(By.ID, f"die_{i}")
            die_element_image_name = die_element.get_attribute("src").split("/")[-1]
            self.assertTrue(self.image_names.index(die_element_image_name)==0) #0: blank.svg
            self.assertFalse("reserved" in die_element.get_attribute("class")) #not reserved on page load
            #can't reserve blank dice
            ActionChains(self.browser).double_click(die_element).perform()
            self.assertFalse("reserved" in die_element.get_attribute("class"))

        try:
            roll_button = self.browser.find_element(By.ID, "roll_button")
        except:
            self.fail("roll_button element does not exist!")
        roll_button.click() 

        for i in range(5): 
            die_element = self.browser.find_element(By.ID, f"die_{i}")
            self.assertFalse("reserved" in die_element.get_attribute("class"))
            die_element_image_name = die_element.get_attribute("src").split("/")[-1]
            self.assertTrue(self.image_names.index(die_element_image_name)>0) #0: blank.svg

            for _ in range(2):#repeat reserve/unreserve cycle twice
                #non-blank dice can be reserved
                ActionChains(self.browser).double_click(die_element).perform()
                self.assertTrue("reserved" in die_element.get_attribute("class"))

                #can unreserve non-blank dice
                ActionChains(self.browser).double_click(die_element).perform()
                self.assertFalse("reserved" in die_element.get_attribute("class"))

        print("test_reserving_unreserving_dice passed")


    def test_roll_button_reserved_die(self):
        
        for _ in range(25): #run 25 times re: random selection of dice to reserve
            self.browser.get(self.url) #ensures dice are no longer reserved from previous tests
            try:
                roll_button = self.browser.find_element(By.ID, "roll_button")
            except:
                self.fail("roll_button element does not exist!")
            
            roll_button.click()
            
            order=[]
            for i in range(5):
                die_element = self.browser.find_element(By.ID, f"die_{i}")
                
                should_reserve = random.choice([True, False])
                if should_reserve:
                    ActionChains(self.browser).double_click(die_element).perform()
                
                self.browser.save_screenshot('roll_button_reserved_die.png') #for debugging purposes
                 
                order.append((die_element.get_attribute("src").split("/")[-1], should_reserve))
           
                if order[i][1]:
                    self.assertTrue("reserved" in die_element.get_attribute("class"))
                else:
                    self.assertFalse("reserved" in die_element.get_attribute("class"))
           
            roll_button.click()

            for i in range(5):#reserved dice should match original image names and still be reserved
                die_element = self.browser.find_element(By.ID, f"die_{i}")
                die_element_image_name = die_element.get_attribute("src").split("/")[-1]
                if order[i][1]:
                    self.assertTrue(die_element_image_name == order[i][0]) 
                    self.assertTrue("reserved" in die_element.get_attribute("class"))
                else:
                    self.assertFalse("reserved" in die_element.get_attribute("class"))
    
        print("test_roll_button_reserved_die passed")

    def test_rolls_remaining_UI(self):
        self.browser.get(self.url)
        try:
            rolls_remaining_element = self.browser.find_element(By.ID, "rolls_remaining")
        except:
            self.fail("rolls_remaining element does not exist!")
        self.assertEqual(rolls_remaining_element.text, "3")

        print("test_rolls_remaining_UI passed")

if __name__ == '__main__':
    unittest.main()