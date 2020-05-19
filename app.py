from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_session import Session
from redis import Redis
import utils
import time

app = Flask(__name__)
app.secret_key = '1234'
SESSION_TYPE = 'redis'
SESSION_REDIS = Redis(host="127.0.0.1", port=6379)
app.config.from_object(__name__)
Session(app)


@app.route('/')
def index():
    session['data'] = {}
    session['username'] = ""
    session['num_posts'] = 0
    session['profile'] = ""
    
    return render_template("index.html")

@app.route('/about/')
def about():
    return render_template("about.html")

@app.route('/submit/', methods=['POST'])
def submit():
    if request.method == "POST":
        username = request.form["username"]
        num_posts = request.form["numPosts"]

        if not username:
            flash("Username was not entered.")
            return redirect(url_for('index'))

        if not num_posts:
            flash("Number of posts was not entered.")
            return redirect(url_for('index'))
        elif "." in num_posts:
            num_posts = int(float(num_posts))
        else:
            num_posts = int(num_posts)

        if "@" in username:
            username.strip("@")

        # check for errors with accounts to minimize bugs
        allowed_str = "abcdefghijklmnopqrstuvwxyz1234567890_."
        for c in username:
            if c not in allowed_str:
                flash("Usernames must contain only letters, numbers, periods, and underscores.")
                return redirect(url_for('index'))
        
        if len(username) > 30:
            flash("Usernames can not be over 30 characters.")
            return redirect(url_for('index'))
        
        profile = utils.get_user_info(username)
        
        if profile["is_private"]:
            flash("We can't analyze private accounts. Try again with a public account.")
            return redirect(url_for('index'))
        

        data = utils.scrape(username, num_posts)
        session['data'] = data
        session['username'] = username
        session['num_posts'] = num_posts
        session['profile'] = profile
        
        return redirect(url_for('top_posts'))

@app.route('/posts/', methods=['GET', 'POST'])
def top_posts():
    data = session['data']
    username = session['username']
    num_posts = session['num_posts']
    profile = session['profile']
    
    if data != {}:
        return render_template('posts.html', username=username, num_posts=num_posts, data=data, profile=profile)
    else:
        flash("Enter a username and number of posts to start analyzing the account.")
        return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
