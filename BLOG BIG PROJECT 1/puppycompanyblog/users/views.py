# users/views.py

# Импорты
from flask import render_template,redirect,url_for,request,flash,Blueprint
from flask_login import login_user,logout_user,current_user,login_required
# current_user. - берет данные из МОДЕЛИ того ПОЛЬЗОВАТЕЛЯ LogIn СЕССИЯ которогог сейчас открыта на компьютере

from puppycompanyblog import db
from puppycompanyblog.models import User, BlogPost
from puppycompanyblog.users.forms import LoginForm,RegistrationForm,UpdateUserForm
from puppycompanyblog.users.picture_handler import add_profile_pic


# Создание BLUEPRINTS
users = Blueprint('users',__name__)

# Register
@users.route('/register', methods=['GET','POST'])
def regiter():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)

        db.session.add(user)
        db.session.commit()
        flash('Thanks for registration')   # Если просто использовать ФЛЕШ с РЕДИРЕКТОМ то сообщение будет мгновенным 0/01 секунду, и пользователь
                                       # его не заметит. Вариант что бы заметил 1) поставить в HTML вывод ФЛЕШ сообщений в базовый шаблон!

        return redirect(url_for('users.login'))
    return render_template('register.html', form=form)


# Login
@users.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        # Фильтр-поиск по ИМЕЙЛУ так как он уникальынй, впрочем можно и по имени но по имейлу лучше. Так же берется first() что бы НЕ ПОЛУЧИТЬ СПИСОК
        user = User.query.filter_by(email = form.email.data).first()

        # Проверка Воркзергом, так как в метод мы вносим 1 аргумент а второй там уже будет от выбраного нами пользователя(ЕСЛИ ОН НАЙДЕН - is not None)
        if user.check_password(form.password.data) and user is not None:
            # Авторизируем user
            login_user(user)
            flash(' Log in Success!')

            # Создаем ОБЪЕКТ next если пользователь хъотел кудато зайти НЕ АВТОРИЗОВАНЫМ, то то ему присвоит uel_for на страницы куджа он хотел
            next = request.args.get('next')

            #Если никуда не пытался зайти раньше, или первый аргумент ДОМАШНЯЯ страница
            if next==None or not next[0]=='/':
                next = url_for('core.index')

            return redirect(next)
    return render_template('login.html', form=form)


# LogOut
@users.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('core.index'))



# Account(update) - # current_user. - берет данные из модели того ПОЛЬЗОВАТЕЛЯ LogIn СЕССИЯ которогог сейчас открыта на компьютере
@users.route('/account', methods=['GET','POST'])
@login_required
def account():

    form = UpdateUserForm()

    print(form.picture.data)
    print(form.username.data)
    print(form.email.data)

    if form.validate_on_submit():

        # Замена картинки если её загрузил пользователь
        # ВСЕ ПОРЛЯ КРОМЕ АВАТАРЫ ПРРВЕРЯЮТСЯ НА СОВПАДЕНИЯ С БДю Если совпадение найдено, то поле пропускается, если нет, то поле перезаписывает в БД!
        if form.picture.data:

            # Берутся данные ЗАГРУЖЕННАЯ КАРТИНКАК и ИМЯ ПОЛЬЗОВАТЕЛЯ для загрузки их в функцию обработки картинки которая вернет нам уже Аватару во Views
            username = current_user.username

            # Функицтя содания аватары - картинку загружаем из формы (form.picture.data) имя взяли из СЕССИИ (current_user.username)
            pic = add_profile_pic(form.picture.data, username)

            # МЕНЯЕМ картинку из МОДЕЛИ LogIn СЕССИИ ПОЛЬЗОВАТЕЛЯ ( в МОДЕЛИ прописывается) на созданую Функцией АВАТАРУ
            current_user.profile_image = pic

        # Смена Имени
        if form.username.data:
            if User.query.filter_by(username=form.username.data).first():
                pass
            else:
                current_user.username = form.username.data

        # Смена email-а
        if form.email.data:
            if User.query.filter_by(username=form.email.data).first():
                pass
            else:
                current_user.email = form.email.data


        # Подтверждаем изменения
        db.session.commit()
        flash('User Accound Updated!')

        # перенаправляение пользователя ЕСЛИ НУЖНО, но НЕ ОБЯЗАТЕЛЬНО
        return redirect(url_for('users.account'))

    # При первичной загрузке страницы ФОРМА будет не отдавать а ПОЛУЧАТЬ(GET) данные из БД заполняя свои ПОЛЯ данными из поста который будет РЕДАКТИРУЕТСЯ
    # Если ничего небыло отослано через форму то полей автозаполняются данными самой ССЕСИИ ПОЛЬЗОВАТЕЛЯ (и ничего меняется в БД)
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    # Создаем наполнение для самой страницы Аккаунта ( загрудаем туда аватару)
    # url_for - выводит на старницу указаные в скобках данные
    # --- 'static' - папка откуцда берется данные
    # --- filename= - сам файл ( 'profile_pics'+current_user.profile_image)
    profile_image = url_for('static',filename='profile_pics/'+current_user.profile_image)

    return render_template('account.html', form=form, profile_image=profile_image)


