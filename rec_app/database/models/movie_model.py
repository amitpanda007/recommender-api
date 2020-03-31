from rec_app.database import db


class Movie(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, nullable=False)
    movie_title = db.Column(db.String(120), nullable=False)
    imdb_url = db.Column(db.String(240), nullable=True)
    genre = db.Column(db.String(240), nullable=True)
    timestamp = db.Column(db.DateTime)

    @staticmethod
    def add_movie(_movie_id, _movie_title, _imdb_url, _genre):
        new_movie = Movie(movie_id=_movie_id, movie_title=_movie_title, imdb_url=_imdb_url, genre=_genre)
        db.session.add(new_movie)
        db.session.commit()