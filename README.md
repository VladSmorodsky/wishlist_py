# wishlist_py

It's a wish management project that provides:

- login and register user system
- friendship system
- manipulating own wishes
- discuss wishes with friends
- create and get your wishes using Telegram bot

Tech stack that used for this project: Django Rest Framework, Celery, Celery Beat, Redis, RabbitMQ, Telegram Bot API.

## Project setup

1. Clone the repo and go to the project root.
2. Go to wishlist_project directory:
   ```shell
   cd wishlist_project
   ```
3. Create `.env` file from `.env.example` and set values:
    - **`DJANGO_SECRET_KEY`**: Django secret key value
    - **`DJANGO_DEBUG`**: Django Debug value. Can be True or False.
    - **`ACCESS_TOKEN_TTL`**: JWT access token lifetime in number of minutes.
    - **`REFRESH_TOKEN_TTL`**: JWT refresh token lifetime in number of days.
    - **`POSTGRES_DB`**: database name.
    - **`POSTGRES_USER`**: database user.
    - **`POSTGRES_PASSWORD`**: database user password.
    - **`DB_HOST`**: database host.
    - **`DB_PORT`**: database port.
    - **`ALLOWED_HOST`**: list of available hosts. It should be string with comma separated values (e.g.
      `'test.com,test.domai.com'`).
    - **`CELERY_BROKER_URL`**: Celery broker url.
    - **`CHAT_BROKER_URL`**: Broker url for Websocket chat.
    - **`EMAIL_HOST`**: email host provider domain
    - **`EMAIL_PORT`**: email port
    - **`EMAIL_HOST_USER`**: host user's email
    - **`EMAIL_HOST_PASSWORD`**: host user's password
    - **`EMAIL_USE_TLS`**: use TLS connection (True or False)
    - **`DEFAULT_FROM_MAIL`**: define from what email messages will be sent by default
    - **`EMAIL_BACKEND`**: define django email backend to work with emails. Use next value for debug environment:
      `django.core.mail.backends.console.EmailBackend`

4. Go to `telegram_bot` directory:
     ```shell
     cd ../telegram_bot
     ```

5. Create `.env` file from `.env.example` and set values:
    - **`TELEGRAM_BOT_TOKEN`**: Telegram bot token
    - **`RABBITMQ_URL`**: connection string for RabbitMQ with next template: `amqp://<user>:<password>@<host>:<port>`

6. Run `docker-compose.yml` script:
     ```shell
     docker compose up --build -d
     ```
7. To create a superuser for entering into django admin, run the next command:
     ```shell
     docker compose run -it api make shell
     ```
   And then run python commands for creating a superuser:

    ```python
    from accounts.models import User
    
    user = User(email="<superuser_email>", is_staff=True, is_superuser=True)
    user.set_password("<superuser_password>")
    user.save()
    exit()
    ```

## Project structure

Project consists of Django Rest Framework application and Telegram bot application.

### wishlist_project Structure:

- **`accounts`**: API for user management application (register, login)
- **`celery_tasks`**: Project background tasks
- **`friendship`**: Friendship management system application (send a friend request, accept or reject it)
- **`wishlist_app`**: Wishlist management application
- **`ws_chat`**: Websocket chat
- **`tests`**: Project's tests
- **`wishlist_project`**: Main project directory with configurations
- **`rabbitmq`**: Message broker logic (publisher and consumer implementation)

### telegram_bot Structure:

- **`main.py`**: Main application file where commands registered
- **`handlers.py`**: Bot event handlers
- **`rabbitmq`**: Message broker logic (publisher and consumer implementation)