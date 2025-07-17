from app import db

class Author(db.Model):
    __tablename__ = "authors"
    author_id = db.Column(db.String, primary_key=True ,nullable=False)
    author_name = db.Column(db.String, unique = True ,nullable=False)
    birth = db.Column(db.String ,nullable=False)

class Books(db.Model):
    __tablename__ = "books"
    book_id = db.Column(db.String, primary_key=True ,nullable=False)
    book_name = db.Column(db.String, unique = True ,nullable=False)
    author_foreign = db.Column(db.String, db.ForeignKey('authors.author_id') ,nullable=False)

class Reviews(db.Model):
    __tablename__ = "reviews"
    review_id = db.Column(db.String, primary_key=True ,nullable=False)
    review_value = db.Column(db.Integer, unique = True ,nullable=False)
    book_id = db.Column(db.String, db.ForeignKey('books.book_id') ,nullable=False) 