from flask import Flask,jsonify,request
from book import find_all, save, delete, update
from flask_restx import Resource, Api, fields, reqparse

app = Flask(__name__)

api = Api(app, version='1.0', title='Books API',
    description='A simple Books API',
)
ns_books = api.namespace('books', description='Books operations')

books_id_arguments = reqparse.RequestParser()
books_id_arguments.add_argument('id', type=int, required=True)

book_definition = api.model('Book Informations', {
    'title': fields.String(required=True),
    'author': fields.String(required=True)
})

book_definition_input = api.model('Book Informations In', {
    'title': fields.String(required=True),
    'author': fields.String(required=True)
})

book_definition_output = api.model('Book Informations Out', {
    'id': fields.Integer,
    'title': fields.String,
    'author': fields.String
})

@ns_books.route("/")
class books(Resource):

    def get(self):
        results = find_all()
        return jsonify(results)
    
    @api.doc(model=book_definition_output, body=book_definition_input)
    def post(self):
        data = request.get_json()
        save(data.get('name'), data.get('author'))
        resp = jsonify(success=True)
        return resp
    
    @api.expect(books_id_arguments)
    def delete(self):
        data = books_id_arguments.parse_args(request)
        delete(data.get('id'))
        resp = jsonify(success=True)
        return resp

    @api.expect(books_id_arguments,book_definition)
    def put(self):
        id = books_id_arguments.parse_args(request)
        data = request.get_json()
        update(id.get('id'), data.get('name'), data.get('author'))
        resp = jsonify(success=True)
        return resp   
          
app.run()