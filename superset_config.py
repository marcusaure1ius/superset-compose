import os

# Получаем переменные из .env файла
POSTGRES_USER = os.environ["POSTGRES_USER"]
POSTGRES_PASSWORD = os.environ["POSTGRES_PASSWORD"]
POSTGRES_DB = os.environ["POSTGRES_DB"]
REDIS_PASSWORD = os.environ["REDIS_PASSWORD"]

# Секретный ключ
SECRET_KEY = os.environ["SUPERSET_SECRET_KEY"]

# Подключение к базе метаданных
# Приоритеты:
# 1) SUPERSET_SQLALCHEMY_DATABASE_URI (если задан) — используется как есть
# 2) METADATA_DB_MODE=prod — берём внешние параметры EXTERNAL_DB_*
# 3) Иначе dev — используем внутренний postgres из docker-compose (host: postgres)
_override_uri = os.getenv("SUPERSET_SQLALCHEMY_DATABASE_URI")
if _override_uri:
    SQLALCHEMY_DATABASE_URI = _override_uri
else:
    _mode = os.getenv("METADATA_DB_MODE", "dev").lower()
    if _mode == "prod":
        EXT_HOST = os.getenv("EXTERNAL_DB_HOST")
        EXT_PORT = os.getenv("EXTERNAL_DB_PORT", "5432")
        EXT_USER = os.getenv("EXTERNAL_DB_USER")
        EXT_PASSWORD = os.getenv("EXTERNAL_DB_PASSWORD")
        EXT_NAME = os.getenv("EXTERNAL_DB_NAME")
        # Если не хватает параметров — мягко откатываемся на dev-конфиг, чтобы не ронять приложение на старте
        if all([EXT_HOST, EXT_USER, EXT_PASSWORD, EXT_NAME]):
            SQLALCHEMY_DATABASE_URI = (
                f"postgresql+psycopg2://{EXT_USER}:{EXT_PASSWORD}@{EXT_HOST}:{EXT_PORT}/{EXT_NAME}"
            )
        else:
            # dev fallback (внутренний postgres)
            SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@postgres:5432/{POSTGRES_DB}"
    else:
        # dev (внутренний postgres)
        SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@postgres:5432/{POSTGRES_DB}"

# Настройки Redis
REDIS_HOST = "redis"
REDIS_PORT = 6379

# Кэш Superset
CACHE_CONFIG = {
    'CACHE_TYPE': 'RedisCache',
    'CACHE_DEFAULT_TIMEOUT': 300,
    'CACHE_KEY_PREFIX': 'superset_cache_',
    'CACHE_REDIS_URL': f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/1",
}

# Брокер Celery
class CeleryConfig:
    broker_url = f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/2"
    imports = ('superset.sql_lab', )
    result_backend = f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/3"
    worker_prefetch_multiplier = 1
    task_acks_late = False
    task_track_started = True

CELERY_CONFIG = CeleryConfig

# Включаем асинхронное выполнение запросов
FEATURE_FLAGS = {"ENABLE_TEMPLATE_PROCESSING": True}
ALERT_REPORTS = True


RATELIMIT_STORAGE_URI = f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/4"

# Локализация интерфейса
LANGUAGES = {
    'en': {'flag': 'us', 'name': 'English'},
    'ru': {'flag': 'ru', 'name': 'Русский'},
}

# Локаль по умолчанию
BABEL_DEFAULT_LOCALE = 'ru'