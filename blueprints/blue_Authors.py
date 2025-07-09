from flask import Blueprint, render_template


authors_app = Blueprint("authors_app",__name__)

@authors_app.route("/home/author/")
def view_Authers():
    return render_template("Author.html")