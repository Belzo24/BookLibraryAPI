from flask import Blueprint, render_template


Reviews_app = Blueprint("Reviews_app",__name__)

@Reviews_app.route("/home/reviews/")
def view_Authers():
    return render_template("Reviews.html")