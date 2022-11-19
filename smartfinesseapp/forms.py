from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired,Length,Email,EqualTo

class SignupForm(FlaskForm):
    firstname = StringField("enter yoor full name", validators=[DataRequired(),Length(min=3, max=35)])
    lastname = StringField("enter yoor full name", validators=[DataRequired(), Length(min=3, max=35)])
    email = StringField("Email",validators=[Email()])
    password = PasswordField("your password must be atleast 5 characters", validators=[DataRequired(),Length(min=5)])
    confirmpass = PasswordField("passwords do not match",validators=[EqualTo('password')])
    #confirm_pass = PasswordField("make sure your password matches"validators=[DataRequired(),])
    submit = SubmitField('CREATE')
class StoreSignupForm(FlaskForm):
    storename = StringField("enter yoor full name", validators=[DataRequired(), Length(min=3, max=55)])
    email = StringField("Email",validators=[Email()])
    phone = StringField("enter your phone number", validators=[DataRequired(), Length(min=8, max=15)])
    password = PasswordField("your password must be atleast 5 characters", validators=[DataRequired(),Length(min=5)])
    confirmpass = PasswordField("passwords do not match",validators=[EqualTo('password')])
    #confirm_pass = PasswordField("make sure your password matches"validators=[DataRequired(),])
    submit = SubmitField('CREATE')