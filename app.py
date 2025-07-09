from flask import Flask, request, flash, jsonify
from flask_swagger_ui import get_swaggerui_blueprint
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///Authors.db"


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
#db.init_app(app)



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
    





Swagger_url = "/testing/"
API_URL = "/static/app.yaml"
swagger_blueprint = get_swaggerui_blueprint(Swagger_url,API_URL, config={"app_name":"Book Store API"} )

app.register_blueprint(swagger_blueprint, url_prefix = Swagger_url)