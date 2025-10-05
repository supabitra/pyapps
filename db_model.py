from flask import (
    Flask,
    jsonify,
    redirect,
    request,
    url_for,
    render_template,
    session,
    flash,
)

from flask_sqlalchemy import SQLAlchemy

# import db_model

#####################################################################
app = Flask(__name__)
app.secret_key = "Galaxy123"  # Needed for session management
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
app.app_context().push()


#####################################################################
class tUser(db.Model):
    # id = db.Column(db.Integer, primary_key=True)
    # username = db.Column(db.String(80), unique=True, nullable=False)
    username = db.Column(db.String(80), primary_key=True)
    password = db.Column(db.String(80), nullable=False)
    user_type = db.Column(db.Integer, nullable=False)

    def __init__(self, username, password, user_type):
        self.username = username
        self.password = password
        self.user_type = user_type

    # def __repr__(self):
    #     return f"<User {self.username}>"


#####################################################################
