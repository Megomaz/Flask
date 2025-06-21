from flask import Flask, redirect, url_for, render_template, request, session,flash
from datetime import timedelta

app = Flask(__name__)
app.secret_key = 'secretkey'  
app.permanent_session_lifetime = timedelta(days=5)  

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
    return redirect(url_for('login'))  

@app.route('/user')
def user():
    if 'user' in session:
        usr = session['user']
        return render_template('user.html', user=usr) # Render the user page with the username passed to the template 'user.html'
    else:
        flash("You need to log in first!", "danger")
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True) 