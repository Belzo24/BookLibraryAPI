from extensions import db

class Book(db.Model):
    __tablename__ = "books"
    book_id = db.Column(db.String, primary_key=True ,nullable=False)
    book_name = db.Column(db.String, unique = True ,nullable=False)
    author_foreign = db.Column(db.String, db.ForeignKey('authors.author_id') ,nullable=False) 