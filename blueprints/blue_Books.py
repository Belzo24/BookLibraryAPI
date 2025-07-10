from flask import Blueprint, render_template


books_app = Blueprint("books_app",__name__, template_folder="C:/Users/fakem/BookLibraryAPI/blueprints/templates")

@books_app.route("/home/books/")
def view_Authers():
    return render_template("Books.html")