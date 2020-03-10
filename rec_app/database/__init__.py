from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def reset_database():
    from rec_app.database.models.user_ratings_model import UserRatings
    db.drop_all()
    db.create_all()


def init_database(engine):
    db_engine = SQLAlchemy.create_engine(engine, echo=True)
    SQLAlchemy.Model.metadata.create_all(db_engine)