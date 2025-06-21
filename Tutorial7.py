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


@app.route('/login', methods=['POST', 'GET'])  
def login():
    if request.method == 'POST':
        session.permanent = True 
        user = request.form['nm'] 
        session['user'] = user  
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
            flash("Email has been saved successfully!", "success") # Flash a message to the user upon email update - "success" is a catergory used to indicate the type of message
        else:
            if 'email' in session:
                email = session['email']
                
        return render_template('user.html', email=email) # Render the user page with the username passed to the template 'user.html'
    else:
        flash("You need to log in first!", "danger")
        return redirect(url_for('login'))

if __name__ == '__main__':
    db.create_all()  # Create the database tables if they don't exist
    app.run(debug=True) 