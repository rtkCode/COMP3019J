from flask import Flask
from sharerapp.config import Config
from flask_sqlalchemy import SQLAlchemy

# init project learned from class code

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

from sharerapp import routes



