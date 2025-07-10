from flask import Flask, request, flash, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
import datetime


from blueprints import blue_Authors, blue_Books, blue_Reviews


app = Flask(__name__,template_folder="C:/Users/fakem/BookLibraryAPI/blueprints/templates")
app.secret_key = "some secrete key"


class Add_data:
    def __init__(self, type, name, forgien_key, ):
        self.type = type
        self.create_id = ""
        self.forgien_key = forgien_key
        self.name = name


    def type_checker(self):
        if self.type == "author":
            self.forgien_key = None
        
    def id_generator(self):
        combine = self.type + str(self.name)
        self.create_id = hash(combine)
        return self.create_id





app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///Authors.db"


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
#db.init_app(app)

Swagger_url = "/testing/"
API_URL = "/static/app.yaml"




@app.route("/home/")
def home_page():
    return render_template("Home.html")


app.register_blueprint(blue_Authors.authors_app)
app.register_blueprint(blue_Books.books_app)
app.register_blueprint(blue_Reviews.Reviews_app)



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
    




if __name__ == '__main__':
    app.run(debug=True)
