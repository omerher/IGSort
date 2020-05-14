from flask import Flask, render_template
import scrape

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/about_us')
def about_us():
    return render_template("about_us.html")

if __name__ == "__main__":
    app.run(debug=True)

