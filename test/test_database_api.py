import unittest, os, shutil
from app import app
from app.data.database import DatabaseInteract

# Import necessary libraries
import openai
import sqlite3


class DatabaseAPITest(unittest.TestCase):
    
    def setUp(self):
        # Make a copy of the database template for testing
        shutil.copy("test/database_template.db","test/test.db")
        self.database = sqlite3.connect("test/test.db", check_same_thread = False) 
        # Create database interact object
        self.db = DatabaseInteract(self.database)


    def tearDown(self):
        # Remove database
        self.database.close()
        os.remove("test/test.db")


    def test_getuser(self):
        # Test getuser
        username = "tartaglia10"
        assert self.db.getuser(username) == ('tartaglia10', 'tartaglia@592668973', 'Fatui Tartaglia', 'tartaglia592668973@travelmail.com')

        username = "fakeuser"
        assert self.db.getuser(username) == False

    def test_user_avail(self):
        # Test username availability
        username = "tartaglia10"
        assert self.db.user(username) == False

        username = "fakeuser"
        assert self.db.user(username) == True    

    def test_email_avail(self):
        # Test email availability
        username = "tartaglia592668973@travelmail.com"
        assert self.db.email(username) == False

        username = "fakeuser@travelmail.com"
        assert self.db.email(username) == True    


    def test_validate(self):
        # Validate email and password
        email_id = "sagepierro493044909@travelmail.com"
        password = "sagepierro@493044909"
        assert self.db.validate(email_id, password) == (False,"pierro11")

        password = "incorrect"
        assert self.db.validate(email_id, password) == (False, "pierro11")

        # Validate username and password
        username = "pierro11"
        password = "sagepierro@493044909"
        assert self.db.validate(username, password) == (False,"pierro11")

        password = "incorrect"
        assert self.db.validate(username, password) == (False, "pierro11")

    def test_create_user(self):
        # Enter a new user into the database
        username = "tester"
        password = "tester@12345678"
        name = "Legendary Tester"
        email_id = "legendarytester1234@travelmail.com"
        assert self.db.create_user(username, password, name, email_id) == True

        # Check that user doesn't exist
        assert self.db.user("tester") == False
        
        # Check that registration doesn't work for the same username or email
        username = "tester"
        password = "tester@12345678"
        name = "Legendary Tester2"
        email_id = "newemail@travelmail.com"
        assert self.db.create_user(username, password, name, email_id) == False

        username = "tester_new"
        password = "tester@12345678"
        name = "Legendary Tester3"
        email_id = "legendarytester1234@travelmail.com"
        assert self.db.create_user(username, password, name, email_id) == False


    def test_countries(self):
        # Test no parameters
        country_list = self.db.countries()
        assert "Australia" in country_list
        assert "Hungary" in country_list
        assert "Cameroon" in country_list
        assert "South Korea" in country_list
        assert "Zimbabwe" in country_list
        
        # Test with country parameter
        places_list = self.db.countries("Australia")
        assert "Sydney" in places_list
        assert "Gold Coast" in places_list
        assert "Perth" in places_list
        assert "Shepparton" in places_list
        assert "Newcastle" in places_list
        

    def test_interaction(self):
        
        # Test when user interaction is to be stored
        username_put = "tartaglia10"
        date = "21/05/2023"
        choice = "Rome"
        interaction_type1 = "put"
        check = self.db.interaction(username_put, date, choice, interaction_type1)
        assert check == True

        # Test when user interaction is to be retrieved
        username_get = "tartaglia10"
        interaction_type2 = "get"
        result = self.db.interaction(username=username_get, interaction_type=interaction_type2)
        assert result == [("Rome","21/05/2023")]


    def test_chatgpt(self):
        question = "What is a good travel location?"

        reply = self.db.chatgpt(question)

        # ChatGPT reply varies, so just make sure it sends something
        assert len(reply) > 0


    def test_clear_history(self):
        username = "tartaglia10"
        date = "21/05/2023"
        choice = "test1"
        interaction_type = "put"

        # Add interactions to the table
        self.db.interaction(username, date, choice, interaction_type)
        choice = "test2"
        self.db.interaction(username, date, choice, interaction_type)
        choice = "test3"
        self.db.interaction(username, date, choice, interaction_type)

        # Ensure clear history was successful
        assert self.db.clear_history(username) == True

        # Check if there are any previous interactions
        interaction_type = "get"
        assert self.db.interaction(username, interaction_type) == []
