from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session
import scrape
import time

app = Flask(__name__)
app.secret_key = '1234'

@app.route('/')
def index():
    session["username"] = ""
    session["numPosts"] = ""
    session["data"] = {}
    
    return render_template("index.html")

@app.route('/about/')
def about():
    return render_template("about.html")

@app.route('/submit/', methods=['POST'])
def submit():
    username = request.form["username"]
    if "@" in username:
        username.strip("@")
    num_posts = int(request.form["numPosts"])
    data = scrape.scrape(username, num_posts)
    
    session["username"] = username
    session["numPosts"] = num_posts
    session["data"] = data
    
    return redirect(url_for('top_posts'))

@app.route('/posts/')
def top_posts():
    username = session["username"]
    num_posts = session["numPosts"]
    data = session["data"]
    
    return str(data)

if __name__ == "__main__":
    app.run(debug=True)
