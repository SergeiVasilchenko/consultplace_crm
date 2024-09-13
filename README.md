# Deploy the Project on a Remote Server

## Preparation

1. **Create environment variable files in your git repository:**

    - Create a file for the bot (or just skip this step as the deploy step will create and write all the files needed):
      ```bash
      touch bot/.env_bot
      ```
      with the following variables:
      ```env
      BOT_TOKEN=<your value>
      REDIS_HOST=<your remote server IP>
      REDIS_PORT=6379
      REDIS_DB=2
      ```

    - Create a file for the application (or just skip this step as the deploy step will create and write all the files needed):
      ```bash
      touch consultplsce/.env
      ```
      with the following variables:
      ```env
      BOT_TOKEN=<your value>
      SECRET_KEY=<django project secret key>
      POSTGRES_DB=<your value>
      POSTGRES_PASSWORD=<your value>
      POSTGRES_USER=<your value>
      DB_HOST=db  # (must match the database container name)
      DB_PORT=5432
      CELERY_BROKER_URL=redis://<your remote server IP>:6379/1
      CELERY_RESULT_BACKEND=redis://<your remote server IP>:6379/1
      ```

2. **Add secrets to the git repository:**

   The following Git Actions secrets must be specified **Settings > Secrets and variables > Actions** for your repository (do this step anyway despite skipping the Step 1 above):
   - `BOT_TOKEN`
   - `SECRET_KEY`
   - `POSTGRES_DB`
   - `POSTGRES_PASSWORD`
   - `POSTGRES_USER`
   - `DB_HOST`
   - `CELERY_BROKER_URL`
   - `CELERY_RESULT_BACKEND`
   - `REDIS_HOST`
   - `REDIS_PORT`
   - `REDIS_DB`
   - `DOCKER_USERNAME`
   - `DOCKER_PASSWORD_SSH`
   - `HOST`
   - `USER`
   - `SSH_KEY`
   - `SSH_PASSPHRASE`

3. **Server connection:**
   - Git must be installed on the remote server, and the server must be connected via SSH to the repository.

4. **Install Redis on the server:**
   - Redis should be installed on the remote server and configured to listen on the default port (6379).

5. **Check the repository branch:**
   - Ensure that the correct branch of the repository for deployment is specified in `main.yml`.

6. **Configure DockerHub repositories:**
   - In the `docker-compose` files, for the `image:` directive, specify the DockerHub repositories you have read and write access to:
     - `<your dockerhub username>/crm_leo-backend:latest`
     - `<your dockerhub username>/crm_leo-bot:latest`
     - `<your dockerhub username>/crm_leo-nginx:latest`

     **Important:** Double-check that all `image:` references in `docker-compose.production.yml` point to your repository username.

## Launch

- **From the local machine:**
  ```bash
  git push

**DEV youstras workflow**
   - Will run tests.
   - Will rebuild DockerHub images for the containers and push them to the DockerHub repositories.
   - During deployment, it will `copy docker-compose.production.yml`, recreate the `.env` files, and run daemonized docker compose.

# Описание проекта
Это - MVP-версия для проекта платформы на Django с интеграцией пользовательского интерфейса через телеграм бот. В данной версии подключена админ-панель. Реализован API. Работают сигналы Джанго и подключены асинхронные задачи Celery на Redis. Регистрация пользователя через телеграм бот. Сервис представляет гибрид финконсалтинга и образовательного ресурса.
Сценарий пользователя
Пользователь регистрируется через телеграм бот. В базе данных создается сущность. Для этого объекта рандомно назначается тестовое задание по финконсалтингу и дается несколько дней для его выполнения. За сутки до дедлайна пользователь (если необходимо) получает напоминание в телеграм бот о дедлайне. Пользователь посылает тестовое задание ссылкой на файл. Авторизованные пользователи проверяют это задание и предлагают испытуемому занять одну из 3 позиций (Студент, Стажер или Аналитик). В зависимости от назначенной должности предполатается разный сценарий поведения пользователя на ресурсе. Студенту предлагается освоить курс по финконсалтингу. Стажер участвует в аналитике на безвозмездной основе. Аналитик участвует в Проекте за деньги.
Админ создает Проект и по своим критериям оценки приглашает в него исполнителей. Исполнителю приходит уведомление в телеграм бот о приглашении в Проект, которое он должен в какой-то срок подтвердить или отказаться от приглашения. Для этого есть дедлайн и уведомление о нем.
Проект делится на Задачи. Принцип уведомления о постановке Задачи - тот же. Выполненная задача проверяется и оценивается системой баллов.
Совокупно оценки по задачам определяет общий рейтинг. Он подсчитывается автоматически.

# Развернуть проект на удаленном сервере

## Подготовка

1. **Создайте файлы переменных окружения в репозитории git:**

    - Создайте файл для бота:
      ```bash
      touch bot/.env_bot
      ```
      с переменными:
      ```env
      BOT_TOKEN=<your value>
      REDIS_HOST=<ip вашего удаленного сервера>
      REDIS_PORT=6379
      REDIS_DB=2
      ```

    - Создайте файл для приложения:
      ```bash
      touch consultplsce/.env
      ```
      с переменными:
      ```env
      BOT_TOKEN=<your value>
      SECRET_KEY=<django project secret key>
      POSTGRES_DB=<your value>
      POSTGRES_PASSWORD=<your value>
      POSTGRES_USER=<your value>
      DB_HOST=db  # (должен совпадать с именем контейнера базы данных)
      DB_PORT=5432
      CELERY_BROKER_URL=redis://<ip вашего удаленного сервера>:6379/1
      CELERY_RESULT_BACKEND=redis://<ip вашего удаленного сервера>:6379/1
      ```

2. **Добавьте секреты в репозиторий git:**

   В разделе **Settings > Secrets and variables > Actions** для репозитория должны быть указаны следующие секреты:
   - `BOT_TOKEN`
   - `SECRET_KEY`
   - `POSTGRES_DB`
   - `POSTGRES_PASSWORD`
   - `POSTGRES_USER`
   - `DB_HOST`
   - `CELERY_BROKER_URL`
   - `CELERY_RESULT_BACKEND`
   - `REDIS_HOST`
   - `REDIS_PORT`
   - `REDIS_DB`

3. **Подключение к серверу:**
   - На удаленном сервере должен быть установлен Git и настроено SSH-подключение к репозиторию.

4. **Установка Redis на сервере:**
   - На удаленном сервере должен быть установлен Redis и настроен на прослушивание порта по умолчанию (6379).

5. **Проверьте ветку репозитория:**
   - Убедитесь, что в `main.yml` указана корректная ветка репозитория, с которой будет происходить деплой.

6. **Настройка DockerHub репозиториев:**
   - В файлах `docker-compose` для директивы `image:` укажите репозитории DockerHub, к которым у вас есть доступ на чтение и запись:
     - `<your dockerhub username>/crm_leo-backend:latest`
     - `<your dockerhub username>/crm_leo-bot:latest`
     - `<your dockerhub username>/crm_leo-nginx:latest`

     **Важно:** дважды проверьте, что все `image:` ссылаются на ваш репозиторий.

## Запуск

- **С локальной машины:**
  ```bash
  git push

