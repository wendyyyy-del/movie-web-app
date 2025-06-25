from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from server.models import Review, Movie, db


review_bp = Blueprint('review_bp', __name__)

@review_bp.route('/<int:movie_id>/reviews', methods=['GET'])
def get_reviews(movie_id):
    reviews = Review.query.filter_by(movie_id=movie_id).all()
    return jsonify([r.to_dict() for r in reviews]), 200

@review_bp.route('/<int:movie_id>/reviews', methods=['POST'])
@jwt_required()
def create_review(movie_id):
    data = request.get_json()

    movie = Movie.query.get(movie_id)
    if not movie:
        return jsonify({'error': 'Movie not found'}), 404

    current_user_id = get_jwt_identity()
    new_review = Review(
        content=data.get('content'),
        rating=data.get('rating'),
        user_id=current_user_id,
        movie_id=movie_id
    )

    db.session.add(new_review)
    db.session.commit()

    return jsonify(new_review.to_dict()), 201

@review_bp.route('/reviews/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_review(id):
    review = Review.query.get(id)
    if not review:
        return jsonify({'error': 'Review not found'}), 404

    current_user_id = get_jwt_identity()
    if review.user_id != current_user_id:
        return jsonify({'error': 'Not authorized'}), 403

    db.session.delete(review)
    db.session.commit()
    return jsonify({'message': 'Review deleted'}), 200
