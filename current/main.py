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



# ---------- Password Verification Functions ---------- #

# Verify password matches database for login attempt
def verify_password_login(password, user):
    return password == user.password
      

# Verify password meets requirements for account creation
def verify_password_create(password, email):
    nshe = email[0:10]
    return password == nshe
        
    


# ---------- Routes ---------- #

# --- Get Page Routes --- #

# Get Index Page
@app.route("/")
def home():
    if "username" in session:
        return redirect(url_for("dashboard"))
    return render_template("index.html")

# Get Create Account Page
@app.route("/create-account")
def create_account():
    return render_template("create-account.html")

# Get Login Page
@app.route("/login")
def login_page():
    return render_template("login.html")

# Get Dashboard Page
@app.route("/dashboard")
def dashboard():
    if "email" in session:
        user = User.query.filter_by(email=session["email"]).first()
        if user:
            return render_template("dashboard.html", first_name = user.first_name,
                                                     last_name  = user.last_name,
                                                     email      = user.email,
                                                     role       = user.role)
    
# --- Authentication Routes --- #

# Register
@app.route("/register", methods=["POST"])
def register():
    email = request.form["email"]
    password = request.form["nshe"]
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    role = request.form["role"]

    user = User.query.filter_by(email=email).first()
    if user:
        return render_template("create-account.html", error = "Email in use! - try again")
    elif not verify_password_create(password, email):
        return render_template("create-account.html", error = "Password must match #nshe used in email - try again")
    else:
        new_user = User()
        new_user.email = email
        new_user.password = password
        new_user.first_name = first_name
        new_user.last_name = last_name
        new_user.role = role

        db.session.add(new_user)
        db.session.commit()
        session["email"] = email
        return redirect(url_for("dashboard"))

# Login
@app.route("/login", methods=["POST"])
def login():
    # Collect info from form
    email = request.form["email"]
    password = request.form["password"]
    
    user = User.query.filter_by(email=email).first()
    if user and verify_password_login(password, user):
        session["email"] = email
        return redirect(url_for("dashboard"))
    else:
        return render_template("login.html", error = "Invalid login! - try again")

# Logout
@app.route("/logout")
def logout():
    session.pop('email', None)
    return redirect(url_for('home'))


if __name__ in "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)







