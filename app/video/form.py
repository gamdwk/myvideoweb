from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField, StringField, BooleanField, SelectField, TextAreaField
from wtforms.validators import DataRequired, InputRequired
from flask_wtf.file import FileAllowed, FileRequired
from app import videos


class VideoUploadForm(FlaskForm):
    video = FileField('video', validators=[FileRequired(message='请选择文件'), FileAllowed(videos, message='格式错误')])
    title = StringField(validators=[InputRequired('标题不能为空')])
    tag = SelectField('tags', choices=[
        ('game', '游戏'),
        ('life', '生活'),
        ('movie', '影视'),
        ('music', '音乐'),
        ('else', '其他')
    ])
    submit = SubmitField('提交')


class CommentForm(FlaskForm):
    comment = TextAreaField('comment', validators=[InputRequired()])
    submit = SubmitField('发表')
