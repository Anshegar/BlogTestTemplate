# puppycompanyblog/__init__.py

# Испорт среду Flask
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app =Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'


# Создаем БАЗУ ДАННЫХ
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,'data.sqlite')
app.config['AQLALCHEMY_TRACK_MODIFICATION'] = False
db=SQLAlchemy(app)

# Создаем Миграцию
Migrate(app,db)

# Создаем среду АУТЕНТЕФИКАЦИИ\РЕГИСТРАЦИИ+инициализируем в ней приложение Flask + указываем функцию куда будет перенаправлять ДЕКОРАТОР @login_required
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


##################################################################
# Импорт Blueprints
from puppycompanyblog.core.views import core
from puppycompanyblog.error_pages.handlers import error_pages
from puppycompanyblog.users.views import users, url_for_other_page
from puppycompanyblog.blog_posts.views import blog_posts

# Регистрация Blueprints
app.register_blueprint(core)
app.register_blueprint(error_pages)
app.register_blueprint(users)
app.register_blueprint(blog_posts)

# Регистрация Глобальной переменной Пагинации для Jinja2
app.jinja_env.globals['url_for_other_page'] = url_for_other_page