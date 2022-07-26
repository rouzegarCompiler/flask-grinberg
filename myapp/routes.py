from flask import render_template,redirect,flash,session
from myapp import app
from myapp.forms import LoginForm


@app.route("/")
@app.route("/index")
def index():
    myuser = {"username": "mohammad"}
    myposts = [
        {
            "author" : {"username" : "mohammd"},
            "body" : "This is the first post ."
        },
        {
            "author" : {"username" : "zahra"},
            "body" : "Avengers is the best movie i have ever seen !"
        }
    ]

    return render_template("index.html",user=myuser,title="Home",posts=myposts)

@app.route("/login", methods=["GET","POST"])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        flash_message = f"Username {login_form.username.data} logged in and remember me value is {login_form.remember_me.data}"
        flash(flash_message)
        return redirect("/index")

    return render_template('login.html',form=login_form)