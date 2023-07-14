import unittest, os, shutil, time
from app import app
from app.data.database import DatabaseInteract
from selenium import webdriver

# Import necessary libraries
import openai
import sqlite3



class UserTest(unittest.TestCase):
    driver = None


    def setUp(self):
        # Make a copy of the database template for testing
        shutil.copy("test/database_template.db","test/test.db")
        self.database = sqlite3.connect("test/test.db", check_same_thread = False) 
        # Create database interact object
        self.db = DatabaseInteract(self.database)
        self.driver = webdriver.Firefox(executable_path="test/geckodriver")

        # Open home page
        self.driver.maximize_window()
        self.driver.get('http://localhost:5000/')



    def tearDown(self):
        # Remove database
        self.database.close()
        os.remove("test/test.db")

        # Reset database changes - Couldn't get test database working with selenium tests
        # -Have to reset the database manually for the test to pass
        # db = sqlite3.connect("app/data/database.db", check_same_thread = False)
        # db.execute("DELETE FROM users WHERE username = testuser AND email = johnsmith@travelmail.com")
        # db.commit()
        # db.close()

        # Close driver
        if self.driver:
            self.driver.close()


    def test_register_login(self):

        # Register an account
        self.driver.get('localhost:5000/register')
        self.driver.implicitly_wait(5)
        fname = self.driver.find_element('id','first-name')
        fname.send_keys('John')
        lname = self.driver.find_element('id','last-name')
        lname.send_keys('Smith')
        username = self.driver.find_element('id','username')
        username.send_keys('testuser')
        email = self.driver.find_element('id','email')
        email.send_keys('johnsmith@travelmail.com')
        password = self.driver.find_element('id','password')
        password.send_keys('testpassword')
        submit = self.driver.find_element('id','register-button')
        time.sleep(1)
        self.driver.implicitly_wait(5)
        submit.click()

        # Redirected to login page
        self.driver.implicitly_wait(5)
        username = self.driver.find_element('id','username-email')
        username.send_keys('testuser')
        password = self.driver.find_element('id','password')
        password.send_keys('testpassword')
        submit = self.driver.find_element('id','login-button')
        time.sleep(1)
        self.driver.implicitly_wait(5)
        submit.click()

        # Logged in
        self.driver.implicitly_wait(5)
        chatbtn = self.driver.find_element('css selector', '.login-btn')
        self.assertEqual(chatbtn.get_attribute('innerHTML'),'CHAT') # Chat button only exists when logged in

