from server import create_app, db

app = create_app()

with app.app_context():
    from server.models import Movie, Review, User  
    
    db.drop_all()
    db.create_all()

    u1 = User(username="testuser", email="test@example.com")
    u1.set_password("testpass")
    db.session.add(u1)
    db.session.commit()

    m1 = Movie(
        title="Inception",
        description="A thief who steals corporate secrets through dreams.",
        genre="Sci-Fi",
        year=2010,
        poster_url="https://example.com/inception.jpg"
    )
    m2 = Movie(
        title="The Dark Knight",
        description="Batman battles the Joker.",
        genre="Action",
        year=2008,
        poster_url="https://example.com/dark_knight.jpg"
    )

    db.session.add_all([m1, m2])
    db.session.commit()

    r1 = Review(content="Mind-blowing visuals!", rating=5, user_id=u1.id, movie_id=m1.id)
    r2 = Review(content="Heath Ledger is iconic.", rating=5, user_id=u1.id, movie_id=m2.id)

    db.session.add_all([r1, r2])
    db.session.commit()

    print("Seeded the database!")
