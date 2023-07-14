from app.data import database
from app import login
from flask_login import UserMixin

db = database.DatabaseInteract()

@login.user_loader
def load_user(username):
    # Get user information from database
    data = db.getuser(username)
    if data:
        # Return user object
        return User(data)
    
    else:
        return False

# Each User object represents a row of the user table for authentication
class User(UserMixin):

    # Constructor method takes the line and gets username
    def __init__(self, data):
        self.username = data[0]
        self.password = data[1]
        self.name = data[2]
        self.email = data[3]

    # Pretty sure we don't need this because of UserMixin inheritance
    # def is_authenticated(self):
    #     return db.validate(self.username, self.password)

    def get_id(self):
        return self.username