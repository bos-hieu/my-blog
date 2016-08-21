from flask_script import Manager, Server

from blog_app.app_factory import create_app
from blog_app.models import *
from blog_app.add_data import add_data

import settings

app = create_app(settings)
db.app = app
db.init_app(app)
db.drop_all()
db.create_all()
add_data()

manager = Manager(app)

#Initializing server instance
server = Server(host=settings.APP_HOST, port=settings.APP_PORT)

#Adding command for running the server
manager.add_command("runserver", server)

s = "Template: " + settings.TEMPLATE_DIR

if __name__ == "__main__":
    manager.run()
