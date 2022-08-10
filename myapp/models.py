from datetime import datetime
from hashlib import md5
import jwt
from time import time
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from myapp import app, db, login


follow_rel = db.Table(
    "follow_rel",
    db.Column("follower_id",db.Integer,db.ForeignKey("user.id")),
    db.Column("followed_id",db.Integer,db.ForeignKey("user.id"))
)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref="author", lazy="dynamic")
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)
    followed = db.relationship('User',secondary=follow_rel,
        primaryjoin = (id == follow_rel.c.follower_id),
        secondaryjoin = (id == follow_rel.c.followed_id),
        backref=db.backref("followers",lazy="dynamic"),
        lazy="dynamic"
    )

    def __repr__(self):
        return f"<User {self.username} >"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size, default="identicon"):
        digest = md5(self.email.encode("utf-8")).hexdigest()
        gravatar_link = "https://gravatar.com/avatar/{}?s={}&d={}"
        user_avatar = gravatar_link.format(digest, size, default)
        return user_avatar
    
    def is_following(self, user):
        return self.followed.filter(follow_rel.c.followed_id == user.id).count() > 0

    
    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def following_posts(self):
        posts = Post.query.join(follow_rel, follow_rel.c.followed_id == Post.user_id).filter(follow_rel.c.follower_id == self.id)
        return posts

    def show_posts(self):
        posts = self.following_posts().union(self.posts).order_by(Post.timestamp.desc())
        return posts
    
    '''Expire in 10 minutes'''
    def get_reset_password_token(self,expire_time=10*60): 
        reset_password_token = jwt.encode({"reset_password":self.id,"exp":time() + expire_time},app.config["SECRET_KEY"],algorithm='HS256')
        return reset_password_token
    
    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = int(jwt.decode(token,app.config["SECRET_KEY"],algorithms=['HS256'])["reset_password"])
        except:
            return
        return User.query.get(id)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text())
    timestamp = db.Column(db.DateTime(), index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __repr__(self):
        return f"<Post {self.body}>"
