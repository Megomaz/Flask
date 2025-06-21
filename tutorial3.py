from flask import Flask, redirect, url_for, render_template

app = Flask(__name__)
@app.route('/')
def home():
    # Renders 'template.html', which extends 'base.html'
    return render_template('template.html')

if __name__ == '__main__':
    app.run(debug=True)  