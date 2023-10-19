from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DateField, TimeField, IntegerField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Optional
from flights.models import User
import datetime as dt

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

def positive_integer(form, field):
    value = field.data
    if value <= 0:
        raise ValidationError("Value must be greater than zero.")


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
    name = StringField('Flight Name', validators=[DataRequired(), Length(min=5, max=20)])
    departure_date = DateField('Departure Date', validators=[DataRequired()])
    departure_time = TimeField('Departure Time', validators=[DataRequired()])
    duration = IntegerField('Duration (minutes)', validators=[DataRequired()])
    origin = SelectField('Origin', choices = city, validators = [DataRequired()])
    destination = SelectField('Destination', choices = city, validators = [DataRequired()])
    economy_seat = IntegerField('Economy Seats', validators=[DataRequired(), positive_integer])
    economy_price = IntegerField('Price', validators=[DataRequired(), positive_integer])
    business_seat = IntegerField(' Business Seats', validators=[DataRequired(), positive_integer])
    business_price = IntegerField('Price', validators=[DataRequired(), positive_integer])
    firstclass_seat = IntegerField('First Class Seats', validators=[DataRequired(), positive_integer])
    firstclass_price = IntegerField('Price', validators=[DataRequired(), positive_integer])
    submit = SubmitField('Submit')

    def validate_departure_time(self, departure_time):
        if dt.datetime.combine(self.departure_date.data, departure_time.data) < dt.datetime.now():
            raise ValidationError('DateTime should be equal to or greater the current DateTime.')

    def validate_duration(self, duration):
        if duration.data < 60:
            raise ValidationError('Duration should be greater than 59 minutes.')
        
    def validate_destination(self, destination):
        if destination.data == self.origin.data:
            raise ValidationError('Origin and Destination cannot be same.')
        


class UpdateFlightForm(FlaskForm):
    name = StringField('Flight Name', validators=[DataRequired(), Length(min=5, max=20)])
    departure_date = DateField('Departure Date', validators=[DataRequired()])
    departure_time = TimeField('Departure Time', validators=[DataRequired()])
    duration = IntegerField('Duration (minutes)', validators=[DataRequired()])
    origin = SelectField('Origin', choices = city, validators = [DataRequired()])
    destination = SelectField('Destination', choices = city, validators = [DataRequired()])
    submit = SubmitField('Submit')

    def validate_departure_time(self, departure_time):
        if dt.datetime.combine(self.departure_date.data, departure_time.data) < dt.datetime.now():
            raise ValidationError('DateTime should be equal to or greater the current DateTime.')

    def validate_duration(self, duration):
        if duration.data < 60:
            raise ValidationError('Duration should be greater than 59 minutes.')
        
    def validate_destination(self, destination):
        if destination.data == self.origin.data:
            raise ValidationError('Origin and Destination cannot be same.')
        


class SearchFlightForm(FlaskForm):
    city_choices = [(None, '')] + [(city, city) for city in city]
    origin = SelectField('Origin', choices = city_choices, validators=[Optional()])
    destination = SelectField('Destination', choices = city_choices, validators=[Optional()])
    date = DateField('Departure Date', validators=[Optional()])
    submit = SubmitField('Search Flight')

    def validate_destination(self, destination):
        if destination.data != 'None' and self.origin.data != 'None' and destination.data == self.origin.data:
            raise ValidationError('Origin and Destination cannot be same.')
        
    def validate_date(self, date):
        if date.data and date.data < dt.date.today():
            raise ValidationError('Date must be on or after today.')
        
