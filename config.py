# Module imports
from logging.config import dictConfig
from pydantic_settings import BaseSettings, SettingsConfigDict
import logging


class Settings(BaseSettings):
    # General settings
    APP_TITLE: str
    APP_SUMMARY: str
    APP_VERSION: str
    APP_RELOAD: bool
    APP_ORIGINS: list

    # Logging Settings
    LOG_LEVEL_WATCHFILES: str
    LOG_LEVEL_UVICORN: str
    LOG_LEVEL_DOCKERLINK: str

    # Authentication Settings
    AUTH_KEY: str

    # Docker Settings
    DOCKER_SOCKET_ENDPOINT: str

    # Specify env file
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()

# Logging
# Define ANSI escape sequences for colors
LOG_COLORS = {
    logging.DEBUG: "\033[94m",    # Blue
    logging.INFO: "\033[92m",     # Green
    logging.WARNING: "\033[93m",  # Yellow
    logging.ERROR: "\033[91m",    # Red
    logging.CRITICAL: "\033[31m", # Maroon
}

RESET_COLOR = "\033[0m"

# Custom Formatter to colorize [levelname]
class ColorFormatter(logging.Formatter):
    def format(self, record):
        # Get color from dictionary
        log_color: str = LOG_COLORS.get(record.levelno, RESET_COLOR)

        # Apply and return formatting
        record.levelname = f"{log_color}[{record.levelname}]{RESET_COLOR}"
        return super().format(record)

# Log config
log_config = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            '()': ColorFormatter,
            'fmt': '\033[90m{asctime} \033[34m{levelname} \x1b[38;5;98m[{name}]\033[97m: {message}\033[0m',
            'datefmt': '%Y-%m-%d %H:%M:%S',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'logfile': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/application.log',
            'backupCount': 5,
            'maxBytes': 10000000,
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
        'formatter': 'verbose',
    },
    'loggers': {
        'watchfiles': {
            'handlers': ['console', 'logfile'],
            'level': settings.LOG_LEVEL_WATCHFILES,
            'propagate': False,
        },
        'uvicorn': {
            'handlers': ['console', 'logfile'],
            'level': settings.LOG_LEVEL_UVICORN,
            'propagate': False,
        },
        'dockerlink': {
            'handlers': ['console', 'logfile'],
            'level': settings.LOG_LEVEL_DOCKERLINK,
            'propagate': False,
        },
    },
}
dictConfig(log_config)
