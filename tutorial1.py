from flask import Flask, redirect, url_for, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello this is my first Flask app!"

@app.route('/<name>')  #http://127.0.0.1:5000 - put a name beside the URL e.g. http://127.0.0.1:5000/spencer
def user(name):
    return f"Hello {name}!"

@app.route('/admin')
def admin():
    return redirect(url_for('user',name='Admin')) # Redirects to the user route - put 'Admin' in the URL

if __name__ == '__main__':
    app.run(debug=True)