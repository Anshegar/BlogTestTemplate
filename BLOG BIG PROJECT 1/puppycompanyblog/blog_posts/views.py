# blog_posts/views.py

# Импорты
from flask import render_template,redirect,url_for,request,flash,Blueprint
from flask_login import current_user,login_required
# current_user. - берет данные из МОДЕЛИ того ПОЛЬЗОВАТЕЛЯ LogIn СЕССИЯ которогог сейчас открыта на компьютере

from puppycompanyblog import db
from puppycompanyblog.models import BlogPost
from puppycompanyblog.blog_posts.forms import BlogPostForm


# Создание BLUEPRINTS
blog_posts = Blueprint('blog_posts',__name__)

#CREATE
@blog_posts.route('/create', methods=['GET','POST'])
@login_required
def create_post():
    form = BlogPostForm()

    if form.validate_on_submit():
        # Создаем ОБЪЕКТИ МОДЕЛИ BlogPost() - Берутся поля заполнения БД title и text (id и date заполняются автоматически)
        # + УСТАНАВЛИВАЕТСЯ СВЯЗЬ С User() через user_id = db.Column(db.Integer,db.ForeignKey('users.id'), nullable=False). т.к. user_id ЕСТЬ в __init__
        # Тоесть создавая запись в блоге сразу связывает её с Авторизированным в данную СЕССИЮ пользователем
        blog_posts = BlogPost(title=form.title.data,
                              text=form.text.data,
                              user_id=current_user.id)
        #Добвляем созданный объект в БД
        db.session.add(blog_posts)
        db.session.commit()
        flash('Post Created')
        return redirect(url_for('core.index'))

    return render_template('create_post.html', form=form)

#VIEW BLOG POST ( каждый блог пост имет уникальный ID, а значит моржно сделать ДИНАМИЧЕСКИЙ ДЕКОРАТОР)
# ВАЖНО УКАЗАТЬ что URL должен быть integer (цифра), так как ПО УМОЛЧАНИЮ в URL передается СТРОКА, а мы должны ИСКАТЬ В БД ЦИФРУ
@blog_posts.route('/int:<blog_post_id>')
def blog_post(blog_post_id):
    # Забор ЦИФРЫ ID из переданой в функцию переменной ( передаем  ОБЪЕКТЫ МОДЕЛИ из БД BlogPost())
    blog_post = BlogPost.query.get_or_404(blog_post_id)

    # Обрабатывается только один BlogPost который был передан через ID
    # Можно как передать ВЕСЬ ОБЪЕКТ BlogPost, а в HTML шаблоне их доставать из него так и его отдельные части сразу
    return render_template('blog_post.html', title = blog_post.title,
                           text = blog_post.text,
                           date = blog_post.date,
                           post = blog_post)


#UPDATE
# СИМБИОЗ СОЗДАНИЯ(форма+необходимость Авторизации) и ПРОСМОТРА(передача динамической переменной ID поста)
@blog_posts.route('/<int:blog_post_id>/update', methods=['GET','POST'])
@login_required
def update(blog_post_id):

    # Забор ЦИФРЫ ID из переданой в функцию переменной ( передаем  ОБЪЕКТЫ МОДЕЛИ из БД BlogPost())
    blog_post = BlogPost.query.get_or_404(blog_post_id)

    # !!! ВАЖНО !!! ПРОВЕРКА что ПОЛЬЗОВАТЕЛЬ и есть Автор поста (что бы кто угодно залогинивийся не мог ИЗМЕНИТЬ чужой пост)!
    # if current_user.id == blog_post.user_id или второй вариант:
    if blog_post.author!= current_user:
        # Можно просто pass, + прописать все в HTML шаблорне что ыб кнопка Update просто ен показывалась при  {%if blog_post.author!= current_user %}
        abort(403)

    # Если же автор и юзер сопадают то просто даем форму создания поста которая перезапишет в БД новые данные
    form = BlogPostForm()
    if form.validate_on_submit():
        # ОБЪЕКТИ МОДЕЛИ BlogPost() НЕ: СОЗДАЕТСЯ, так как мы уже взяли его выше, нашли в БД через динамический ДЕКОРАТОР ID -
        # + УСТАНАВЛИВАЕТСЯ СВЯЗЬ С User() через user_id = db.Column(db.Integer,db.ForeignKey('users.id'), nullable=False). т.к. user_id ЕСТЬ в __init__
        # ЗАМЕНЯЕМ ПОЛЯ в найденом ранее в БД ОБЪЕКТЕ на новые данные из ФОРМЫ
        blog_post.title = form.title.data
        blog_post.text = form.text.data
        # user_id менять смысла нет, так как он уже доказано что тот же что и Автор

        # Возвращаем(поддтверждаем ИЗМЕНЕНИЯ) объект в БД (а не создаем новый)
        db.session.commit()
        flash('Post Updated')

        # Переадресация идет иммено на тот пост которы йбьлы изменены , для этого передаем в ШАБЛОН ID измененного поста
        # (можно и переменную динамического декоратора)
        return redirect(url_for('blog_posts.blog_post',blog_post_id=blog_post.id))

    # При первичной загрузке страницы ФОРМА будет не отдавать а ПОЛУЧАТЬ(GET) данные из БД заполняя свои ПОЛЯ данными из поста который будет РЕДАКТИРУЕТСЯ
    # Если ничего небыло отослано через форму то полей автозаполняются данными самой ССЕСИИ ПОЛЬЗОВАТЕЛЯ (и ничего меняется в БД)
    elif request.method == 'GET':
        form.title.data = blog_post.title
        form.text.data = blog_post.text

    # title в ШАБЛОНЕ будет заменен на нашу переменную!
    return render_template('create_post.html', title = 'Updating', form=form)
    #АЛЬТЕРНАТИВА:
    #При первичной загрузке страницы СРАЗУ заполняет поля формы текстом из редактируемого поста, что бы ПОЛЬЗОВАТЕЛЬ видел что он меняет, опять таки
    #можно передать  сразу blog_post и разобрать его уже в ШАБЛОНЕ, а можно почастям
    #return render_template('update.html', form=form, blog_post=blog_post)



#DELETE
# Не будет имет ШАБЛОНА а создадим его через BootsTrap так же зачемто методы переданы
# methods=['GET','POST'], такак будет обработка МИНИ формы для МОДАЛЬНОГО ТОКНА
@blog_posts.route('/<int:blog_post_id>/delete', methods=['GET','POST'])
@login_required
def delete_post(blog_post_id):

    # Забор ЦИФРЫ ID из переданой в функцию переменной ( передаем  ОБЪЕКТЫ МОДЕЛИ из БД BlogPost())
    blog_post = BlogPost.query.get_or_404(blog_post_id)

    # !!! ВАЖНО !!! ПРОВЕРКА что ПОЛЬЗОВАТЕЛЬ и есть Автор поста (что бы кто угодно залогинивийся не мог УДАЛИТЬ чужой пост)!
    # if current_user.id == blog_post.user_id или второй вариант:
    if blog_post.author!= current_user:
        # Можно просто pass, + прописать все в HTML шаблорне что бы кнопка Delete просто ен показывалась при  {%if blog_post.author!= current_user %}
        abort(403)

    db.session.delete(blog_post)
    db.session.commit()
    flash('Post was Deleted!')

    return redirect(url_for('core.index'))
