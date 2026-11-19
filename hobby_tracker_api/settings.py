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
    var = "HS256"
AUTH_ALGORITHM = var

if (var := os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")) is None:
    var = "30"
ACCESS_TOKEN_EXPIRE_MINUTES = int(var)

if (var := os.getenv("REFRESH_TOKEN_EXPIRE_DAYS")) is None:
    var = "30"
REFRESH_TOKEN_EXPIRE_DAYS = int(var)

if (var := os.getenv("REFRESH_TOKEN_BYTES")) is None:
    var = "32"
REFRESH_TOKEN_BYTES = int(var)
