# users/pictures_handler.py

import os

# Библиотека обрабатывающая загрузку картинок
from  PIL import Image

# current_app - используется что бы указать на ЯДРО программы ( или указать ыбстро путь к каталогу где ядро лежит через import os)
from flask import url_for, current_app

# Создаем функциию которую будем передаать во VIEWS
def add_profile_pic(pic_upload,username):

    # Загрузка файла ( картинка которую выбирает пользователь для загрузки - filename)
    filename = pic_upload.filename

    # Выбор типа расширения extension type-  выбираем файл загружаемый пользователем, делим его имя на 2 части через точку, и берем САМУЮ посдледнюю часть
    # Тоесть в файле "lolo.hu.gara.jpg" будет взято только jpg
    ext_type = filename.split('.')[-1]

    # Создание НА СЕРВЕРЕ имени загружаемому пользователю файлу
    # Берется имя пользователя, к нему добаляется точка и расширение загружаемого им файла (username.jpg) А можно ХЭШИРОВАТЬ для безопастности пользователя
    storage_filename = str(username) + '.' +ext_type

    # Сохравнение файла на сервере - 1) Путь к КОРНЕВОЙ ПАПКЕ  Приложения 2) Указывается путь 3) Имя под которым сохраняется загружаемый файл
    filepath = os.path.join(current_app.root_path, 'static\profile_pics', storage_filename)

    # Проверка размера аватара в пиксилях
    output_size = (200, 200)

    # Обработка загруженного Аватара ( что бы все были одинаковыми)
    # Открытия загруженной картинки
    pic = Image.open(pic_upload)
    # Сжатие картинки до размеров разрешенных нами
    pic.thumbnail(output_size)
    # Сохранение получившегося изображения
    pic.save(filepath)

    # Возвращаем имя файла для испорльзования в коде ( к примеру username.png)
    return storage_filename

