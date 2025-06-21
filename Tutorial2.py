from flask import Flask, redirect, url_for, render_template

app = Flask(__name__)

@app.route('/<name>') #http://127.0.0.1:5000 - put a name beside the URL to run e.g. http://127.0.0.1:5000/spencer
def home(name):
    return render_template('index.html', content=name, number=42, arr=["Amy","Spencer","Denzel", "Ryan"]) # 'Content' and 'number' are variables passed to the template, they can be found in index.html

if __name__ == '__main__':
    app.run(debug=True)