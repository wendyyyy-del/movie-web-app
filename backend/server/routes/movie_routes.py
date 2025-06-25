from flask import Blueprint, jsonify, request
from server.models import Movie, db

movie_bp = Blueprint('movie_bp', __name__)

@movie_bp.route('/api/movies', methods=['GET'])
def get_movies():
    movies = Movie.query.all()
    return jsonify([m.to_dict() for m in movies]), 200

@movie_bp.route('/api/movies/<int:id>', methods=['GET'])
def get_movie(id):
    movie = Movie.query.get_or_404(id)
    return jsonify(movie.to_dict()), 200

@movie_bp.route('/api/movies', methods=['POST'])
def create_movie():
    data = request.get_json()
    new_movie = Movie(
        title=data.get('title'),
        description=data.get('description'),
        genre=data.get('genre'),
        poster_url=data.get('poster_url')
    )
    db.session.add(new_movie)
    db.session.commit()
    return jsonify(new_movie.to_dict()), 201
