from datetime import datetime

from rec_app.database import db


class RecommendationsModel(db.Model):
    __tablename__ = 'recommendations'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    rec_type = db.Column(db.String(5))
    rec_avl_status = db.Column(db.String(10))
    rec_mov_ids = db.Column(db.String(40))
    date_created = db.Column(db.DateTime)
    date_modified = db.Column(db.DateTime)

    @staticmethod
    def init_recommendation(_user_id, _rec_type, _rec_avl_status="EMPTY", _rec_mov_ids=None):
        new_rec = RecommendationsModel(user_id=_user_id, rec_type=_rec_type, rec_avl_status=_rec_avl_status, rec_mov_ids=_rec_mov_ids)
        new_rec.date_created = datetime.utcnow()
        db.session.add(new_rec)
        db.session.commit()

    def __repr__(self):
        return '<RecommendationsModel {}>'.format(self.user_id + "," + self.rec_mov_ids)


class RecommendationsEnum:
    # STATUS
    EMPTY_STATUS = "EMPTY"
    AVAILABLE_STATUS = "AVAILABLE"
    PROCESSING_STATUS = "PROCESSING"

    # Recommendation Type
    MATRIX_FACTORIZATION = "MTX"
    SINGULAR_VALUE_DECOMPOSITION = "SVD"