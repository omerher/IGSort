from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_session import Session
import redis
import flask_excel as excel
import utils
import time
from datetime import datetime
from collections import OrderedDict

app = Flask(__name__)
app.static_folder = 'static'
app.secret_key = '1234'
SESSION_TYPE = 'redis'

r = redis.StrictRedis(host='ig-sort.redis.cache.windows.net',
        port=6380, db=0, password='xpB8GGNx8Wqj8J1Rl1RmtB9Sg2at3eyWnzbCv8kbI8U=', ssl=True)

SESSION_REDIS = r
app.config.from_object(__name__)
Session(app)


@app.route('/')
def index():
    session['username'] = ""
    session['data'] = {}
    session['num_posts'] = 0
    session['profile'] = ""
    
    return render_template("index.html")

@app.route('/about/')
def about():
    return render_template("about.html")

@app.route('/submit/', methods=['POST'])
def submit():
    if request.method == "POST":
        username = request.form["username"].lower()
        num_posts = request.form["numPosts"]

        # handles all the errors and formats
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

        allowed_str = "abcdefghijklmnopqrstuvwxyz1234567890_."
        for c in username:
            if c not in allowed_str:
                flash("Usernames must contain only letters, numbers, periods, and underscores.")
                return redirect(url_for('index'))
        
        if len(username) > 30:
            flash("Usernames can not be over 30 characters.")
            return redirect(url_for('index'))
        
        
        profile = utils.get_user_info(username)
        if isinstance(profile, str):
            flash(profile)
            return redirect(url_for('index'))
        
        if profile["is_private"]:
            flash("We can't analyze private accounts. Try again with a public account.")
            return redirect(url_for('index'))
        

        data = utils.scrape(username, num_posts)
        if isinstance(data, str):
            flash(data)
            return redirect(url_for('index'))
        
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


@app.route('/download_file')
def download_file():
    local_time = time.time() - int(request.cookies.get('localTimeZoneOffset'))*60
    file_name = "{}-{}".format(session['username'], datetime.utcfromtimestamp(local_time).strftime('%Y.%m.%d-%H.%M.%S'))
    
    data = session['data']
    
    file_data = []
    for post in data:
        post_dict = OrderedDict()
        post_dict['Likes'] = post['likes']
        post_dict['Comments'] = post['comments']
        if post['views']:
            post_dict['Views'] = post['views']
        else:
            post_dict['Views'] = "N/A"
        post_dict['Media Type'] = post['media_type']
        post_dict['Link'] = post['link']
        post_dict['Publish Date'] = post['published_date']
        
        file_data.append(post_dict)
    
    return excel.make_response_from_records(file_data, 'csv', file_name=file_name)

if __name__ == "__main__":
    excel.init_excel(app)
    app.run(debug=True)
