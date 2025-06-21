from flask import Flask, redirect, url_for, render_template, request, session,flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'secretkey'  
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # Set the database URI, using SQLite for simplicity
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable track modifications to avoid overhead
app.permanent_session_lifetime = timedelta(days=5)  

db = SQLAlchemy(app)  # Initialize SQLAlchemy

class User(db.Model):  # Define a User model for the database
    _id = db.Column("id",db.Integer, primary_key=True)  # Primary key for the User model
    username = db.Column(db.String(100), nullable=False, unique=True)  # Username field, must be unique
    email = db.Column(db.String(100), nullable=False, unique=True)  # Email field, must be unique

    def __init__(self, username, email):
        self.username = username
        self.email = email


@app.route('/')  
def home():
    return render_template('index.html')

@app.route('/view')
def view():
    return render_template('view.html', values=User.query.all())  # Render the view page with all users from the database


@app.route('/login', methods=['POST', 'GET'])  
def login():
    if request.method == 'POST':
        session.permanent = True 
        user = request.form['nm'] 
        session['user'] = user  

        # found_user =  User.query.filter_by(username=user).delete() --> if you eanted to delete a user, you could use this line instead of the next one
        found_user =  User.query.filter_by(username=user).first() # Query the database to check if the user already exists
        if found_user:  # Check if the user already exists in the database
            session['email'] = found_user.email
            flash(f"Welcome back, {user}!", "info") # If the user exists, we can retrieve their email and store it in the session  
        else:
            usr = User(user,"") # Create a new User object with the username and an empty email
            db.session.add(usr)  # Add the new user to the database
            db.session.commit()  # Commit the changes to the database

        flash(f"Welcome you have successfuly logged in, {user}!", "info") # Flash a message to the user upon login - "info" is a catergory used to indicate the type of message
        return redirect(url_for('user')) 
    else:
        if 'user' in session:
            flash("Already logged in!", "warning") # Flash a message to the user if they are already logged in - "warning" is a catergory used to indicate the type of message
            return redirect(url_for('user'))
        else:
            return render_template('login.html') 

@app.route('/logout')
def logout():
    if 'user' in session:
        user = session['user']
        flash(f"You have been logged out successfully, {user}!", "info") # Flash a message to the user upon logout - "info" is a catergory used to indicate the type of message
    else: 
        flash("You were not logged in!", "warning")
    session.pop('user', None)
    session.pop('email', None)
    return redirect(url_for('login'))  

@app.route('/user', methods=['POST','GET'])
def user():
    email = None
    if 'user' in session:
        usr = session['user']
        if request.method == 'POST':
            email = request.form['email']
            session['email'] = email
            found_user =  User.query.filter_by(username=usr).first()
            found_user.email = email
            db.session.commit()  # Commit the changes to the database
            flash("Email has been saved successfully!", "success") # Flash a message to the user upon email update - "success" is a catergory used to indicate the type of message
        else:
            if 'email' in session:
                email = session['email']
                
        return render_template('user.html', email=email) # Render the user page with the username passed to the template 'user.html'
    else:
        flash("You need to log in first!", "danger")
        return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():  
        db.create_all()       # Create the database tables if they don't exist
    app.run(debug=True) 