import os

from dotenv import load_dotenv


class SettingsException(Exception):
    pass


class RequiredENV(Exception):
    pass


load_dotenv()


if (var := os.getenv("DATABASE_URL")) is None:
    raise RequiredENV("env DATABASE_URL is required")
DATABASE_URL = var

if (var := os.getenv("AUTH_SECRET_KEY")) is None:
    raise RequiredENV("env AUTH_SECRET_KEY is required")
AUTH_SECRET_KEY = var

if (var := os.getenv("AUTH_ALGORITHM")) is None:
    AUTH_ALGORITHM = "HS256"
else:
    AUTH_ALGORITHM = var

if (var := os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")) is None:
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
else:
    ACCESS_TOKEN_EXPIRE_MINUTES = int(var)

if (var := os.getenv("REFRESH_TOKEN_EXPIRE_DAYS")) is None:
    REFRESH_TOKEN_EXPIRE_DAYS = 30
else:
    REFRESH_TOKEN_EXPIRE_DAYS = int(var)

if (var := os.getenv("REFRESH_TOKEN_BYTES")) is None:
    REFRESH_TOKEN_BYTES = 32
else:
    REFRESH_TOKEN_BYTES = int(var)
