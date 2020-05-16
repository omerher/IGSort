from flask import Flask, render_template, request, redirect, url_for, session, flash
import utils
import time

app = Flask(__name__)
app.secret_key = '1234'

@app.route('/')
def index():
    session["alert"] = False
    return render_template("index.html")

@app.route('/about/')
def about():
    return render_template("about.html")

@app.route('/posts/', methods=['GET', 'POST'])
def top_posts():
    if request.method == "POST":
        username = request.form["username"]
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
        
        num_posts = int(request.form["numPosts"])
        data = utils.scrape(username, num_posts)
        
        return render_template('posts.html', username=username, num_posts=num_posts, data=data, profile=profile)
    else:
        flash("You silly goose! You can't go straight to that page!")
        return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
