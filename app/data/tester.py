import database

object = database.DatabaseInteract()

#----------------------------test username availability---------------------------------
username = "tartaglia10"
available = object.user(username)
print(available)

#----------------------------validate email_id and password-----------------------------
email_id = "sagepierro493044909@travelmail.com"
password = "sagepierro@493044909"
validation = object.validate(email_id, password)
print(validation)

#----------------------------validate username and password-----------------------------
username1 = "pierro11"
password1 = "sagepierro@493044909"
validation = object.validate(username1, password1)
print(validation)

#----------------------------enter a new user into the database-------------------------

username2 = "tester"
password2 = "tester@12345678"
name = "Legendary Tester"
email_id = "legendarytester1234@travelmail.com"
response = object.create_user(username2, password2, name, email_id)
print(response)

#----------------------------test countries function------------------------------------
# Test when no country is passed
result1 = object.countries()
print(result1)
# Test when a country is passed
result2 = object.countries("Australia")
print(result2)

#----------------------------test interaction function-----------------------------------

# Test when user interaction is to be stored
username_put = "tartaglia10"
date = "21/05/2023"
choice = "Rome"
interaction_type1 = "put"
result3 = object.interaction(username_put, date, choice, interaction_type1)
print(result3)

# Test when user interaction is to be retrieved
username_get = "tartaglia10"
interaction_type2 = "get"
result4 = object.interaction(username_get, interaction_type2)
print(result4)
