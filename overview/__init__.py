from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_migrate import Migrate
from config import Config
from flask_bootstrap import Bootstrap


db = SQLAlchemy()
migrate = Migrate()  

DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    Bootstrap(app)
    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app, db)

    from .views import views
    from .auth import auth
    from .projects import projects

    app.register_blueprint(projects, url_prefix='/projects')
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    

    return app

def create_database(app):
    if not path.exists('overview/' + DB_NAME):
        with app.app_context():
            db.create_all()
        print('Created Database')

