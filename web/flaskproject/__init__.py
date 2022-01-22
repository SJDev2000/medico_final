from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.secret_key = "mysecretkey123"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://" + str(os.environ.get("POSTGRES_USER")) + ":" + str(os.environ.get("POSTGRES_PASSWORD")) + "@" + "db:5432/" + str(os.environ.get("POSTGRES_DB"))
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False
db = SQLAlchemy(app)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
UPLOAD_FOLDER = './static/uploads'
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

from flaskproject import routes