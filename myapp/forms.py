from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length
from myapp.models import User


class LoginForm(FlaskForm):
    username = StringField(label='Username', validators=[DataRequired()])
    password = PasswordField(label="Password", validators=[DataRequired()])
    remember_me = BooleanField(label="Remember Me")
    submit = SubmitField(label="Sign In")


class RegisterForm(FlaskForm):
    username = StringField(label="Username", validators=[DataRequired()])
    email = StringField(label="Email", validators=[DataRequired(), Email()])
    password = PasswordField(label="Password", validators=[DataRequired()])
    password2 = PasswordField(label="Password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Register")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError("Username is duplicated, Enter another username")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError("Email is duplicated, Enter another email")


class EditProfileForm(FlaskForm):
    username = StringField(label="Username")
    about_me = TextAreaField(label="About Me", validators=[Length(min=0, max=140)])
    submit = SubmitField("Edit")

    def __init__(self, original_user , *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_user = original_user
    
    def validate_username(self,username):
        if self.original_user != username.data:
            user = User.query.filter_by(username=username.data).first()
            if user is not None:
                raise ValidationError("Username is duplicated, Enter another username")