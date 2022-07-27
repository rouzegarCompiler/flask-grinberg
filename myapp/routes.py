from flask import render_template, redirect, flash, url_for, session
from flask_login import login_user, current_user
from myapp import app
from myapp.forms import LoginForm
from myapp.models import User


@app.route("/")
@app.route("/index")
def index():
    myuser = {"username": "mohammad"}
    myposts = [
        {
            "author": {"username": "mohammd"},
            "body": "This is the first post ."
        },
        {
            "author": {"username": "zahra"},
            "body": "Avengers is the best movie i have ever seen !"
        }
    ]

    return render_template("index.html", user=myuser, title="Home", posts=myposts)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(username=login_form.username.data).first()
        if user is None or not user.check_password(login_form.password.data):
            flash("Invalid username or password !")
            return redirect(url_for("login"))
        login_user(user=user, remember=login_form.remember_me.data)
        return redirect(url_for("index"))
    return render_template('login.html', form=login_form)
