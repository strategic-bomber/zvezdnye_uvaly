ЗАПУСК СЕРВЕРА
1) Переходим в директорию backend и устанавливаем req.txt:

cd backend

-m pip install -r req.txt

python manage.py migrate

3) Запускаем сервер:
python manage.py runserver

4) Переходим по ссылке http://127.0.0.1:8000/


USER EXPERIENCE
1) Нажимаем "пройти опрос"
2) Заполняем форму (или пропускаем)
3) Выбираем точку на карте, затем выбираем объект справа в рамках указанного бюджета (можно кликнуть на объект справа, чтобы вылезла картинка)
4) Сохраняем свой выбор


АДМИН ПАНЕЛЬ

Чтобы попасть в админ панель, добавляем /admin в адресной строке

Логин и пароль: user@username.ru

Здесь можно добавлять опросы, объекты, указывать бюджет

Имеется возможность сделать выгрузку статистики в формате csv (пока готова только одна выгрузка для примера)

Для того чтобы выгрузить количество выбранных объектов:
1) В админ панели переходим в "Опросы"
2) Выбираем сверху действие "Выгрузить количество выбранных объектов"
3) Ставим галочку на опросе
4) Нажимаем "Go"
