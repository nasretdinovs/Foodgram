![workflow](https://github.com/nasretdinovs/foodgram-project-react/actions/workflows/main.yml/badge.svg)
[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)

# FOODGRAM

«Продуктовый помощник» — онлайн-сервис с API. На котором пользователи могут:
публиковать рецепты, подписываться на публикации,
добавлять рецепты в список «Избранное», скачивать список продуктов,
необходимых для приготовления одного или нескольких выбранных блюд.

## Технологии

Приложение работает на
- [Django 2.2](https://www.djangoproject.com/download/)
- [Django REST Framework 3.12](https://www.django-rest-framework.org/#installation).
- [Simple JWT](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/).

# Установка
## Secrets for Actions:

- DB_ENGINE — указываем систему управления базами данных
- DB_HOST — название сервиса (контейнера)
- DB_NAME — имя базы данных
- DB_PORT — порт для подключения к БД
- DOCKER_PASSWORD — пароль от hub.docker.com
- DOCKER_USERNAME — логин от hub.docker.com
- HOST — публичный IP-адрес сервера
- PASSPHRASE — для подключения к серверу по SSH
- POSTGRES_PASSWORD — пароль для подключения к БД
- POSTGRES_USER — логин для подключения к базе данных
- SSH_KEY — приватный ключ с компьютера, имеющего доступ к боевому серверу [cat ~/.ssh/id_rsa]
- TELEGRAM_TO — ID своего телеграм-аккаунта
- TELEGRAM_TOKEN — токен бота
- USER — имя пользователя для подключения к серверу

## Команды:
После разворачивания надо выполнить команды по очереди на удаленном сервере:
```
sudo docker compose exec backend python manage.py add_ingredients #добавляет ингредиенты в базу
sudo docker compose exec backend python manage.py add_tags #добавляет теги по умолчанию в базу
sudo docker compose exec backend python manage.py createsuperuser
```

## Разработчики

Проект разработан
- [Виталий Насретдинов](https://github.com/nasretdinovs)

## Адрес сервера:
http://51.250.110.95/
- Логин админки: admin
- Пароль админки: Yandex2022

## License
[MIT](https://choosealicense.com/licenses/mit/)
