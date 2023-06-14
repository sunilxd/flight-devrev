from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DateField, TimeField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flights.models import User
from datetime import datetime as dt

city = ['Agartala',
 'Ahmedabad',
 'Aizawl',
 'Amritsar',
 'Bangalore',
 'Bhopal',
 'Bhubaneswar',
 'Chandigarh',
 'Chennai',
 'Coimbatore',
 'Dehradun',
 'Delhi',
 'Diu',
 'Goa',
 'Guwahati',
 'Hyderabad',
 'Imphal',
 'Jaipur',
 'Jammu',
 'Kanpur',
 'Kolkata',
 'Lucknow',
 'Mangalore',
 'Mumbai',
 'Nagpur',
 'Pune',
 'Tiruchirappalli',
 'Trivandrum',
 'Vadodara',
 'Varanasi']


class RegistrationForm(FlaskForm):
    name = StringField('Name',
        validators=[DataRequired(), Length(min=5, max=50)])
    email = StringField('Email',
        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email',
        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class AdminLoginForm(FlaskForm):
    name = StringField('Name',
        validators=[DataRequired(), Length(min=3, max=10)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class AddFlightForm(FlaskForm):
    name = StringField('Flight Name', validators=[DataRequired(), Length(min=5, max=30)])
    departure_date = DateField('Departure Date', validators=[DataRequired()])
    departure_time = TimeField('Departure Time', validators=[DataRequired()])
    duration = IntegerField('Duration (minutes)', validators=[DataRequired()])
    origin = SelectField('Origin', choices = city, validators = [DataRequired()])
    destination = SelectField('Destination', choices = city, validators = [DataRequired()])
    economy_seat = IntegerField('Economy Seats', validators=[DataRequired()])
    economy_price = IntegerField('Price', validators=[DataRequired()])
    business_seat = IntegerField(' Business Seats', validators=[DataRequired()])
    business_price = IntegerField('Price', validators=[DataRequired()])
    firstclass_seat = IntegerField('First Class Seats', validators=[DataRequired()])
    firstclass_price = IntegerField('Price', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def validate_departure_time(self, departure_time):
        if dt.combine(self.departure_date.data, departure_time.data) < dt.now():
            raise ValidationError('DateTime should be equal to or greater the current DateTime.')

    def validate_duration(self, duration):
        if duration.data < 60:
            raise ValidationError('Duration should be greater than or equal to 60 minutes.')
        