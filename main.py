from flask import Flask, render_template, request, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy

# Application Setup
app = Flask(__name__)
app.secret_key = "secret_key"

# Database Config
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFCATIONS"] = False
db = SQLAlchemy(app)

# Database Model

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(30), unique = True, nullable = False)
    password = db.Column(db.String(10), nullable = False)
    first_name = db.Column(db.String(15), nullable = False)
    last_name = db.Column(db.String(15), nullable = False)
    role = db.Column(db.String(10), nullable = False)

### ---------- Password Verification Functions ---------- ###

# Verify password matches database for login attempt
def verify_password_login(password, user):
    return password == user.password
      
# Verify password meets requirements for account creation
def verify_password_create(password, email):
    nshe = email[0:10]
    return password == nshe
        
### ---------- Routes ---------- ###

## ----- Get Page Routes ----- ##

# --- Index Page --- #
@app.route("/")
# When User visits the above url ("/" = website root)... 
# run the following function
def index():

    # Retreive "index.html" from templates folder and display the page
    return render_template("index.html")

# --- Create Account Page --- #
@app.route("/create_account")
def create_account():
    return render_template("create_account.html")

# --- Login Page --- #
@app.route("/login")
def login_page():
    return render_template("login.html")

# --- Dashboard Page --- #
@app.route("/dashboard")
def dashboard():

    # Check if a user is currently in session (logged in)
    if "email" in session:

        # Filter through DB until correct user is identified
        user = User.query.filter_by(email=session["email"]).first()

        # Display the user's unique dashboard
        # Pass the user's firstname and last name to "dashboard.html"
        if user:
            return render_template("dashboard.html",
                                     first_name = user.first_name,
                                     last_name  = user.last_name,)
# --- My Reservation Page --- #                                            
@app.route("/my_reservations")
def my_reservations():
    return render_template("my_reservations.html")
## ----- Authentication Routes ----- ##

# Register
@app.route("/register", methods=["POST"]) # Post: Recieve data from frontend
                                          # Example: a form submission

# When the user submits a post request at the above URL ("/register")...
# run the following function.
def register():                          
    
    # Store data from post request into local variables
    email = request.form["email"]
    password = request.form["nshe"]
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    role = request.form["role"]

    # Search the DB by email to see if it's in use. If a user exists with that
    # email, assign it to the local variable user
    user = User.query.filter_by(email=email).first()

    # Checks the truth value of the variable user.
    #   Returns true if it contains a valid row in the User table
    #   Returns false if the value is "none" - user not found
    if user:
        return render_template("create-account.html", 
                               error = "Email in use! - try again")
    
    # If password is invaid refresh page and return an error message
    elif not verify_password_create(password, email):
        return render_template("create-account.html", 
                error = "Password must match #nshe used in email - try again")
    
    # User doesn't already exist and password is valid... add user to DB
    else:
        # Create a new row in the User table ("mock row" not submitted yet)
        new_user = User()

        # Fill row with the new user's data
        new_user.email = email
        new_user.password = password
        new_user.first_name = first_name
        new_user.last_name = last_name
        new_user.role = role

        # Stage the row (ready to commit)
        db.session.add(new_user)

        # Commit the row (officially submitted to the DB)
        db.session.commit()

        # save the current user's email under the session key: "email"
        session["email"] = email

        # Redirects the user to their unique dashboard after account creation.
        # Go to the URL which maps to the dashboard function and run it.
        return redirect(url_for("dashboard"))

# Login
@app.route("/login", methods=["POST"])
def login():

    # Collect info from form
    email = request.form["email"]
    password = request.form["password"]
    
    # Look up corresponding user in DB using the email recieved from the form.
    user = User.query.filter_by(email=email).first()

    # Check if the user exists and that the password is correct.
    if user and verify_password_login(password, user):

        # login attempt is valid - add the user by email to the session.
        session["email"] = email

        # Send user to their unique dashboard.
        return redirect(url_for("dashboard"))
    else:
        # login attempt was invalid... refresh page and display error message.
        return render_template("login.html", error = "Invalid login! - try again")

# Logout
@app.route("/logout")
def logout():

    # Remove the current user from the session by their unique email address.
    # None - specifies that no action is taken if logout fails.
    session.pop('email', None)

    # Redirect user to the index page.
    return redirect(url_for("index"))


# Ensures application can only be run directly - never when imported.
# Ignore for now.
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)







