from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Book(db.Model):
   
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    author = db.Column(db.String(120))

    def __init__(self, title=None, author=None, comment=None, comment_id=None):
        self.title = title
        self.author = author
        self.comment = comment
        self.comment_id = comment_id

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(100))
    booki_id = db.Column(db.Integer, db.ForeignKey("books.id"))
    book = db.relationship("Book", backref=db.backref("comments", lazy="dynamic")) 

    def __init__(self, comment=None):
        self.comment = comment