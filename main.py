from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import (
    abort,
    Api,
    fields,
    marshal_with,
    Resource,
    reqparse
)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite///database.db'
db = SQLAlchemy(app)
api = Api(app)

class Librario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    author = db.Column(db.String(80), unique=False, nullable=False)
    year = db.Column(db.Integer, unique=False, nullable=False)
    isbn = db.Column(db.Integer, unique=True, nullable=False)

    def __repr__(self):
        return f"Name: {self.name}, Author: {self.author}, Year Released: {self.year}, ISBN Number: {self.isbn}"
