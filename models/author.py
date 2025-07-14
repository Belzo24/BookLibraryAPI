from extensions import db

class Author(db.Model):
    __tablename__ = "authors"
    author_id = db.Column(db.String, primary_key=True ,nullable=False)
    author_name = db.Column(db.String, unique = True ,nullable=False)
    birth = db.Column(db.String ,nullable=False) 