from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import abort, Api, fields, marshal_with, Resource, reqparse

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite///database.db"
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


book_args = reqparse.RequestParser()
book_args.add_argument("name", type=str, required=True, help="name cannot be empty.")
book_args.add_argument(
    "author", type=str, required=True, help="author cannot be empty."
)
book_args.add_argument("year", type=int, required=True, help="year cannot be empty.")
book_args.add_argument("isbn", type=int, required=True, help="isbn cannot be empty.")

book_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "author": fields.String,
    "year": fields.Integer,
    "isbn": fields.Integer,
}


class Books(Resource):
    @marshal_with(book_fields)
    def get(self):
        books = Librario.query.all()
        return books

    @marshal_with(book_fields)
    def post(self):
        args = book_args.parse_args()
        book = Librario(
            name=args["name"],
            author=args["author"],
            year=args["year"],
            isbn=args["isbn"],
        )
        db.session.add(book)
        db.session.commit()
        books = Librario.query.all()
        return books, 201


class Book(Resource):
    @marshal_with(book_fields)
    def get(self, id):
        book = Librario.query.filter_by(id=id).first()
        if not book:
            abort(404, description="Book not found.")

        return book

    @marshal_with(book_fields)
    def patch(self, id):
        args = book_args.parse_args()
        book = Librario.query.filter_by(id=id).first()
        if not book:
            abort(404, description="Book not found.")

        book.name = args["name"]
        book.author = args["author"]
        book.year = args["year"]
        book.isbn = args["isbn"]
        db.session.commit()

        return book

    @marshal_with(book_fields)
    def delete(self, id):
        book = Librario.query.filter_by(id=id).first()
        if not book:
            abort(404, description="Book not found.")

        db.session.delete(book)
        db.session.commit()
        book = Librario.query.all()

        return book


api.add_resource(Books, "/api/books/")
api.add_resource(Book, "/api/books/<int:id>")


@app.before_request
def create_table():
    db.create_all()


@app.route("/")
def home():
    return f"<h1>Welcome to Librario!</h1>"


if __name__ == "__main__":
    app.run(debug=True)
