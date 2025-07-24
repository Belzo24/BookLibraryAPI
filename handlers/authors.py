from flask import render_template, request, redirect, url_for, jsonify, flash
import requests
from extensions import db
from models import Author
from models import Book
from models import Review
from validation_logging import errors 
from sqlalchemy.exc import IntegrityError
from validation_logging import logging_config
import logging
logger = logging_config.logger


def get_authors_page():
    authors = Author.query.all()
    return render_template('Authors.html', Authors=authors)

def add_author_form():
    name = request.form.get('author_input')
    birth = request.form.get('birth')
    temp_id = str(hash(name+birth))

    try:
        validated_data = errors.AuthorInput(
            author_name = name,
            birth = birth,
            author_id = temp_id
        )

    except ValueError as e :
        logger.error("tried logging here again, will know if something happen ")
        return redirect(url_for('handlers_authors_get_authors_page'))

    if name and birth:
        try:
            author = Author(author_id = validated_data.author_id, author_name = validated_data.author_name, birth = validated_data.birth)
            db.session.add(author)
            db.session.commit()
            logger.info(f"{author} was sucessfully added ")

        except IntegrityError:
            db.session.rollback()
            logger.error(errors.ERROR_DICTIONARY["Author already exists, 403"])
    
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
        validated_data = errors.AuthorInput(
            author_name = data['author_name'],
            birth = data['birth'],
            author_id = str(hash(data['author_name']+data['birth']))
        )

    except ValueError as e :
        logger.error("tried logging here again, will know if something happen ")
        return redirect(url_for('handlers_authors_get_authors_page'))


    try:
        author = Author(author_id = validated_data.author_id, author_name = validated_data.author_name, birth = validated_data.birth)
        db.session.add(author)
        db.session.commit()
        logger.info({"author_id": author.author_id, "author_name": author.author_name, "birth": author.birth})
        return redirect(url_for('handlers_authors_get_authors_page')), 201
    
    except IntegrityError:
        db.session.rollback()
        logger.error(errors.ERROR_DICTIONARY["Author already exists, 403"])
        return errors.ERROR_DICTIONARY["Author name, 422"]

def get_author(author_id):
    author = Author.query.get(author_id)
    if not author:
        return redirect(url_for('handlers_authors_get_authors_page')), 404
    return {"author_id": author.author_id, "author_name": author.author_name, "birth": author.birth}

def update_author():

    data_json = request.get_json()

    temp_author = data_json.get("author_name")
    temp_birth = data_json.get("birth")
    temp_id = data_json.get("author_id")



    author = Author.query.get(temp_id)
    if not author:
        logger.error(errors.ERROR_DICTIONARY["404 author update"])
        return redirect(url_for('handlers_authors_get_authors_page')), 404


    author.author_name = temp_author    
    author.birth = temp_birth
    
    try:
        db.session.commit()
        logger.info("author has been updated:",
                     {"author_id": author.author_id, "author_name": author.author_name, "birth": author.birth})    
        return 204
    
    except IntegrityError:
        db.session.rollback()
        logger.error(errors.ERROR_DICTIONARY["404 author update"])
        return redirect(url_for('handlers_authors_get_authors_page'))
    

def delete_author():
    temp_id = request.form.get("author_id")
    author = Author.query.get(temp_id)
    books = Book.query.filter_by(author_foreign = temp_id).all()
    
    if not author:
        logger.error(errors.ERROR_DICTIONARY["404, not found in userbase"], author)
        return errors.ERROR_DICTIONARY["404, not found in userbase"], 404
    
    if books:
        for book in books:
            reviews = Review.query.filter_by(book_id=book.book_id).all()
            if reviews:
                for review in reviews:
                    db.session.delete(review)
                    logger.info(f"{review} has been removed from the database ")

            db.session.delete(book)
            logger.info(f"{book} has been removed from the database")
    
    db.session.delete(author)
    logger.info(f"{author} has been removed from the database")
    db.session.commit()
    return redirect(url_for('handlers_authors_get_authors_page'))