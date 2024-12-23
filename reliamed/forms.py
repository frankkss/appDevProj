from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, HiddenField, IntegerField, TextAreaField, DecimalField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError, Optional
from reliamed.models import User, Pharmaceuticals
from flask_wtf.file import FileField

class RegisterForm(FlaskForm):
    csrf_token = HiddenField()
    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exists! Please try a different username')

    def validate_email_address(self, email_address_to_check):
        email_address = User.query.filter_by(email_address=email_address_to_check.data).first()
        if email_address:
            raise ValidationError('Email Address already exists! Please try a different email address')

    username = StringField(label='User Name:', validators=[Length(min=2, max=30), DataRequired()])
    email_address = StringField(label='Email Address:', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password:', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirm Password:', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create Account')

class LoginForm(FlaskForm):
    csrf_token = HiddenField()
    username = StringField(label='User Name:', validators=[DataRequired()])
    password = PasswordField(label='Password:', validators=[DataRequired()])
    submit = SubmitField(label='Sign in')

class PurchaseProductForm(FlaskForm):
    csrf_token = HiddenField()
    submit = SubmitField(label='Purchase Product!')

class SellProductForm(FlaskForm):
    csrf_token = HiddenField()
    submit = SubmitField(label='Sell Product!')
    
# Admin User form: Create, Update, Delete
class AdminUserForm(FlaskForm):
    csrf_token = HiddenField()
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=30)])
    email_address = StringField('Email Address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Optional(), Length(min=6)])
    is_admin = BooleanField('Admin')
    submit = SubmitField('Submit')

    def __init__(self, original_username=None, original_email=None, *args, **kwargs):
        super(AdminUserForm, self).__init__(*args, **kwargs)
        self.original_username = original_username
        self.original_email = original_email

    def validate_username(self, username):
        if username.data != self.original_username:  # Ensure it doesn't validate against itself
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username is already in use. Please choose a different one.')

    def validate_email_address(self, email_address):
        if email_address.data != self.original_email:  # Ensure it doesn't validate against itself
            user = User.query.filter_by(email_address=email_address.data).first()
            if user:
                raise ValidationError('Email address is already in use. Please choose a different one.')

class AdminLoginForm(FlaskForm):
    csrf_token = HiddenField()
    username = StringField(label='User Name', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    submit = SubmitField(label='Sign in')

# Added a medicine form for adding and updating medicines
class MedicineForm(FlaskForm):
    csrf_token = HiddenField()
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=30)])
    price = IntegerField('Price', validators=[DataRequired()])
    barcode = StringField('Barcode', validators=[DataRequired(), Length(min=12, max=12)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=2, max=1024)])
    submit = SubmitField('Submit')
    

#User form: Edit user profile information, Change password ,Upload and display profile pictures
class UserForm(FlaskForm):
    csrf_token = HiddenField()
    name = StringField("Name", validators=[DataRequired()])
    username = StringField("Username", validators=[DataRequired()])
    email_address = StringField("Email Address", validators=[DataRequired(), Email()])
    password_hash = PasswordField('Password', validators=[DataRequired(), EqualTo('password_hash2', message='Passwords Must Match!')])
    password_hash2 = PasswordField('Confirm Password', validators=[DataRequired()])
    profile_pic = FileField("Profile Pic")
    submit = SubmitField("Submit")

class ChangePasswordForm(FlaskForm):
    csrf_token = HiddenField()
    current_password = PasswordField('Current Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired(), Length(min=6)])
    confirm_new_password = PasswordField('Confirm New Password', validators=[DataRequired(), EqualTo('new_password', message='Passwords must match')])
    submit = SubmitField('Change Password')