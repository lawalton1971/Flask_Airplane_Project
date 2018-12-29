from flask import Flask

app = Flask(__name__)

path = "sqlite:///C:\\flask\\interview_project\\database.db"
app.config["SQLALCHEMY_DATABASE_URI"] = path
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
