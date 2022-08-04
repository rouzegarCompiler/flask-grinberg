from flask import render_template, redirect, flash, url_for, request
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.urls import url_parse
from datetime import datetime
from myapp import app, db
from myapp.forms import LoginForm, RegisterForm, EditProfileForm,PostForm
from myapp.models import User, Post
from myapp.faker import fake

@app.before_request
def before_request_handler():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@app.route("/",methods=["GET","POST"])
@app.route("/index",methods=["GET","POST"])
@login_required
def index():
    post_form = PostForm()
    if post_form.validate_on_submit():
       post = Post(body=post_form.body.data,author=current_user) 
       db.session.add(post)
       db.session.commit()
           
       flash("Your post added successfully")
       return redirect(url_for("index"))
    page_number = request.args.get("page",default=1,type=int)
    posts = current_user.show_posts().paginate(page=page_number,per_page=app.config["POSTS_PER_PAGE"],error_out=False)
    prev_page = url_for("index",page=posts.prev_num) if posts.has_prev else None
    next_page = url_for("index",page=posts.next_num) if posts.has_next else None
    return render_template("index.html", title="Home", posts=posts.items,form=post_form,prev_page=prev_page, next_page=next_page)

@app.route("/explore")
@login_required
def explore():
    page_number = request.args.get("page",default=1,type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(page=page_number,per_page=app.config["POSTS_PER_PAGE"],error_out=False)
    prev_page = url_for("explore",page=posts.prev_num) if posts.has_prev else None
    next_page = url_for("explore",page=posts.next_num) if posts.has_next else None
    return render_template("index.html",title="Explore page",posts=posts.items,prev_page=prev_page,next_page=next_page)


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
        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for("index")
        return redirect(next_page)
    return render_template('login.html', form=login_form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    register_form = RegisterForm()
    if register_form.validate_on_submit():
        user = User(username=register_form.username.data, email=register_form.username.data)
        user.set_password(register_form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("You're registration completed !!!")
        return redirect(url_for("login"))
    return render_template("register.html", form=register_form)


@app.route("/user/<username>")
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page_number = request.args.get("page",default=1,type=int)
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(page=page_number,per_page=app.config["POSTS_PER_PAGE"],error_out=False)
    prev_page = url_for("user",page=posts.prev_num,username=username) if posts.has_prev else None
    next_page = url_for("user",page=posts.next_num,username=username) if posts.has_next else None
    return render_template("user.html", user=user, posts=posts.items , prev_page=prev_page,next_page=next_page)


@app.route("/edit_profile", methods=["GET", "POST"])
@login_required
def edit_profile():
    edit_profile_form = EditProfileForm(original_user=current_user.username)
    if request.method.upper() == "POST" and edit_profile_form.validate_on_submit():
        current_user.username = edit_profile_form.username.data
        current_user.about_me = edit_profile_form.about_me.data
        db.session.commit()
        flash("Profile updated successfully !")
        return redirect(url_for("edit_profile"))
    elif request.method.upper() == "GET":
        edit_profile_form.username.data = current_user.username
        edit_profile_form.about_me.data = current_user.about_me
    return render_template("edit_profile.html", form=edit_profile_form)


@app.route("/follow/<username>")
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        flash("User not found !")
        return redirect(url_for("index"))
    elif user == current_user:
        flash("You can not follow yourself !")
        return redirect(url_for("user", username = current_user.username))
    
    current_user.follow(user)
    db.session.commit()
    flash(f"You followed {username}")
    return redirect(url_for("user",username = username))


@app.route("/unfollow/<username>")
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        flash("User not found !")
        return redirect(url_for("index"))
    elif user == current_user:
        flash("You can not unfollow yourself !")
        return redirect(url_for("user", username = current_user.username))
    current_user.unfollow(user)
    db.session.commit()
    flash(f"You unfollowed {username}")
    return redirect(url_for("user",username = username))
