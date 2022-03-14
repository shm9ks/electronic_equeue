from app import *
#################################
from werkzeug.debug import DebuggedApplication

def create_app_heroku(environ, start_response):
    return app

def create_app():
    # Insert whatever else you do in your Flask app factory.

    if app.debug:
        app.wsgi_app = DebuggedApplication(app.wsgi_app, evalex=True)

    return