from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, SubmitField, FileField
from wtforms.validators import EqualTo, InputRequired
from flask_wtf.file import FileAllowed, FileRequired
from app import photos


class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired()])
    password = PasswordField('password', validators=[InputRequired()])
    remember_me = BooleanField('remember_me', default=False)
    submit = SubmitField('登录')


class RegisterForm(FlaskForm):
    username = StringField('username', validators=[InputRequired()])
    password = PasswordField('password', validators=[InputRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[InputRequired(), EqualTo('password')])
    submit = SubmitField('注册')


class IconForm(FlaskForm):
    icon = FileField('icon',
                     validators=[FileRequired(message='请选择文件'), FileAllowed(photos, message='格式错误')])
    submit = SubmitField('提交')


class PasswordForm(FlaskForm):
    password = PasswordField('password', validators=[InputRequired()])
    newpassword = PasswordField('newpassword', validators=[InputRequired()])
    newpassword2 = PasswordField(validators=[InputRequired(), EqualTo('newpassword')])
    submit = SubmitField('确认')
