#!/usr/bin/python
import os


#
# IMPORTANT: Put any additional includes below this line.  If placed above this
# line, it's possible required libraries won't be in your searchable path
#
"""from wsgi.blog import app as application
from wsgi.blog import *
db.create_all()"""


from blog_app.app_factory import create_app
from blog_app.models import *
import settings


app = create_app(settings)
db.app = app
db.init_app(app)
db.drop_all()
db.create_all()

#
# Below for testing only
#
if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    httpd = make_server('localhost', 8051, app)
    # Wait for a single request, serve it and quit.
    #httpd.handle_request()

    #server forever
    httpd.serve_forever()
