# Import necessary libraries
import openai
import sqlite3
from app.data.encryption import encode
from app.data.encryption import decode

# Initialisation -0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-

def_db = sqlite3.connect("app/data/database.db", check_same_thread = False) # Had to add check_same_thread paramter or database didn't work for me
openai.api_key = "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"
chat = openai.ChatCompletion()

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------
# Creating a class to interact with our database

class DatabaseInteract:
    database = def_db # Set database to default

    # Pass in database as optional parameter (for test database)
    def __init__(self, db=None):
        if db:
            self.database = db

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------   
    # Get user information
    def getuser(self, username):
        if self.user(username): # User not in database
            return False
        else:
            # Fetch user data
            return self.database.execute("SELECT * FROM users WHERE username = :username", { 'username': username}).fetchall()[0]
    
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------   
    # Check if the username is available
    def user(self, username):
        check = self.database.execute("SELECT COUNT(*) FROM users WHERE username = :username", { 'username': username}).fetchall()[0][0]
        if check > 0:
            return False
        else:
            return True
    
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------    
    # Check if the email is available
    def email(self, email):
        check = self.database.execute("SELECT COUNT(*) FROM users WHERE email_id = :email", { 'email': email}).fetchall()[0][0]
        if check > 0:
            return False
        else:
            return True
    
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------
    # Validate password against username
    def validate(self, user, password):
        passkey = self.database.execute("SELECT password FROM users WHERE username = :username OR email_id = :email_id", { 'username': user, 'email_id': user }).fetchall()[0][0]
        decrypted = decode(passkey)
        # Do note that username is aldo return to track logged-in session
        username = self.database.execute("SELECT username FROM users WHERE username = :username OR email_id = :email_id", { 'username': user, 'email_id': user }).fetchall()[0][0]
        if decrypted == password:
            return True, username
        else:
            return False, username
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------   
    # Create a new user
    def create_user(self, username, password, name, email_id):
        encrypted = encode(password)
        flag = self.user(username)
        if flag == False:
            return False
        else:
            try:
                create = self.database.execute("INSERT INTO users (username, password, name, email_id) VALUES (:username, :password, :name, :email_id)", { 'username': username, 'password': encrypted, 'name': name, 'email_id': email_id})
                self.database.commit()
                return True
            except sqlite3.IntegrityError or sqlite3.ProgrammingError:
                return False
            else:
                return False
            
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------   
# Handle other required data      
    # Data Handling Functions ->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    def countries(self, country=None):
        if country is None:
            try:
                countries = []
                response = self.database.execute("SELECT country_name FROM country_name").fetchall()
                for item in response:
                    countries.append(item[0])
                return countries
            except sqlite3.DatabaseError or sqlite3.ProgrammingError:
                return False
            else:
                return False
        else:
            places = self.places(country)
            return places
        

    def places(self, country):
        try:
            places = []
            response = self.database.execute("SELECT place_name FROM places WHERE country_name = :country", { 'country': country}).fetchall()
            for item in response:
                places.append(item[0])
            return places
        except sqlite3.DatabaseError or sqlite3.ProgrammingError:
            return False
        else:
            return False
    
    def info(self, choice):
        try:
            response = self.database.execute("SELECT COUNT(*) FROM country_name WHERE country_name = :choice", {'choice': choice})
            if len(response) > 0:
                question = "Give me a detailed description of "+choice+", highlighting places I can visit as a tourist. Also, do not add any unnecessary messages and just type what is asked."
                answer, log = self.chatgpt(question)
                return answer
            else:
                try:
                    response = self.database.execute("SELECT country_name FROM places WHERE place_name = :choice", {'choice': choice}).fetchall()[0][0]
                    question = "Give me a detailed description of "+choice+", "+response+", and nearby places I can visit. Also, do not add any unnecessary messages and just type what is asked."
                    answer, log = self.chatgpt(question)
                    coordinates = self.coordinates(choice+", "+response)
                    return answer, coordinates
                except:
                    return False
        except:
            return False
    
    def coordinates(self, place):
        question = "Mention the co-ordinates of "+place+" in a tuple form. Also, do not add any unnecessary messages."
        answer, log = self.chatgpt(question)
        return answer
        
    # ChatGPT integration ->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    def chatgpt(self,question, chat_log=None):
        if chat_log is None:
            chat_log = [{
                'role': 'system',
                'content': 'Tell me that I ask',
            }]
        chat_log.append({'role': 'user', 'content': question})
        response = chat.create(model='gpt-3.5-turbo', messages=chat_log)
        answer = response.choices[0]['message']['content']
        chat_log.append({'role': 'assistant', 'content': answer})
        return answer, chat_log
        
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------   
    # Handle User Interaction
    def interaction(self, username, date=None, choice=None, interaction_type="get"):
        
        if interaction_type == "put" and date is not None and choice is not None:
            try:
                response = self.database.execute("INSERT INTO interaction (username, event_date, choice) VALUES (:username, :date, :choice)", { 'username': username, 'date': date, 'choice': choice})
                self.database.commit()
                return True
            except:
                return False
        elif interaction_type == "get":
            try:
                interaction = []
                response = self.database.execute("SELECT choice,event_date FROM interaction WHERE username = :username ORDER BY event_date", {'username' : username}).fetchall()
                for item in response:
                    interaction.append(item)
                return interaction
            except sqlite3.DatabaseError or sqlite3.ProgrammingError:
                return False 

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------   
    # Clear user chat history
    def clear_history(self, username):
        if not self.user(username):
            try:
                self.database.execute("DELETE FROM interaction WHERE username = :username", {'username' : username})
                self.database.commit()
                return True
            except sqlite3.DatabaseError or sqlite3.ProgrammingError:
                return False
        else:
            return False
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------   