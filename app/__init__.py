from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
#from flask_bootstrap import Bootstrap

app = Flask(__name__)
#bootstrap = Bootstrap(app)
login = LoginManager(app)
login.login_message = "Войдите, чтобы открыть эту страницу."
app.config.from_object(Config)
db = SQLAlchemy(app)
from app import routes
migrate = Migrate(app, db)
login.login_view = 'login'
#app.run(host="127.0.0.1", port="5000", debug=True)