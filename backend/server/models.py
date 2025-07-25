from .app import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    age = db.Column(db.Integer)  # ✅ Added age field

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Movie(db.Model):
    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    genre = db.Column(db.String(50))
    poster_url = db.Column(db.String(255))

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "year": self.year,
            "genre": self.genre,
            "poster_url": self.poster_url
        }


class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', name='fk_reviews_users'),
        nullable=False
    )
    movie_id = db.Column(
        db.Integer,
        db.ForeignKey('movies.id', name='fk_reviews_movies'),
        nullable=False
    )

    def to_dict(self):
        return {
            "id": self.id,
            "content": self.content,
            "rating": self.rating,
            "user_id": self.user_id,
            "movie_id": self.movie_id
        }

