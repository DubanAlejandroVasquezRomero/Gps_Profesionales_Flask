from flask import Flask
import os 

def create_app ():
    app = Flask (__name__)

    app.config.from_mapping (
        SECRET_KEY = 'mikey',
        API_KEY_GOOGLE = os.environ.get (""),
        DATABASE_HOST = os.environ.get('FLASK_DATABASE_HOST'),
        DATABASE_PASSWORD = os.environ.get ('FLASK_DATABASE_PASSWORD'),
        DATABASE_USER = os.environ.get ('FLASK_DATABASE_USER'),
        DATABASE = os.environ.get ('FLASK_DATABASE'),
        
    )

    from . import db, auth, Home, Usuario, Admin, Profesional
    db.init_app(app)
    app.register_blueprint (Admin.bp)
    app.register_blueprint (Usuario.bp)
    app.register_blueprint (auth.bp)
    app.register_blueprint (Home.bp)
    app.register_blueprint (Profesional.bp)

    return app

