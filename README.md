# Project Overview
This is the MVP version of a platform built with Django, featuring a user interface integrated with a Telegram bot. It includes an admin panel, a fully functional API, Django signals, and asynchronous task handling using Celery with Redis. User registration is done through the Telegram bot. The service combines financial consulting with educational resources.

## Features
- **Telegram Bot Integration**: Users interact with the platform directly through a Telegram bot.
- **Django Admin Panel**: Provides an admin interface for managing users, projects, and tasks.
- **API**: Offers API endpoints for various platform functionalities.
- **Celery Tasks**: Supports asynchronous task processing using Celery, with Redis as the message broker.
- **User Registration**: Users register via the Telegram bot, receive tasks, project invitations, and more.
- **Notification System**: Sends reminders and notifications via Telegram for tasks, deadlines, and project updates.

## User Scenario
- Users register through the Telegram bot, which creates a record in the database.
- A random financial consulting test task is assigned to the user with a set deadline for completion.
- If necessary, the user receives a reminder via the Telegram bot 24 hours before the deadline.
- The user submits the completed task by sharing a file link.
- Authorized users review the submission and offer the user one of three roles:
  - **Student**: Engages in a financial consulting course.
  - **Intern**: Contributes to analytics work on a voluntary basis.
  - **Analyst**: Takes part in paid projects.

## Admin Workflow
- Admins create projects and invite selected users based on certain assessment criteria.
- Participants receive an invitation via the Telegram bot, which they must accept or decline within a set time. Reminders are sent if deadlines approach.
- Projects are divided into tasks, with task notifications following the same structure as project invitations.
- Completed tasks are reviewed and scored based on a points system. The total score determines the participant’s overall rating, which is automatically calculated.

## Project Structure
- **Projects**: Created by admins, with specific tasks and deadlines assigned to participants.
- **Tasks**: Subdivisions of a project, assigned to users based on their roles (Student, Intern, Analyst).
- **Ratings**: Participants are evaluated based on task performance, and their overall score determines their ranking on the platform.

## Installation
See `Deploy the Project on a Remote Server` section


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

7. **Use your own domain name**
   - Change `consultplacetest.sytes.net` to your own domain in all the configuration files.

## Launch

- **From the local machine:**
  ```bash
  git push

**DEV youstras workflow**
   - Will run tests.
   - Will rebuild DockerHub images for the containers and push them to the DockerHub repositories.
   - During deployment, it will `copy docker-compose.production.yml`, recreate the `.env` files, and run daemonized docker compose.


# Описание проекта
Это MVP-версия платформы, разработанной на Django с интеграцией пользовательского интерфейса через телеграм-бота. В данной версии подключена админ-панель, реализован API, работают сигналы Django и подключены асинхронные задачи с использованием Celery на базе Redis. Регистрация пользователя происходит через телеграм-бота. Сервис представляет собой гибрид финансового консалтинга и образовательного ресурса.

## Возможности
- **Интеграция с Telegram ботом**: Пользователи взаимодействуют с платформой через Telegram.
- **Админ-панель Django**: Интерфейс для администрирования пользователей, проектов и задач.
- **API**: Реализованы API-эндпоинты для взаимодействия с платформой.
- **Асинхронные задачи**: Обработка фоновых задач с использованием Celery и Redis.
- **Регистрация пользователей**: Регистрация через телеграм-бот с последующей выдачей задач и приглашений.
- **Система уведомлений**: Напоминания и уведомления о задачах и дедлайнах через Telegram.

## Сценарий пользователя
- Пользователь регистрируется через телеграм-бот, и для него создается объект в базе данных.
- Объекту случайным образом назначается тестовое задание по финансовому консалтингу с установленным сроком выполнения.
- За сутки до дедлайна (при необходимости) пользователь получает напоминание через телеграм-бот.
- Пользователь отправляет ссылку на файл с выполненным тестовым заданием.
- Авторизованные пользователи проверяют задание и предлагают одну из трех должностей:
  - **Студент**: Проходит курс по финансовому консалтингу.
  - **Стажер**: Участвует в аналитической работе на добровольной основе.
  - **Аналитик**: Участвует в проектах за вознаграждение.

## Рабочий процесс администратора
- Администраторы создают проекты и приглашают выбранных пользователей (на основании оценки) в качестве исполнителей.
- Исполнители получают приглашение в проект через телеграм-бот с установленным сроком для принятия решения. Если они не ответят вовремя, приходит напоминание о дедлайне.
- Проект делится на задачи. Принцип уведомления при назначении задач такой же, как и для приглашения в проект.
- Выполненные задачи проверяются и оцениваются системой баллов. Суммарная оценка задач определяет общий рейтинг пользователя, который подсчитывается автоматически.

## Структура проекта
- **Проекты**: Создаются администраторами и содержат задачи с установленными дедлайнами.
- **Задачи**: Подразделения проектов, которые назначаются пользователям в зависимости от их роли (Студент, Стажер, Аналитик).
- **Рейтинги**: Оценки пользователей за выполнение задач формируют их общий рейтинг на платформе.

## Установка
См. раздел `Развернуть проект на удаленном сервере`


# Развернуть проект на удаленном сервере

## Подготовка

1. **Создайте файлы переменных окружения в репозитории git:**

    - Создайте файл для бота (или пропустите этот шаг: все нужные файлы будут созданы автоматически при деплое):
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

    - Создайте файл для приложения (или пропустите этот шаг: все нужные файлы будут созданы автоматически при деплое):
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
