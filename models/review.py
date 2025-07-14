from extensions import db

class Review(db.Model):
    __tablename__ = "reviews"
    review_id = db.Column(db.String, primary_key=True ,nullable=False)
    review_value = db.Column(db.Integer, unique = True ,nullable=False)
    book_id = db.Column(db.String, db.ForeignKey('books.book_id') ,nullable=False) 