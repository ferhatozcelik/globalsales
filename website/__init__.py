import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
import config

db = SQLAlchemy()


def create_app():
    # POSTGRES Database Config
    if config.DEBUG:
        POSTGRES_URL = config.CONFIG['postgresUrl']
        POSTGRES_USER = config.CONFIG['postgresUser']
        POSTGRES_PASS = config.CONFIG['postgresPass']
        POSTGRES_DB = config.CONFIG['postgresDb']
    else:
        POSTGRES_URL = os.environ.get('postgresUrl')
        POSTGRES_USER = os.environ.get('postgresUser')
        POSTGRES_PASS = os.environ.get('postgresPass')
        POSTGRES_DB = os.environ.get('postgresDb')

    # POSTGRES Database Connection
    DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER,
                                                                   pw=POSTGRES_PASS,
                                                                   url=POSTGRES_URL,
                                                                   db=POSTGRES_DB)
    app = Flask(__name__)
    app.debug = config.DEBUG
    app.secret_key = "ferhat-ozcelik"
    app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Advert

    db.create_all(app=app)

    login_manager = LoginManager()
    login_manager.login_view = 'views.home'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app
