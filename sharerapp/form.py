from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

# forms learned from class code

# used in index to open feed
class RssForm(FlaskForm):
	link = StringField('link', validators=[DataRequired()])
	submit = SubmitField('OPEN')


# used in home page to add feed
class HomeForm(FlaskForm):
	add_link = StringField('link', validators=[DataRequired()])
	add = SubmitField('Add')


# to logout
class LogoutForm(FlaskForm):
	logout = SubmitField('logout')


# login, learned from lecture code
class LoginForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	login = SubmitField('Login')


# signup, learned from lecture code
class SignupForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	email = StringField('Email', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	password2 = PasswordField('Repeat Password', validators=[DataRequired()])
	register = SubmitField('Register')