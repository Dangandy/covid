from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# load flask
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"

# load db
db = SQLAlchemy(app)

# db models
class Stat(db.Model):
    id = db.Column(db.String(120), primary_key=True)
    country = db.Column(db.String(100), unique=False, nullable=False)
    date = db.Column(db.String(10), nullable=False)
    confirmed = db.Column(db.Integer, nullable=False)
    deaths = db.Column(db.Integer, nullable=False)
    recovered = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Stat('{self.country}', '{self.date}', '{self.confirmed}', '{self.deaths}', '{self.recovered}')"

