from rec_app.database import db
from sqlalchemy import func


class MoviesModel(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, nullable=False)
    movie_title = db.Column(db.String(500), nullable=False)
    imdb_url = db.Column(db.String(240), nullable=True)
    genre = db.Column(db.String(240), nullable=True)
    cover_image = db.Column(db.String(240), nullable=True)
    story_line = db.Column(db.String(1000), nullable=True)
    timestamp = db.Column(db.DateTime)

    @staticmethod
    def add_movie(_movie_id, _movie_title, _imdb_url, _genre, _cover_image=None, _story_line=None):
        new_movie = MoviesModel(movie_id=_movie_id, movie_title=_movie_title, imdb_url=_imdb_url, genre=_genre, cover_image=_cover_image, story_line=_story_line)
        db.session.add(new_movie)
        db.session.commit()

    @staticmethod
    def get_random_movie():
        return MoviesModel.query.order_by(func.rand()).first()

    def __repr__(self):
        return "<MovieModel {}>".format(self.movie_id)