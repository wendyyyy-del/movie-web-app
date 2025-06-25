from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from sqlalchemy import or_
from .. import db
from ..models import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    print("🔐 REGISTER DATA:", data)

    if not data.get('username') or not data.get('password') or not data.get('email'):
        return jsonify({'error': 'Missing fields'}), 400

    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username exists'}), 400

    try:
        user = User(username=data['username'], email=data['email'])
        user.set_password(data['password'])
        db.session.add(user)
        db.session.commit()
        return jsonify({'message': 'User registered successfully'}), 201

    except Exception as e:
        print("⚠️ Registration Error:", e)
        return jsonify({'error': 'Registration failed'}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    print("🔑 LOGIN DATA:", data)

    if not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Missing username or password'}), 400

    user = User.query.filter(
        or_(
            User.username == data['username'],
            User.email == data['username']
        )
    ).first()

    if user and user.check_password(data['password']):
        token = create_access_token(identity=user.id)
        return jsonify({
            'access_token': token,
            'username': user.username
        }), 200

    return jsonify({'error': 'Invalid credentials'}), 401
