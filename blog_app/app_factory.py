from flask import Flask
from flask_sqlalchemy import SQLAlchemy


def create_app(config_file):
    """

    Create app object
    Parameters:
    @config_file: python module with application settings
    """

    app = Flask(__name__)
    app.config.from_object(config_file)
    app.config['PROPAGATE_EXCEPTIONS'] = True
    #db.init_app(app)
    #db.create_all(db.engine)

    #Registering modules
    from main import main
    app.register_blueprint(main)

    from post import post
    app.register_blueprint(post, url_prefix="/post")

    from users import user
    app.register_blueprint(user, url_prefix="/user")
    
    return app
