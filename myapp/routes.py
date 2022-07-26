from flask import render_template
from myapp import app


@app.route("/")
@app.route("/index")
def index():
    myuser = {"username": "mohammad"}
    return render_template("index.html",user=myuser,title="Home")
