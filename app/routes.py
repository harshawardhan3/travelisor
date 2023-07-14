from flask import Flask, render_template, redirect, request, jsonify
from flask_login import current_user, login_user, logout_user, login_required

from app import app

from pydantic import ValidationError

from app.data import database

from app.forms import UserModel

from app.models import load_user

# Initialise database API object
db = database.DatabaseInteract()


@app.route('/')
def home():
    print(f"Current user: {current_user.get_id()}") # Checking that authentication works
    return render_template('travelisor-home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    # Validate form for post request
    if request.method == 'POST':

        # Print form inputs for troubleshooting
        for k,v in request.form.items():
            print(f"{k}: {v}")

        # Ensure that user inputs are valid
        try:
            user = UserModel(
                name = request.form['first-name'] + ' ' + request.form['last-name'],
                username = request.form['username'],
                email = request.form['email'],
                password = request.form['password']
            )

        # Catch error if user input is invalid
        except ValidationError as e:
            print(e)
            return render_template('register-page.html')


        # Username taken
        if not db.user(user.username):
            print("Username taken.")

        # Email taken
        elif not db.email(user.email):
            print("Email already in use.")
        
        # Username and email available
        else:
            if db.create_user(user.username, user.password, user.name, user.email): # User creation successful
                print("Account created.")
                return redirect('login') 
            else: # Error creating user
                print("Could not create user")
            

    return render_template('register-page.html')

@app.route('/login', methods=['GET','POST'])
def login():

    # Validate form for post request
    if request.method == 'POST':

        # Print form inputs for troubleshooting
        for k,v in request.form.items():
            print(f"{k}: {v}")

        username_email = request.form['username-email']
        password = request.form['password']

        # If user exists (i.e., username/email not free)
        if not db.user(username_email) or not db.email(username_email):
            
            # Note: need to hash passwords

            check, username = db.validate(username_email, password)
            if check: 
                # Log in as user
                print(f"Logging in as {username}...")

                user_obj = load_user(username)

                login_user(user_obj) 

                # Redirect to chat view
                return redirect('/')  
        
            # Password did not match
            else: 
                print("Password was incorrect")


        else: # User does not exist
            print("No user exists with the specified credentials.")


    return render_template('login-page.html')

@app.route('/chat', methods=['GET','POST'])
@login_required
def chat():
    print(f"Chatting as {current_user.get_id()}") # Checking authentication

    if request.is_json:
        
        query = request.args.get('msg')
        q_timestamp = request.args.get('timestamp')
        print(f"User query: {query}")
        print(f"Timestamp: {q_timestamp}")

        ans = db.chatgpt(query)[0]

        # Add the query and reply to history (user timestamp for both during testing)
        print(db.interaction(current_user.get_id(), q_timestamp, query, "put"))
        print(db.interaction(current_user.get_id(), q_timestamp, ans, "put"))

        print(f"Ans: {ans}")

        return jsonify({'reply': ans})
    
    else:
        # Get chat history of current user on page reload
        history = db.interaction(current_user.get_id(), interaction_type="get")

        prev_msgs = []
        prev_timestamps = []
        for msg in history:
            prev_msgs.append(msg[0])
            prev_timestamps.append(msg[1])

        print(f"prev_msgs = {prev_msgs}")
        print(f"prev_timestamps = {prev_timestamps}")


    return render_template('chatview.html', uname=current_user.get_id(), prev_msgs=prev_msgs, prev_timestamps=prev_timestamps)

@app.route("/get_countries")
def get_countries():

    countries = db.countries()

    return jsonify({"countries": countries})

@app.route("/places")
def get_places():

    country = request.args.get("country")
    places = db.countries(country)

    return jsonify({"places": places})


@app.route('/logout')
@login_required
def logout():
    print("Logging out...")
    logout_user()

    return redirect('/')

# Add /clear to chat url to clear the chat history
@app.route('/chat/clear')
@login_required
def clear():
    db.clear_history(current_user.get_id())
    print(f"Chat messages cleared for {current_user.get_id()}")

    return redirect('/chat')
    