import datetime

from rec_app.database import db


class ImdbUserRatingsModel(db.Model):
    __tablename__ = 'imdb_user_ratings'
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, nullable=False)
    ten_star = db.Column(db.Integer, nullable=False)
    nine_star = db.Column(db.Integer, nullable=False)
    eight_star = db.Column(db.Integer, nullable=False)
    seven_star = db.Column(db.Integer, nullable=False)
    six_star = db.Column(db.Integer, nullable=False)
    five_star = db.Column(db.Integer, nullable=False)
    four_star = db.Column(db.Integer, nullable=False)
    three_star = db.Column(db.Integer, nullable=False)
    two_star = db.Column(db.Integer, nullable=False)
    one_star = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime)

    @staticmethod
    def add_imdb_rating(_user_id, _movie_id, _ten_star, _nine_star, _eight_star, _seven_star, _six_star, _five_star,
                        _four_star, _three_star, _two_star, _one_star, _timestamp=None):
        if _timestamp is None:
            _timestamp = datetime.datetime.utcnow()
        new_rating = ImdbUserRatingsModel(user_id=_user_id, movie_id=_movie_id, ten_star=_ten_star, nine_star=_nine_star,
                                      eight_star=_eight_star, seven_star=_seven_star, six_star=_six_star,
                                      five_star=_five_star, four_star=_four_star, three_star=_three_star,
                                      two_star=_two_star, one_star=_one_star, timestamp=_timestamp)
        db.session.add(new_rating)
        db.session.commit()