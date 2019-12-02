# users\forms.py


from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import DataRequired,Email,EqualTo
from wtforms import ValidationError

# Позволяет загружать и апдейтить уже существующий на сервере png/jpeg файлы (аватары в профиле к примеру)
from flask_wtf.file import FileField,FileAllowed

# Импорты из кода
from flask_login  import current_user
from puppycompanyblog.models import User




# Формы

# Аутентефикация
class LoginForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField('Log In')


# Регистрация
class RegistrationForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(),Email()])
    username = StringField('UserName',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired(),EqualTo('pass_confirm',message='Passwords must match!')])
    pass_confirm = PasswordField('Confirm Password',validators=[DataRequired()])
    submit = SubmitField('Register!')

    # -  raise - это ОБРАБОТЧИК ОШИБОК, он лучше return когда функция вложена в другие функции, так как ретерн будет обрабатывать ошибку только
    # --- в той функции в которой прописан, а rise возбудит ошибку в любой вышестоящей функции, он как бы в кэш цепи функций в которой находится её заносит
    # Прооверка email в Базе Данных (что бы небыло совпадений)
    #!!!!!!!!!!!!! В ДОКУМЕНТАЦИИ ПРАИВЛЬНО ПИСАТЬ ВОТ ТАК через  validate_<field_name>  - это ПОЛЬЗОВАТЕЛЬСКИЙ ВАЛИДАТОР!!!!!!!!!!!!!
    # Так же в HTML ШАБЛОН где будет эта форма автоматически передается СПИСОК(лист) form.username.errors с пояснениями ошибок ВСЕХ описаных в форме
    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
            print('Ошибка!')
            raise ValidationError('Your email has been already registered!')


    def validate_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username is taken!')




# Изменение Профиля пользователя
class UpdateUserForm(FlaskForm):

    # Поля для изменения email и username
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('UserName', validators=[DataRequired()])

    # Поле для изменения аватары ( картинки), которая в моделях прописана дефолтной
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg','jpeg', 'png'])])
    #FileAllowed(['...','...','...']) - Лист(список) расширений файлов которые позволено загружать в это поле

    submit = SubmitField('Update')
# УБРАЛ ПРОВЕРКУ ТАК КАК С НЕЙ НЕПОЛУЧАЛОСЬ МЕНЯТЬ ПАРАМЕТРЫ ОТДЕЛЬНЫХ ПОЛЕЙ!, приходилось вносить изменения во ВСЕ СРАЗУ
# ПРОВЕРКА ПЕРЕНЕСЕНА В users/views.py def account():

'''
    # -  raise - это ОБРАБОТЧИК ОШИБОК, он лучше return когда функция вложена в другие функции, так как ретерн будет обрабатывать ошибку только
    # --- в той функции в которой прописан, а rise возбудит ошибку в любой вышестоящей функции, он как бы в кэш цепи функций в которой находится её заносит
    # Прооверка email в Базе Данных (что бы небыло совпадений)
    #!!!!!!!!!!!!! В ДОКУМЕНТАЦИИ ПРАИВЛЬНО ПИСАТЬ ВОТ ТАК через  validate_<field_name>  - это ПОЛЬЗОВАТЕЛЬСКИЙ ВАЛИДАТОР!!!!!!!!!!!!!
    # Так же в HTML ШАБЛОН где будет эта форма автоматически передается СПИСОК(лист) form.username.errors с пояснениями ошибок ВСЕХ описаных в форме

    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
            print('Ошибка!')
            raise ValidationError('Your email has been already registered!')


    def validate_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username is taken!')

'''
'''




HTML Страница Регистрации!!!!! очень важно передать ошибки!
{% extends 'base.html' %}
{% block content %}
    <form method="POST">
        {{form.hidden_tag()}}

        {{form.email.label}}{{form.email()}}
        {% for error in form.email.errors %}
            <span style="color: red;">[{{ error }}]</span>
        {% endfor %}
        <br>
        {{form.username.label}}{{form.username()}}
        {% for error in form.username.errors %}
            <span style="color: red;">[{{ error }}]</span>
        {% endfor %}
        <br>
        {{form.password.label}}{{form.password()}}
        {% for error in form.password.errors %}
            <span style="color: red;">[{{ error }}]</span>
        {% endfor %}
        <br>
        {{form.pass_confirm.label}}{{form.pass_confirm()}}<br>
        {{form.submit()}}
    </form>
{% endblock %}



HTML Аккаунт страница крайне ВАЖНО не забыть в форме с загрузкой файла установить ЭНКРИПТИНГ! <form method="POST" action="" enctype="multipart/form-data">

{% extends 'base.html'%}
{% block content %}
<div class="jumbotron">
    <div align="center">
        <h1> Welcome to the page for {{current_user.username}}</h1>
        <img align= "center" src="{{url_for('static',filename='profile_pics/'+current_user.profile_image)}}">
    </div>
</div>
{#  При ЗАГРУЗКЕ КАРТИНКИ  !!! ВАЖНО !!! прописать action="" enctype="multipart/form-data" иначе не примет картинку! #}
<form method="POST" action="" enctype="multipart/form-data">
        {{form.hidden_tag()}}
        <div class="form-group">
        {{form.username.label(class='form-group')}}
        {{form.username(class='form-control')}}
        </div>
        {% for error in form.username.errors %}
            <span style="color: red;">[{{ error }}]</span>
        {% endfor %}
<div class="form-group">
        {{form.email.label(class='form-group')}}
        {{form.email(class='form-control')}}
        </div>
        {% for error in form.email.errors %}
            <span style="color: red;">[{{ error }}]</span>
        {% endfor %}
<div class="form-group">
        {{form.picture.label(class='form-group')}}
        {{form.picture(class='form-control')}}
        </div>
        {% for error in form.picture.errors %}
            <span style="color: red;">[{{ error }}]</span>
        {% endfor %}
<div class="form-group">
        {{form.submit(class='btn btn-primary')}}
</div>
</form>
{% endblock %}

'''

