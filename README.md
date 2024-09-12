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
