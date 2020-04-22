from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# load flask
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# load db
db = SQLAlchemy(app)

# db models
class Stat(db.Model):
    id = db.Column(db.String(120), primary_key=True)
    country = db.Column(db.String(100), unique=False, nullable=False)
    date = db.Column(db.Date, nullable=False)
    confirmed = db.Column(db.Integer)
    deaths = db.Column(db.Integer)
    recovered = db.Column(db.Integer)
    confirmed_pred = db.Column(db.Integer)
    deaths_pred = db.Column(db.Integer)
    recovered_pred = db.Column(db.Integer)

    def __repr__(self):
        return f"Stat('{self.country}', '{self.date}', '{self.confirmed}', '{self.deaths}', '{self.recovered}',  '{self.confirmed_pred}', '{self.deaths_pred}', '{self.recovered_pred}')"

