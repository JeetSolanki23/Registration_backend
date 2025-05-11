from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField, DateField, IntegerField, SelectField,
    FileField
)
from wtforms.validators import DataRequired, Email, Length, EqualTo, Optional

class VisitorRegistrationForm(FlaskForm):
    phone = StringField(validators=[DataRequired(), Length(min=10, max=15)])
    email = StringField(validators=[DataRequired(), Email()])
    password = PasswordField(validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField(validators=[DataRequired(), EqualTo('password')])

    full_name = StringField(validators=[DataRequired()])
    dob = DateField(validators=[DataRequired()], format='%Y-%m-%d')
    age = IntegerField(validators=[DataRequired()])
    gender = SelectField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], validators=[DataRequired()])

    address = StringField(validators=[DataRequired()])
    city = StringField(validators=[DataRequired()])
    state = StringField(validators=[DataRequired()])
    country = StringField(validators=[DataRequired()])
    pincode = StringField(validators=[DataRequired()])
    nationality = StringField(validators=[DataRequired()])

    person_image = FileField(validators=[Optional()])
    id_proof_type = SelectField(choices=[
        ('Aadhar', 'Aadhar'),
        ('Passport', 'Passport'),
        ('VoterID', 'Voter ID'),
        ('DrivingLicense', 'Driving License'),
        ('Other', 'Other')
    ], validators=[DataRequired()])
    id_proof_number = StringField(validators=[DataRequired()])
    id_proof_photo = FileField(validators=[Optional()])


class VisitorLoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
