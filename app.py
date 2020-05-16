from flask import Flask, render_template, request, redirect, url_for, session
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
        
        profile = utils.get_user_info(username)
        
        if profile["is_private"]:
            pass
        
        num_posts = int(request.form["numPosts"])
        data = utils.scrape(username, num_posts)
        
        return render_template('posts.html', username=username, num_posts=num_posts, data=data, profile=profile)
    else:
        return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
