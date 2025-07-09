from flask import Flask, request, flash, jsonify, render_template
from flask_swagger_ui import get_swaggerui_blueprint
from flask_sqlalchemy import SQLAlchemy
import datetime


from blueprints import blue_Authors, blue_Books, blue_Reviews


app = Flask(__name__,template_folder="some direction please remember to do for next time ")


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///Authors.db"


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
#db.init_app(app)

Swagger_url = "/testing/"
API_URL = "/static/app.yaml"
swagger_blueprint = get_swaggerui_blueprint(Swagger_url,API_URL, config={"app_name":"Book Store API"} )




@app.route("/home/")
def home_page():
    return render_template("Home.html")




app.register_blueprint(swagger_blueprint, url_prefix = Swagger_url)
app.register_blueprint(blue_Authors.authors_app)
app.register_blueprint(blue_Books.books_app)
app.register_blueprint(blue_Reviews.Reviews_app)



class Author(db.Model):
    __tablename__ = "authors"
    author_id = db.Column(db.String, primary_key=True)
    author_name = db.Column(db.String, unique = True)
    birth = db.Column(db.String)

class Books(db.Model):
    __tablename__ = "books"
    book_id = db.Column(db.String, primary_key=True)
    book_name = db.Column(db.String, unique = True)
    author_foreign = db.Column(db.String, db.ForeignKey('authors.author_id'))


class Reviews(db.Model):
    __tablename__ = "reviews"
    review_id = db.Column(db.String, primary_key=True)
    review_value = db.Column(db.Integer, unique = True)
    book_id = db.Column(db.String, db.ForeignKey('books.book_id'))
    





