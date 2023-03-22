# Дипломный проект Foodgram
![status workflow](https://github.com/alexeyadi/foodgram-project-react/actions/workflows/yamdb_workflow.yml/badge.svg)

## Стек технологий используемый в проекте:
* Python - 3.7

```
https://www.python.org/
```

* Django  - 2.2.19

```
https://www.djangoproject.com/
```

* Django Rest Framework - 3.12.4

```
https://www.django-rest-framework.org/
```

* Simple JWT - 5.2.2

```
https://django-rest-framework-simplejwt.readthedocs.io/en/latest/
```

* Django Filter - 21.1

```
https://www.django-rest-framework.org/api-guide/filtering/#setting-filter-backends
```

* Docker

```
https://docs.docker.com/engine/install/
```

## Как запустить проект:
Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:alexeyadi/foodgram-project-react.git
```

```
cd foodgram-project-react
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

```
source env/bin/activate
```

```
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```

```

