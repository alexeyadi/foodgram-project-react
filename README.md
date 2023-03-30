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
- Установить docker-compose на сервер:
```bash
curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
```
- Локально отредактировать файл infra/nginx.conf, обязательно в строке server_name вписать IP-адрес сервера
- Скопировать файлы docker-compose.yml и nginx.conf из директории infra на сервер:
```bash
scp docker-compose.yml <username>@<host>:/home/<username>/docker-compose.yml
scp nginx.conf <username>@<host>:/home/<username>/nginx.conf
```
- Создать .env файл по предлагаемому выше шаблону. Обязательно изменить значения POSTGRES_USER и POSTGRES_PASSWORD
- Для работы с Workflow добавить в Secrets GitHub переменные окружения для работы:
    ```
    DB_ENGINE=<django.db.backends.postgresql>
    DB_NAME=<имя базы данных postgres>
    DB_USER=<пользователь бд>
    DB_PASSWORD=<пароль>
    DB_HOST=<db>
    DB_PORT=<5432>
    
    DOCKER_PASSWORD=<пароль от DockerHub>
    DOCKER_USERNAME=<имя пользователя>
    
    SECRET_KEY=<секретный ключ проекта django>
    USER=<username для подключения к серверу>
    HOST=<IP сервера>
    PASSPHRASE=<пароль для сервера, если он установлен>
    SSH_KEY=<ваш SSH ключ (для получения команда: cat ~/.ssh/id_rsa)>
    TELEGRAM_TO=<ID чата, в который придет сообщение>
    TELEGRAM_TOKEN=<токен вашего бота>
    ```
    Workflow состоит из четырёх шагов:
     - Проверка кода на соответствие PEP8
     - Сборка и публикация образа бекенда на DockerHub.
     - Автоматический деплой на удаленный сервер.
     - Отправка уведомления в телеграм-чат.
- собрать и запустить контейнеры на сервере:
```bash
docker-compose up -d --build
```
- После успешной сборки выполнить следующие действия (только при первом деплое):
    * провести миграции внутри контейнеров:
    ```bash
    docker-compose exec web python manage.py migrate
    ```
    * собрать статику проекта:
    ```bash
    docker-compose exec web python manage.py collectstatic --no-input
    ```  
    * Создать суперпользователя Django, после запроса от терминала ввести логин и пароль для суперпользователя:
    ```bash
    docker-compose exec web python manage.py createsuperuser
    ```
## Проверка работы сервера
Проверить работу сервера можно по IP: 158.160.28.232

### Команды для заполнения базы данных
Создать дамп базы данных:
```
sudo docker-compose exec web python manage.py dumpdata > fixtures.json
```
**Далее команды по востановлению базы данных из резервной копии.**
Узнаем CONTAINER ID для контейнера:
```
sudo docker container ls -a
```
Копируем файл с фикстурами в контейнер::
```
sudo docker cp fixtures.json <CONTAINER ID>:/app
```
Применяем фикстуры::
```
sudo docker-compose exec web python manage.py loaddata fixtures.json
```
Удаляем файл фикстуры из контейнера:
```
sudo docker exec -it <CONTAINER ID> bash
rm fixtures.json
exit
```


