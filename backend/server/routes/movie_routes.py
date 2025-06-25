from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from server.models import Movie, db

movie_bp = Blueprint('movie_bp', __name__)

# GET all movies (protected)
@movie_bp.route('/api/movies', methods=['GET'])
@jwt_required()
def get_movies():
    movies = Movie.query.all()
    return jsonify([m.to_dict() for m in movies]), 200

# GET movie by ID (protected)
@movie_bp.route('/api/movies/<int:id>', methods=['GET'])
@jwt_required()
def get_movie(id):
    movie = Movie.query.get_or_404(id)
    return jsonify(movie.to_dict()), 200

# POST new movie (protected)
@movie_bp.route('/api/movies', methods=['POST'])
@jwt_required()
def create_movie():
    data = request.get_json()

    required_fields = ['title', 'description', 'year', 'genre', 'poster_url']
    if not all(field in data and data[field] for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        new_movie = Movie(
            title=data['title'],
            description=data['description'],
            year=data['year'],
            genre=data['genre'],
            poster_url=data['poster_url']
        )
        db.session.add(new_movie)
        db.session.commit()
        return jsonify(new_movie.to_dict()), 201
    except Exception as e:
        print("⚠️ Movie creation error:", e)
        return jsonify({'error': 'Failed to create movie'}), 500
