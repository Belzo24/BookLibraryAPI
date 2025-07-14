from flask import Blueprint, render_template,request, flash, redirect


books_app = Blueprint("books_app",__name__, template_folder="C:/Users/fakem/BookLibraryAPI/blueprints/templates")

@books_app.route("/home/books/", methods = ["GET","POST"])
def view_books():
    from app import db, Books
    global book
    global enter_author
    
    if request.form.get("action") == "submit":
        enter_author = request.form.get("author_input")
        book = request.form.get("book")
    
    
    return render_template("Books.html",books = Books.query.all())




@books_app.route("/home/books/add/", methods = ["GET","POST"])
def add_books():
    from app import db, Books, Author, Add_data
    checker = Author.query.filter_by(author_name = str(enter_author)).first()
    if checker:
        create_book = Add_data("book", book, checker )
        new_book = Books(book_id = create_book.id_generator(), book_name = book, author_foreign = checker.author_id)
        db.session.add(new_book)
        db.session.commit()
        return redirect("/home/books/")
    else:
        return "finished"
    
    

@books_app.route("/home/books/remove/", methods = ["GET","POST"])
def remove_books():
    from app import db, Books
    book_condition = request.form.get("unalive")
    data = request.form.get("data_remove")
    if book_condition == "true":
        temp_book = Books.query.get(data)
        db.session.delete(temp_book)
        db.session.commit()
        return redirect("/home/books/")
    
    return "<h1>None</h1>"


@books_app.route("/home/books/update/", methods = ["GET","POST"])
def update_books():
    from app import db, Books
    return "hello"