'''
    form = UpdateUserForm()

    if form.validate_on_submit():
        print(form.picture.data)
        print(form.username.data)
        print(form.email.data)


        if form.picture.data:

            username = current_user.username
            pic = add_profile_pic(form.picture.data,username)
            current_user.profile_image = pic

        if form.username.data != current_user.username :
            current_user.username = form.username.data
        else:
            pass

        if form.email.data != current_user.email:
            current_user.email = form.email.data
        else:
            pass


        db.session.commit()
        flash('User Account Updated')
        return redirect(url_for('users.account'))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    profile_image = url_for('static', filename='profile_pics/' + current_user.profile_image)
    return render_template('account.html', profile_image=profile_image, form=form)

'''

# List of user blog posts
# Забираются все блог посты асоциированые с указанным пользователем
# ВЫЗЫВАЕТСЯ В HTML ШАБЛОНЕ ЧЕРЕЗ user.username -  Используется именно user так как mы передали значение user в шаблон.
# Без этой передачи в ШАБЛОНЕ надо использовать current_user.          username же это колонка СЕССИИ current_user в БД)
@users.route('/<username>')
def user_posts(username):

    # Позволяет создать(рабить на страницы) сраницы на которых будут выводиться посты пользователя в blog_posts см. ниже.
    # request.args.get - ЗАПРОС метода get() для MultiDict - get(key, default=None, type=None))
    # МУЛЬТИСЛОВАРЬ  - https://werkzeug.palletsprojects.com/en/0.15.x/datastructures/#werkzeug.datastructures.MultiDict.get
    # 'page' - ключ словаря создания страниц
    # ,1, - страницыа которая будет выводиться при образщении. НЕ наименование а Именно СТРАНИЦА, тоесть если указакть 2, то будет перенаправлять на 2,
    #  --- а на 1 уже придется переключится самомоу
    # type=int - тип передаваемых в запрос даненых, номера страницы.
    page = request.args.get('page',1,type=int)  # КЛЮЧ 'page' берется из СЛОВАРЯ paginate(page=) см. ниже
    # Эта Строка значит что если у пользователя 150 постов, тов се 150 мы видеть не будем, а сможем перелисытывать(остальное делается в ШАБЛОНЕ БУТСТРАПОМ)

    # first_or_404() - используем так как ктото мог пытатся вручную ввести '/<username>', но в итоге ввел неправильно ( вернет 404, пользователь несуществует)
    user = User.query.filter_by(username=username).first_or_404()

    # Поиск всех постов этого найденого выше user-а  по колонке author являющейся обратной ссылкой созданной в через db.relationship в МОДЕЛИ USER()
    # .order_by(BlogPost.date.desc()) - вывод списка постов в убывающем порядке от последнего к первому
    # --- order_by - ДОПОЛНИТЕЛЬНЫЙ критерий вывода запроса
    # --- desc() - Для того чтобы сортировка производилась в обратном порядке, в утверждении ORDER BY к имени заданного столбца, в котором производится сортировка, следует добавить ключевое слово DESC (убывающий).
    # .paginate(page=page,per_page=5) - СЛОВАРЬ ПАГИНАЦИИ разбивка на страницы.ИМЕНО по этому используется ЗАПРОС ИЗ СЛОВАРЯ page = request.args.get('page',1,type=int)
    # ---Метод paginate вызывается на любом объекте query. Он принимает ТРИ аргумента:
    # --- page=         - Номер страницы, начиная с 1
    # --- per_page=     - количество элементов на страницу,
    # --- False\True    - флаг error. Если флаг выставлен в True, когда происходит выход за пределы списка, клиенту возвращается ошибка 404.
    # В противном случает будет возвращен пустой список вместо ошибки ( по умолчанию False).
    blog_posts = BlogPost.query.filter_by(author=user).order_by(BlogPost.date.desc()).paginate(page=page,per_page=5)
    # Метод paginate возвращает объект Pagination. Члены этого объекта содержат список элементов запрошеной страницы.

    return render_template('user_blog_posts.html', blog_posts=blog_posts, user=user)


# Создание Глобальной переменной Пагинации для Jinja2 которую потом надо ЗАРЕГЕСТРИРВАТЬ в ЯДРЕ (главном __init__.py)
def url_for_other_page(page):
    args = request.view_args.copy()
    args['page'] = page
    return url_for(request.endpoint, **args)
#app.jinja_env.globals['url_for_other_page'] = url_for_other_page   # # Регистрация Глобальной переменной Пагинации для Jinja2  в ЯДРЕ