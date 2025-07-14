from flask import render_template, request, jsonify
from extensions import db
from models import Review, Book

def get_reviews_page():
    return render_template('Reviews.html')

def list_reviews():
    reviews = Review.query.all()
    return jsonify([
        {"review_id": r.review_id, "review_value": r.review_value, "book_id": r.book_id}
        for r in reviews
    ])

def create_review():
    data = request.get_json()
    review = Review(review_id=str(hash(str(data['review_value'])+data['book_id'])), review_value=data['review_value'], book_id=data['book_id'])
    db.session.add(review)
    db.session.commit()
    return jsonify({"review_id": review.review_id, "review_value": review.review_value, "book_id": review.book_id}), 201

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
    if 'book_id' in data:
        review.book_id = data['book_id']
    db.session.commit()
    return {"review_id": review.review_id, "review_value": review.review_value, "book_id": review.book_id}

def delete_review(review_id):
    review = Review.query.get(review_id)
    if not review:
        return '', 204
    db.session.delete(review)
    db.session.commit()
    return '', 204 