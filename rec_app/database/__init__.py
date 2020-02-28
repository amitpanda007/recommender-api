from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def reset_database():
    from rec_app.database.user_model import User
    db.drop_all()
    db.create_all()