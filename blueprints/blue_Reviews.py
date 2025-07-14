from flask import Blueprint, render_template, request, flash, redirect


Reviews_app = Blueprint("Reviews_app",__name__, template_folder="/blueprints/templates")

@Reviews_app.route("/home/reviews/", methods = ["GET","POST"])
def view_Review():
    from app import db, Books, Author, Reviews
    global book
    global input_review_val
    if request.form.get("action") == "submit":
        book = request.form.get("book")
        input_review_val = request.form.get("review_value")
        
    return render_template("Reviews.html",reviews = Reviews.query.all())

@Reviews_app.route("/home/reviews/add/", methods = ["GET","POST"])
def add_Review():
    from app import db, Books, Author, Reviews, Add_data
    book_checker = Books.query.filter_by(book_name = book).first()
    if book_checker:
        new_review = Add_data("review", book_checker.book_id)
        add_review = Reviews(review_id =new_review.id_generator(), review_value = input_review_val)
    



@Reviews_app.route("/home/reviews/remove/", methods = ["GET","POST"])
def remove_Review():
    from app import db, Books, Author, Reviews


@Reviews_app.route("/home/reviews/update/", methods = ["GET","POST"])
def update_Review():
    from app import db, Books, Author, Reviews
