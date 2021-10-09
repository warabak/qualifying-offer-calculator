from logging.config import dictConfig

from dotenv import load_dotenv
from flask import Flask
from flask.logging import default_handler
from werkzeug.middleware.proxy_fix import ProxyFix


def create_app() -> Flask:
    load_dotenv()

    # Differ import until we've loaded dotenv
    from calculator import config
    dictConfig(_get_dict_logger_config(config.LOG_LEVEL))

    app = Flask(__name__, instance_relative_config=False)
    app.logger.removeHandler(default_handler)
    app.wsgi_app = ProxyFix(app.wsgi_app)
    app.logger.info(f"Initializing Flask application with log level = [{config.LOG_LEVEL}]")

    from calculator.players.players import api_bp
    app.register_blueprint(api_bp)

    # https://flask.palletsprojects.com/en/2.0.x/templating/#registering-filters
    from calculator.utils import format_currency
    app.jinja_env.filters["format_currency"] = format_currency

    return app


def _get_dict_logger_config(log_level):
    return {
        "version": 1,
        "disable_existing_loggers": True,
        "formatters": {
            "flask": {
                "format": "[%(asctime)s] | %(levelname)s | %(module)s:%(lineno)d | %(message)s",
            },
        },
        "handlers": {
            "flask": {
                "level": "INFO",
                "class": "logging.StreamHandler",
                "stream": "ext://flask.logging.wsgi_errors_stream",
                "formatter": "flask",
            },
        },
        "loggers": {
            "": {"level": "INFO", "handlers": ["flask"], "propagate": False},
            "calculator": {
                "level": log_level,
                "handlers": ["flask"],
                "propagate": False,
            },
        },
    }
