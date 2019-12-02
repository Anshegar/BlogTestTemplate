# models.py
from puppycompanyblog import db,login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime

# Если пользователь АВТОРИЗОВАН, то позволяет использовать в template различные ФУНКЦИИ из flask_login вроде current_user.is_authenticated
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


# Модель для РЕГИСТРАЦИИ и Аутентефикации(Login) пользователей
class User(db.Model,UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)

    # Прием аватара  как ССЫЛКИ , поэтому принимает строку
    # nullable=False - неможет быть пустой, и если пользователь аватар не загрузил то ставится дефолтная картинка
    # default='default_profile.png' - непосредственна сама Дефалтная картинка аватара(папка static/profile_pics), если пользователь не загрузил свою
    # Папка дефалт задана в users\views.py def account(): profile_image = url_for('static',filename='profile_pics/'+current_user.profile_image)
    profile_image = db.Column(db.String(64),nullable=False, default='default_profile.png')

    # unique=True - email ДОЛЖЕН быть УНИКАЛЬНЫМ
    # index=True -   создается в Колонке значения которой должны быть УНИКАЛЬНЫМИ для всей таблицы, загружает память. Нужны только в важных столбцах иначе будут тормоза
    email = db.Column(db.String(64),unique=True,index=True)

    # unique=True - email ДОЛЖЕН быть УНИКАЛЬНЫМ
    # index=True -   создается в Колонке значения которой должны быть УНИКАЛЬНЫМИ для всей таблицы, загружает память. Нужны только в важных столбцах иначе будут тормоза
    username = db.Column(db.String(64),unique=True,index=True)

    # Уже ХЭШИРОВАННЫЙ Пароль
    password_hash = db.Column(db.String(128))

    # СВЯЗЬ-колонка таблиц - Пользователя(РОДИТЕЛЬСКАЯ) с его БлогПостами(ДОЧЕРНЯЯ)
    # РОДИТЕЛЬСКАЯ МОДЕЛЬ от её атрибутов оталкиваются запросы (главная)
    posts = db.relationship('BlogPost', backref = 'author', lazy=True)

    # Конструктор класса
    def __init__(self,email,username,password):
        self.email    = email
        self.username = username

        # Хэширование вносимого в БД пароля при Регистрации нового пользователя
        self.password_hash = generate_password_hash(password)

    # Сверка хэшированого пароля из БД с ввеленым паролем при Аутентефикации Пользователя
    def check_password(self,password):
        return check_password_hash(self.password_hash,password)


    def __repr__(self):
        return f'Username {self.username}'



class BlogPost(db.Model):

    # Связь позволяющая обращаться к атрибутам МОДЕЛИ Родительской-Связи из МОДЕЛИ Дочерней-Связи, так же просто как это делает МОДЕЛЬ Ролительской-Связи
    # обращаясь к атрибутам МОДЕЛИ Дочерней-Связи
    users = db.relationship(User)

    id = db.Column(db.Integer,primary_key= True)
    # Дата публикации
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # Заголовок Публикации
    title = db.Column(db.String(140),nullable=False)
    # Текст Публикации
    text = db.Column(db.Text,nullable=False)

    # ДОЧЕРНЯЯ МОДЕЛЬ её атрибуты передаются по запросу от атрибута РОДИТЕЛЬСКОЙ  МОДЕЛИ(без РОДИТЕЛЬСКОЙ не создать)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'), nullable=False)



    # Конструктор. данные приходящие извне ( дата к ним не относится)
    def __init__(self,title,text,user_id):
        self.title   = title
        self.text    = text
        self.user_id = user_id


    def __repr__(self):
        return f'Post id: {sefl.id} --- Date: {self.date} --- Title: {self.title}'