**DEV youstras workflow**
   - запустит тесты
   - пересоберет оразы dockerhub для контейнеров и отправит их в репозитории dockerhub
   - во время деплоя скопирует `docker-compose.production.yml`, пересоздаст `.env` файлы и запустит docker-compose в режиме демона


# consultplace_crm!!!

Развернуть проект на удаленном сервере
Подготовка
    1. Создайте файлы переменных окружения в репозитории git
        touch bot/.env_bot
            с переменными:
                BOT_TOKEN=<your value>
                REDIS_HOST= ip вашего удаленного сервера
                REDIS_PORT=6379
                REDIS_DB=2
        touch consultplsce/.env
            с переменными:
                BOT_TOKEN=<your value>
                SECRET_KEY=<django project secret key>
                POSTGRES_DB=<your value>
                POSTGRES_PASSWORD=<your value>
                POSTGRES_USER=<your value>
                DB_HOST=db (должен совпадать с именем контейнера базы данных)
                DB_PORT=5432
                CELERY_BROKER_URL=redis://<ip вашего удаленного сервера>:6379/1
                CELERY_RESULT_BACKEND=redis://<ip вашего удаленного сервера>:6379/1
    2. В Settings > Secrets and variables > Actions для данного репозитория git должны быть указаны секреты:
        BOT_TOKEN
        SECRET_KEY
        POSTGRES_DB
        POSTGRES_PASSWORD
        POSTGRES_USER
        DB_HOST
        CELERY_BROKER_URL
        CELERY_RESULT_BACKEND
        REDIS_HOST
        REDIS_PORT
        REDIS_DB
    3. На удаленном сервере установлен Git и сервер подключен к нему через SSH
    4. На удаленном сервере установлен Redis и слушает порт по умолчанию (6379)
    5. В main.yml указана корректная ветка репозитория, с которого должен быть произведен деплой
    6. В docker-compose файлах для директивы
        image:
       указаны репозитории DockerHub, к которым вы имеете доступ на чтение и запись (соответственно приведенные в docker-compose файлах примеры следует заменить на удаленные образа собственной сборки). Это необходимо потому что автомитизация после отправки обновленного кода на github пересобирает образы и пытается перезаписать соответствующий репозиторий dockerhub, но у вас для этого нет прав. Следовательно, нужно пересобрать образа контейнеров и указать для них свой собственный репозиторий:
        <your dockerhub usernane>/crm_leo-backend:latest
        <your dockerhub usernane>/crm_leo-bot:latest
        <your dockerhub usernane>/crm_leo-nginx:latest
      (дважды проверьте что все image: ссылаются на ваш репозиторий)

Запуск
    С локальной машины:
        git push
    (при условии что сервер видит репозиторий git, в main.yml указаны команды, нужные для запуска)
    Воркфлоу git actions
        запустит тесты
        пересоберет оразы dockerhub для контейнеров и отправит их в репозитории dockerhub
        во время деплоя скопирует docker-compose.production.yml, пересоздаст .env файлы и запустит docker-compose в режиме демона
