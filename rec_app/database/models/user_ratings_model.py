import datetime

from rec_app.database import db


class UserRatings(db.Model):
    __tablename__ = 'user_ratings'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    movie_id = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Integer, nullable=True)
    timestamp = db.Column(db.DateTime)

    @staticmethod
    def add_rating(_user_id, _movie_id, _rating, _timestamp=None):
        if _timestamp is None:
            _timestamp = datetime.datetime.utcnow()
        new_rating = UserRatings(user_id=_user_id, movie_id=_movie_id, rating=_rating, timestamp=_timestamp)
        db.session.add(new_rating)
        db.session.commit()