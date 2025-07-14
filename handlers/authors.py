from flask import render_template, request, redirect, url_for, jsonify, flash
from extensions import db
from models import Author
from sqlalchemy.exc import IntegrityError

def get_authors_page():
    authors = Author.query.all()
    return render_template('Authors.html', Authors=authors)

def add_author_form():
    name = request.form.get('author_input')
    birth = request.form.get('birth')
    if name and birth:
        try:
            author = Author(author_id=str(hash(name+birth)), author_name=name, birth=birth)
            db.session.add(author)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash(f"Author '{name}' already exists!", "error")
    return redirect(url_for('handlers_authors_get_authors_page'))

def list_authors():
    authors = Author.query.all()
    return jsonify([
        {"author_id": a.author_id, "author_name": a.author_name, "birth": a.birth}
        for a in authors
    ])

def create_author():
    data = request.get_json()
    try:
        author = Author(author_id=str(hash(data['author_name']+data['birth'])), author_name=data['author_name'], birth=data['birth'])
        db.session.add(author)
        db.session.commit()
        return jsonify({"author_id": author.author_id, "author_name": author.author_name, "birth": author.birth}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": f"Author '{data['author_name']}' already exists!"}), 409

def get_author(author_id):
    author = Author.query.get(author_id)
    if not author:
        return {"error": "Not found"}, 404
    return {"author_id": author.author_id, "author_name": author.author_name, "birth": author.birth}

def update_author(author_id):
    author = Author.query.get(author_id)
    if not author:
        return {"error": "Not found"}, 404
    data = request.get_json()
    if 'author_name' in data:
        author.author_name = data['author_name']
    if 'birth' in data:
        author.birth = data['birth']
    try:
        db.session.commit()
        return {"author_id": author.author_id, "author_name": author.author_name, "birth": author.birth}
    except IntegrityError:
        db.session.rollback()
        return {"error": f"Author '{data.get('author_name', '')}' already exists!"}, 409

def delete_author(author_id):
    author = Author.query.get(author_id)
    if not author:
        return '', 204
    db.session.delete(author)
    db.session.commit()
    return '', 204 