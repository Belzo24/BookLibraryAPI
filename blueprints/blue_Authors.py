from flask import Blueprint, render_template, request, redirect, flash, url_for

authors_app = Blueprint("authors_app",__name__, template_folder="/blueprints/templates")

@authors_app.route("/home/author/", methods = ["GET","POST"])
def view_Authers():
    from app import Author
    global name
    global date
    if request.form.get("action") == "submit":
        name = request.form.get("author_input") 
        date = request.form.get("birth")
        
        
    return render_template("Authors.html",Authors = Author.query.all())



@authors_app.route("/home/author/add/", methods = ["GET","POST"])
def add_data():
    from app import Author, Add_data,db, Add_data
    
    if request.method == "POST":
        author_new = Add_data("author",name, date)
        
        author_add = Author(author_id = author_new.id_generator(), author_name = str(name), birth = str(date))

        db.session.add(author_add)
        db.session.commit()
        
        flash("<h1> author had been added </h1>")
        
        return redirect("/home/author/")
        
    if request.method == "GET":
        return "GET"

    

@authors_app.route("/home/author/remove/", methods = ["GET","POST"])
def remove_data():
    from app import Author, db, Books

    author_temp = Author.query.get(request.form.get("data_remove"))
    if author_temp:
        db.session.delete(Author.query.get(request.form.get("data_remove")))
        db.session.commit()
        book_temp = Books.query.filter_by(author_foreign = author_temp.author_id).all()
        
        if book_temp:
            for books in book_temp:
                db.session.delete(books)
            db.session.commit()
            
            
        flash("<h1>data has been removed</h1>")
        return redirect("/home/author/")
    else:
        return "<h1>user was not found</h1>"


@authors_app.route("/home/author/update/", methods = ["GET","POST"])
def update_data():
    from app import Author, Add_data, db
    new_author = Add_data("author",name, date)
    update_author = Author.query.get(request.form.get("update"))
    
    update_author.author_name = new_author.name
    update_author.author_id = new_author.id_generator()
    update_author.birth = date
    
    db.session.commit()
    
    flash("<h1>data has been altered</h1>")
    return redirect("/home/author/")
