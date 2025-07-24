from flask import render_template, request, redirect, url_for, jsonify, flash
from extensions import db
from models import Book, Author ,Review
import logging
from validation_logging import errors
from validation_logging import logging_config
logger = logging_config.logger


def get_books_page():
    books = Book.query.all()
    return render_template('Books.html', books=books)

def add_book_form():
    request_name = request.form.get('author_input')
    book_title = request.form.get('book')
    author = Author.query.filter_by(author_name=request_name).first()
    temp_id = str(hash(book_title+author.author_id))
    try:
        validation_data = errors.BookInput(
            book_id= temp_id,
            book_name= book_title
        )

    except ValueError as e :
        logger.error("did not pass validation check")
        return redirect(url_for('handlers_authors_get_books_page'))

    books = Book.query.filter_by(book_name=book_title).all()
    if books:
        logger.error("book already exists inside data base")
        return redirect(url_for('handlers_books_get_books_page'))

    
    if author and book_title:
        book = Book(book_id=validation_data.book_id, book_name=validation_data.book_name, author_foreign=author.author_id)
        db.session.add(book)
        db.session.commit()
        logger.info(f"{book_title} was scuessfuly added to the book tables")
        return redirect(url_for('handlers_books_get_books_page'))



def list_books():
    books = Book.query.all()
    return jsonify([
        {"book_id": b.book_id, "book_name": b.book_name, "author_foreign": b.author_foreign}
        for b in books
    ])

def create_book():
    data = request.get_json()
    temp_id = str(hash(data['book_name']+data['author_foreign']))
    
    try:
        validation_data = errors.BookInput(
            book_id= temp_id,
            book_name= data['book_name']
        )

    except ValueError as e :
        logger.error("did not pass validation check")
        return redirect(url_for('handlers_authors_get_authors_page'))
    
    book = Book(book_id=validation_data.book_id, book_name=data['book_name'], author_foreign=data['author_foreign'])
    db.session.add(book)
    db.session.commit()
    logger.info(f"{book.book_id} was sucessfully added to the database")
    return jsonify({"book_id": book.book_id, "book_name": book.book_name, "author_foreign": book.author_foreign}), 201

def get_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return {"error": "Not found"}, 404
    return {"book_id": book.book_id, "book_name": book.book_name, "author_foreign": book.author_foreign}

def update_book():
    data = request.get_json()
    book_id = data.get("book_id")
    author_foreign = data.get("author_key")
    book_name = data.get("book_name")

    try:
        validation_data = errors.BookInput(
            book_id= book_id,
            book_name= book_name
        )

    except ValueError as e :
        logger.error("did not pass validation check")
        return redirect(url_for('handlers_authors_get_authors_page'))
    

    
    author = Author.query.filter_by(author_id=author_foreign).first()
    if not author:
        logger.error("data could not be found, hence is not edited")
        return {"error": "Author not found"}, 404
    
    book = Book.query.get(book_id)

    if not book:
        logger.error("book was not foun within the book database")
        return 404

    book.book_name = book_name
    book.author_foreign = author_foreign


    db.session.commit()
    logger.info("book was sucesfully edited and updated")
    return {"book_id": book.book_id, "book_name": book.book_name, "author_foreign": book.author_foreign}

def delete_book():
    get_book_id = request.form.get('data_remove')
    book = Book.query.get(get_book_id)

    if not book:
        logger.error(f"book was not found within the database, {get_book_id}")
        return '', 204
    
    reviews = Review.query.filter_by(book_id=book.book_id).all()
    if reviews:
        for review in reviews:
            db.session.delete(review)
            logger.info(f"{review}, was sucessfully removed from the review database")
            
    db.session.delete(book)
    db.session.commit()


    return redirect(url_for('handlers_books_get_books_page')), 204 