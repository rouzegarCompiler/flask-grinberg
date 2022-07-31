import unittest
from datetime import datetime, timedelta
from myapp import app, db
from myapp.models import User, Post


class TestUserModel(unittest.TestCase):
    def setUp(self):
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"
        app.config["SQLALCHEMY_ECHO"] = False
        db.create_all()
        self.u1 = User(username="mohammad",email="mohammad.rouzegar78@gmail.com")
        self.u2 = User(username="ali",email="ali@sample.com")
        self.u3 = User(username="reza",email="reza_reza@gmail.com")
        db.session.add_all([self.u1,self.u2,self.u3])
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()
    
    def test_check_password(self):
        u1 = User(username="mohammad",email="mohammad.rouzegar78@gmail.com")
        u1.set_password("secure-password")
        self.assertTrue(u1.check_password("secure-password"))
        self.assertFalse(u1.check_password("not-secure-password"))
    
    def test_avatar(self):
        u1 = User(username="mohammad",email="mohammad.rouzegar78@gmail.com")
        avatarsize = 128
        avatar = "https://gravatar.com/avatar/{}?s={}&d=identicon".format("646dcad689a3c56ad5da1f5ce07f0b27", avatarsize)
        self.assertEqual(u1.avatar(avatarsize),avatar)
    
    def test_is_following(self):
        u1 = User(username='john', email='john@example.com')
        u2 = User(username='susan', email='susan@example.com')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        self.assertEqual(u1.followed.all(), [])
        self.assertEqual(u1.followers.all(), [])

        u1.follow(u2)
        db.session.commit()
        self.assertTrue(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 1)
        self.assertEqual(u1.followed.first().username, 'susan')
        self.assertEqual(u2.followers.count(), 1)
        self.assertEqual(u2.followers.first().username, 'john')

        u1.unfollow(u2)
        db.session.commit()
        self.assertFalse(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 0)
        self.assertEqual(u2.followers.count(), 0)

    def test_follow_posts(self):
        u1 = User(username='john', email='john@example.com')
        u2 = User(username='susan', email='susan@example.com')
        u3 = User(username='mary', email='mary@example.com')
        u4 = User(username='david', email='david@example.com')
        db.session.add_all([u1, u2, u3, u4])

        now = datetime.utcnow()
        p1 = Post(body="post from john", author=u1,
                  timestamp=now + timedelta(seconds=1))
        p2 = Post(body="post from susan", author=u2,
                  timestamp=now + timedelta(seconds=4))
        p3 = Post(body="post from mary", author=u3,
                  timestamp=now + timedelta(seconds=3))
        p4 = Post(body="post from david", author=u4,
                  timestamp=now + timedelta(seconds=2))
        db.session.add_all([p1, p2, p3, p4])
        db.session.commit()

        
        u1.follow(u2)  
        u1.follow(u4) 
        u2.follow(u3)  
        u3.follow(u4)  
        db.session.commit()

        
        f1 = u1.show_posts()
        f2 = u2.show_posts()
        f3 = u3.show_posts()
        f4 = u4.show_posts()
        self.assertEqual(f1, [p2, p4, p1])
        self.assertEqual(f2, [p2, p3])
        self.assertEqual(f3, [p3, p4])
        self.assertEqual(f4, [p4])

if __name__ == "__main__":
    unittest.main(verbosity=2)   