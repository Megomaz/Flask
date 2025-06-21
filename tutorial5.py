from flask import Flask, redirect, url_for, render_template, request, session
from datetime import timedelta

app = Flask(__name__)
app.secret_key = 'secretkey'  # Set a secret key for the session management, this is required to use sessions in Flask
app.permanent_session_lifetime = timedelta(days=5)  # Set the session lifetime to 5 days, this means the session will last for 5 days before expiring

@app.route('/')  
def home():
    return render_template('index.html')

# To run - http://127.0.0.1:5000/login
@app.route('/login', methods=['POST', 'GET'])  # This route handles both POST and GET requests
def login():
    if request.method == 'POST':
        session.permanent = True # Make the session permanent, so it lasts for the duration specified in app.permanent_session_lifetime
        user = request.form['nm'] # 'nm' is the name of the input field in the 'login.html' form
        session['user'] = user # Store the username in the session for later use, thus allowing the username to be accessed in other routes without needing to pass it each time
        return redirect(url_for('user')) 
    else:
        if 'user' in session:
            return redirect(url_for('user')) # If the user is already logged in, redirect to the user page
        else:
            return render_template('login.html') # Render the login form if the user is not logged in

@app.route('/logout')
def logout():
    session.pop('user', None)  # Remove the user from the session
    return redirect(url_for('login'))  # Redirect to the home page after logging out

@app.route('/user')
def user():
    if 'user' in session:
        usr = session['user'] # check the dictionary for the key 'user' and assign it to usr
        return f"<h1>{usr}</h1>"
    else:
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)  # Run the Flask application in debug mode