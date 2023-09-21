from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///store.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)


# model Produkt
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)
    count = db.Column(db.Integer, nullable=False)

    def __str__(self):
        return self.name


# model Historia
class History(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String, nullable=False)
    #date = db.Column(db.Integer, default=0)

    def __init__(self, action):
        self.action = action

    def __str__(self):
        return self.action


# model Konto
class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account = db.Column(db.Float)
