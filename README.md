# Установка Superset

Особенности:

* Режим установки - Docker Compose с поддержкой dev/prod окружений
* Dockerfile для сборки образа на базе Apache Superset 5.0.0
* Поддержка внешней PostgreSQL для production развертывания
* Celery для асинхронных задач
* Flower для мониторинга Celery задач
* Redis для кэширования и брокера сообщений

### Сервисы

* `postgres` (только в dev режиме) - PostgreSQL база данных для метаданных
* `redis` - Redis для кэша и Celery брокера
* `superset-init` - контейнер, который запускается один раз для инициализации базы данных и создания администратора
* `superset-app` - Web UI
* `superset-worker` - Celery worker для асинхронных задач
* `superset-beat` - Celery beat для периодических задач
* `flower` - Web UI для мониторинга Celery

### Установка

1. Клонируйте репозиторий и перейдите в папку с проектом

```bash
git clone https://github.com/marcusaure1ius/superset-compose.git
```

2. Создайте файл `.env` на основе следующего шаблона:

**Для dev режима (с внутренней PostgreSQL):**
```env
# Пароль для PostgreSQL
POSTGRES_USER=superset
POSTGRES_PASSWORD=superset
POSTGRES_DB=superset

# Пароль для Redis
REDIS_PASSWORD=redis

# Учетные данные администратора Superset
SUPERSET_ADMIN_USERNAME=admin
SUPERSET_ADMIN_PASSWORD=admin
SUPERSET_ADMIN_EMAIL=admin@example.com

# Секретный ключ Superset
SUPERSET_SECRET_KEY=your-secret-key-here

# Режим работы БД (dev или prod)
METADATA_DB_MODE=dev
```

**Для prod режима (с внешней PostgreSQL):**
```env
# Пароль для Redis
REDIS_PASSWORD=redis

# Учетные данные администратора Superset
SUPERSET_ADMIN_USERNAME=admin
SUPERSET_ADMIN_PASSWORD=admin
SUPERSET_ADMIN_EMAIL=admin@example.com

# Секретный ключ Superset
SUPERSET_SECRET_KEY=your-secret-key-here

# Режим работы БД
METADATA_DB_MODE=prod

# Параметры внешней БД
EXTERNAL_DB_HOST=your-postgres-host
EXTERNAL_DB_PORT=5432
EXTERNAL_DB_USER=superset_user
EXTERNAL_DB_PASSWORD=superset_password
EXTERNAL_DB_NAME=superset_db

# Или можно указать полный URI напрямую:
# SUPERSET_SQLALCHEMY_DATABASE_URI=postgresql+psycopg2://user:pass@host:5432/dbname
```

3. Опционально. В файл `requirements.txt` можно внести необходимые библиотеки, которые будут установлены во время развертывания Superset.

4. Сделайте исполняемым файл `compose.sh`, который автоматически выберет нужный docker-compose файл (dev или prod) на основе переменной `METADATA_DB_MODE`:

```bash
chmod +x compose.sh
```

5. Запустите контейнеры:

```bash
./compose.sh up -d
```

> **Important**
> 
> Скрипт `compose.sh` автоматически выбирает `docker-compose-dev.yml` (с PostgreSQL) или `docker-compose-prod.yml` (без PostgreSQL) на основе переменной `METADATA_DB_MODE` из `.env` файла.
> 
> В случае, если вам необходимо, например, добавить новые библиотеки и сделать новый билд, выполните команду `./compose.sh down && ./compose.sh up --build -d`

### Использование

После запуска контейнеров дождитесь завершения инициализации (контейнер `superset-init` должен завершиться успешно), затем перейдите по адресу `http://YOUR_HOST:8088` и используйте логин и пароль из файла `.env`.

Для доступа к Flower (мониторинг Celery) используйте адрес `http://YOUR_HOST:5555` (логин/пароль: `admin/admin`).

### Референсы

* [Apache Superset Documentation](https://superset.apache.org/docs/)
* [Superset GitHub](https://github.com/apache/superset)
* [Docker Compose Documentation](https://docs.docker.com/compose/)

##### Автор - [marcusaure1ius](https://github.com/marcusaure1ius)