from flask import Flask,jsonify,request
from flask_restx import Resource, Api, fields, reqparse
from flask_sqlalchemy import SQLAlchemy
from models import Book, db, Comment


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///book.db'
db.init_app(app)

with app.app_context():
    db.create_all()
    db.session.commit()

api = Api(app, version='1.0', title='Books API',
    description='A simple Books API',
)
ns_books = api.namespace('books', description='Books operations')

books_id_arguments = reqparse.RequestParser()
books_id_arguments.add_argument('id', type=int, required=True)

comments_id_arguments = reqparse.RequestParser()
comments_id_arguments.add_argument('id', type=int, required=True)


book_definition = api.model('Book Informations', {
    'name': fields.String(required=True),
    'author': fields.String(required=True),
    'comment_id': fields.Integer(),
    'comment': fields.String()
})

comment_definition = api.model('Comment Informations', {
    'comment': fields.String(required=True)
})

def row2dict(row):
    d = {}
    for column in row.__table__.columns:
        d[column.name] = str(getattr(row, column.name))

    return d



@ns_books.route("/")
class books(Resource):

    def get(self):
        books = Book.query.all()
        return jsonify([row2dict(book) for book in books])
    
    @api.expect(book_definition)
    def post(self):
        data = request.get_json()
        book = Book(data.get('name'), data.get('author'))
        db.session.add(book)
        db.session.commit()
        resp = jsonify(success=True)
        return resp
    
    @api.expect(books_id_arguments)
    def delete(self):
        data = books_id_arguments.parse_args(request)
        book = Book.query.get(data.get('id'))
        db.session.delete(book)
        db.session.commit()
        resp = jsonify(success=True)
        return resp

    @api.expect(books_id_arguments,book_definition)
    def put(self):
        id = books_id_arguments.parse_args(request)
        data = request.get_json()
        book = Book.query.get(id)
        book.title = data.get('name')
        book.author = data.get('author')
        db.session.commit()
        resp = jsonify(success=True)
        return resp 

@ns_books.route("/comments")
class comments(Resource):

    def get(self):
        comments = Comment.query.all()
        return jsonify([row2dict(comment) for comment in comments])
    
    @api.expect(comment_definition)
    def post(self):
        data = request.get_json()
        comment = Comment(data.get('comment'))
        db.session.add(comment)
        db.session.commit()
        resp = jsonify(success=True)
        return resp
    
    @api.expect(comments_id_arguments)
    def delete(self):
        data = comments_id_arguments.parse_args(request)
        comment = Comment.query.get(data.get('id'))
        db.session.delete(comment)
        db.session.commit()
        resp = jsonify(success=True)
        return resp

    @api.expect(comments_id_arguments,comment_definition)
    def put(self):
        id = comments_id_arguments.parse_args(request)
        data = request.get_json()
        comment = Comment.query.get(id)
        comment.comment = data.get('comment')
        db.session.commit()
        resp = jsonify(success=True)
        return resp  

app.run()