# Как заставить всё работать:
- Убедиться, что у вас стоит Django 1.5.4
- В *settings.py* закомментировать строки, относящиеся к postgres, раскомментировать sqlite
- В *Tools > Run manage.py task* запустить команду *syncdb*
- Там же запустить *loaddata* с параметром *all1.json*
- Подождать, пока всё влезет в базу
- Там же запустить *runserver*
- Пойти в браузер на **127.0.0.1:8000**