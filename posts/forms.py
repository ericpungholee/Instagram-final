from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length 

class PostForm(FlaskForm):
    title = TextAreaField('Title', validators=[DataRequired(), Length(min=1, max=50)])
    content = TextAreaField('Content', validators=[DataRequired()])
    image_file = FileField('Image', validators=[DataRequired(), FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Post')

class CommentForm(FlaskForm):
    content = TextAreaField('Comment', validators=[DataRequired(), Length(min=1, max=150)])
    submit = SubmitField('Post')