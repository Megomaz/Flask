from flask import Flask, redirect, url_for, render_template, request

app = Flask(__name__)

@app.route('/')  
def home():
    return render_template('index.html')

# To run - http://127.0.0.1:5000/login
@app.route('/login', methods=['POST', 'GET'])  # This route handles both POST and GET requests
def login():
    if request.method == 'POST':
        user = request.form['nm'] # 'nm' is the name of the input field in the 'login.html' form
        return redirect(url_for('user', usr=user)) # Redirects to the user route with the username as a parameter
    else:
        return render_template('login.html')


@app.route('/<usr>')
def user(usr):
    return f"<h1>{usr}</h1>"

if __name__ == '__main__':
    app.run(debug=True)  # Run the Flask application in debug mode