from flask import render_template, request, jsonify, redirect, url_for
from extensions import db
from models import Review, Book

def get_reviews_page():
    review_table = Review.query.all()
    return render_template('Reviews.html', reviews=review_table)

def list_reviews():
    reviews = Review.query.all()
    return jsonify([
        {"review_id": r.review_id, "review_value": r.review_value, "book_id": r.book_id}
        for r in reviews
    ])

def create_review():

    review_value = request.form.get('review_value')
    book_id = request.form.get('book_id')

    review = Review(review_id=str(hash(str(review_value))), review_value=review_value, book_id=book_id)
    db.session.add(review)
    db.session.commit()
    return redirect(url_for('handlers_reviews_get_reviews_page')), 201

def get_review(review_id):
    review = Review.query.get(review_id)
    if not review:
        return {"error": "Not found"}, 404
    return {"review_id": review.review_id, "review_value": review.review_value, "book_id": review.book_id}

def update_review(review_id):
    review = Review.query.get(review_id)
    if not review:
        return {"error": "Not found"}, 404
    data = request.get_json()
    if 'review_value' in data:
        review.review_value = data['review_value']
    if 'update_book_id' in data:
        review.book_id = data['update_book_id']
    db.session.commit()
    return jsonify({"redirect": url_for('handlers_reviews_get_reviews_page')})

def delete_review(review_id):
    review = Review.query.get(review_id)
    if not review:
        return '', 204
    db.session.delete(review)
    db.session.commit()
    return redirect(url_for('handlers_reviews_get_reviews_page')), 204 