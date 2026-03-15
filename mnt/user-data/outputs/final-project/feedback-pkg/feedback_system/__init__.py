"""
feedback_system
~~~~~~~~~~~~~~~
A plug-and-play Student Feedback web application built with Flask.

Basic usage:
    from feedback_system import create_app
    app = create_app()
    app.run()

Custom config:
    from feedback_system import create_app
    from feedback_system.config import Config

    class MyConfig(Config):
        DB_PATH    = '/var/data/feedback.db'
        SECRET_KEY = 'super-secret-key'
        APP_NAME   = 'My University Feedback'

    app = create_app(config=MyConfig)

String shortcuts:
    app = create_app(config='production')
    app = create_app(config='development')
    app = create_app(config='testing')
"""

from flask import Flask
from .config import Config, config_map
from .database import init_db
from .routes import feedback_bp

__version__ = '1.0.0'
__author__  = 'Student DevOps Lab'
__all__     = ['create_app', 'feedback_bp', '__version__']


def create_app(config=None) -> Flask:
    """
    Application factory — creates and returns a configured Flask app.

    Args:
        config: None | Config subclass | 'production' | 'development' | 'testing'

    Returns:
        Configured Flask application instance.
    """
    app = Flask(__name__, template_folder='templates', static_folder='static')

    if config is None:
        app.config.from_object(Config)
    elif isinstance(config, str):
        cfg_class = config_map.get(config)
        if not cfg_class:
            raise ValueError(f"Unknown config '{config}'. Choose from: {list(config_map.keys())}")
        app.config.from_object(cfg_class)
    else:
        app.config.from_object(config)

    app.secret_key = app.config['SECRET_KEY']

    with app.app_context():
        init_db(app.config['DB_PATH'])

    app.register_blueprint(feedback_bp)

    return app
