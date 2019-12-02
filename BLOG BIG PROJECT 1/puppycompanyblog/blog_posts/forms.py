# blog_posts\forms.py


from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField
from wtforms.validators import DataRequired


class BlogPostForm(FlaskForm):
    # Дату вносить ненадо так как она автоматически прописывается в МОДЕЛИ в момент СОЗДАНИЯ Поста
    title = StringField('Title', validators=[DataRequired()])
    text = TextAreaField('Text', validators=[DataRequired()])
    submit = SubmitField('Post')
