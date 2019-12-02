# core/views.py

npf = 'I am here!'

from flask import render_template, request, url_for, Blueprint

#Загрузка МОДЕЛЬ
from puppycompanyblog.models import BlogPost


# Создаем Блюпринт CORE
core = Blueprint('core',__name__)
#template_folder='some_path' - НЕУКАЗАННО путь к Шаблонам которые будет обрабатывать данный модуль ( куда обращаются ДЕКОРАТОРЫ через
# return render_template())       - Если не указать то по умолчанию берется папка template лежащая в папке С !ЯДРОМ! - старшим __init__.py файлом проекта




@core.route('/')
def index():

    # Простой способ передать все посты blog_posts = BlogPost.query.all(), но это херовое решение если постов много,
    # так что надо разбить на страницы (paginate())

# ПАГИНАЦИЯ (разбивка) постов ПО СТРАНИЦАМ
    # blog_posts = BlogPost.query.paginate() - создает ОБЪЕКТ Пагинации ( разбивку) выдаст на странице первые 20 объектов из БД
    # dir(blog_posts) - покажет все методы и атрибуты Обекта ( вызываются либо через paginate(...=...) либо через blog_posts.total\page\items и т.д.
    # has_next, has_prev, items, page, per_page, total - основные методы для работы
    # items - элементы которые будут отображаться на странице ( в нашем случае посты)
    # page - текущая страница ( по умолчанию 1)
    # per_page - сколько айтемов  будет на 1 странице ( по умолчанию 20)
    # total - сколько всего элементов (items) в выборке для которой делается пагинация ( тоесть сколько всего постов в blog_posts= BlogPost.query.paginate())
    # ДОПОЛНИТЕЛЬНО : blog_posts = BlogPost.query.paginate(page=2)- выведет объекты взятые из БД оказавшиеся на второй странице ( с 21 по 40)

# Забор ТЕКУЩЕЙ СТРАНИЦЫ из URL. - ТОЕСТЬ заберается параметр из АДРЕСНОЙ СТРОКИ, и переносится в пагинацию(что бы правилно нумеровались кнопки страниц).
    # request.args.get - ЗАПРОС метода get() для MultiDict - get(key, default=None, type=None))
    # МУЛЬТИСЛОВАРЬ  - https://werkzeug.palletsprojects.com/en/0.15.x/datastructures/#werkzeug.datastructures.MultiDict.get
    #ЗАПРОС элементов словаря по КЛЮЧУ 'page' с порядковым знаком начинающимся с 1, и элемент перечисления должен быть ЧИСЛОМ
    # 'page' - ключ словаря создания страниц
    # ,1, - страницыа которая будет выводиться при образщении. НЕ наименование а Именно СТРАНИЦА, тоесть если указакть 2, то будет перенаправлять на 2,
    #  --- а на 1 уже придется переключится самомоу
    # type=int - тип передаваемых в запрос даненых, номера страницы.
    page = request.args.get('page',1,type=int)

    # Добавляем очередь(query) из МОДЕЛИ BlogPost - Поиск ВСЕХ ПОСТОВ
    # .order_by(BlogPost.date.desc()) - вывод списка постов в убывающем порядке от последнего к первому
    # --- order_by - ДОПОЛНИТЕЛЬНЫЙ критерий вывода запроса
    # --- desc() - Для того чтобы сортировка производилась в обратном порядке, в утверждении ORDER BY к имени заданного столбца, в котором
    # --- * производится сортировка, следует добавить, принцип сортировки- ДАТУ(date), и  ключевое слово DESC (убывающий).
    # .paginate(page=page,per_page=5) - СЛОВАРЬ ПАГИНАЦИИ разбивка на страницы. ИМЕНО по этому используется ЗАПРОС ИЗ СЛОВАРЯ page = request.args.get('page',1,type=int)
    # --- Метод paginate вызывается на любом объекте query. Он принимает ТРИ аргумента:
    # --- page=         - Номер страницы, начиная с 1
    # --- per_page=     - количество элементов на страницу,
    # --- False\True    - флаг error. Если флаг выставлен в True, когда происходит выход за пределы списка, клиенту возвращается ошибка 404.
    # В противном случает будет возвращен пустой список вместо ошибки ( по умолчанию False).
    blog_posts = BlogPost.query.order_by(BlogPost.date.desc()).paginate(page=page, per_page=2)
    # Метод paginate возвращает объект Pagination. Члены этого объекта содержат список элементов запрошеной страницы.


    return render_template('index.html',blog_posts=blog_posts)

def url_for_other_page(page):
    args = request.view_args.copy()
    args['page'] = page
    return url_for(request.endpoint, **args)
#app.jinja_env.globals['url_for_other_page'] = url_for_other_page   # # Регистрация Глобальной переменной Пагинации для Jinja2  в ЯДРЕ

@core.route('/info')
def info():
    return render_template('info.html')
