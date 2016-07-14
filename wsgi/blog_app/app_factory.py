from flask import Flask
from flask_sqlalchemy import SQLAlchemy

#Database

def create_app(config_file):
    """

    Create app object
    Parameters:
    @config_file: python module with application settings
    """

    app = Flask(__name__)
    app.config.from_object(config_file)
    #app.config['PROPAGATE_EXCEPTIONS'] = True
    #db.init_app(app)
    #db.create_all(db.engine)

    #Registering modules
    from main import main
    app.register_blueprint(main)

    from blog import blog
    app.register_blueprint(blog, url_prefix="/blog")
    
    return app
