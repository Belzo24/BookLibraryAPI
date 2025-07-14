from flask import render_template, request, redirect, url_for, jsonify
from extensions import db
from models import Book, Author

def get_books_page():
    books = Book.query.all()
    return render_template('Books.html', books=books)

def add_book_form():
    author_name = request.form.get('author_input')
    book_title = request.form.get('book')
    author = Author.query.filter_by(author_name=author_name).first()
    if author and book_title:
        book = Book(book_id=str(hash(book_title+author.author_id)), book_name=book_title, author_foreign=author.author_id)
        db.session.add(book)
        db.session.commit()
    return redirect(url_for('handlers.books.get_books_page'))

def list_books():
    books = Book.query.all()
    return jsonify([
        {"book_id": b.book_id, "book_name": b.book_name, "author_foreign": b.author_foreign}
        for b in books
    ])

def create_book():
    data = request.get_json()
    book = Book(book_id=str(hash(data['book_name']+data['author_foreign'])), book_name=data['book_name'], author_foreign=data['author_foreign'])
    db.session.add(book)
    db.session.commit()
    return jsonify({"book_id": book.book_id, "book_name": book.book_name, "author_foreign": book.author_foreign}), 201

def get_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return {"error": "Not found"}, 404
    return {"book_id": book.book_id, "book_name": book.book_name, "author_foreign": book.author_foreign}

def update_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return {"error": "Not found"}, 404
    data = request.get_json()
    if 'book_name' in data:
        book.book_name = data['book_name']
    if 'author_foreign' in data:
        book.author_foreign = data['author_foreign']
    db.session.commit()
    return {"book_id": book.book_id, "book_name": book.book_name, "author_foreign": book.author_foreign}

def delete_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return '', 204
    db.session.delete(book)
    db.session.commit()
    return '', 204 