from rec_app.database import db


class ImdbUserRatingsModel(db.Model):
    __tablename__ = 'imdb_user_ratings'
    id = db.Column(db.Integer, primary_key=True)
    imdb_url_id = db.Column(db.String(20), nullable=False)
    imdb_movie_id = db.Column(db.Integer, nullable=False)
    ten_rtn_cnt = db.Column(db.Integer, nullable=True)
    nine_rtn_cnt = db.Column(db.Integer, nullable=True)
    eight_rtn_cnt = db.Column(db.Integer, nullable=True)
    seven_rtn_cnt = db.Column(db.Integer, nullable=True)
    six_rtn_cnt = db.Column(db.Integer, nullable=True)
    five_rtn_cnt = db.Column(db.Integer, nullable=True)
    four_rtn_cnt = db.Column(db.Integer, nullable=True)
    three_rtn_cnt = db.Column(db.Integer, nullable=True)
    two_rtn_cnt = db.Column(db.Integer, nullable=True)
    one_rtn_cnt = db.Column(db.Integer, nullable=True)
    rating_source = db.Column(db.String(10), nullable=True)
    timestamp = db.Column(db.DateTime)

    def get_rating(self):
        rating = {
            "ten_rtn_cnt": self.ten_rtn_cnt,
            "nine_rtn_cnt": self.nine_rtn_cnt,
            "eight_rtn_cnt": self.eight_rtn_cnt,
            "seven_rtn_cnt": self.seven_rtn_cnt,
            "six_rtn_cnt": self.six_rtn_cnt,
            "five_rtn_cnt": self.five_rtn_cnt,
            "four_rtn_cnt": self.four_rtn_cnt,
            "three_rtn_cnt": self.three_rtn_cnt,
            "two_rtn_cnt": self.two_rtn_cnt,
            "one_rtn_cnt": self.one_rtn_cnt
        }
        return rating
