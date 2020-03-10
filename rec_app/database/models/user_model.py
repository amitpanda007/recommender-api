# The examples in this file come from the Flask-SQLAlchemy documentation
# For more information take a look at:
# http://flask-sqlalchemy.pocoo.org/2.1/quickstart/#simple-relationships

from datetime import datetime
from sqlalchemy.sql import select, func

from rec_app.database import db
from rec_app.common.hash_service import encrypt, verify
from rec_app.database.db_connector import run_query


USER_ID_START_SEQUENCE = 1000

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    first_name = db.Column(db.String(32))
    last_name = db.Column(db.String(32))
    username = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50), index=True, nullable=False, unique=True)
    password_hash = db.Column(db.String(128))
    date_created = db.Column(db.DateTime)
    date_modified = db.Column(db.DateTime)

    def __init__(self, first_name, last_name, username, email, date_created=None):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.email = email
        if date_created is None:
            date_created = datetime.utcnow()
        self.date_created = date_created

    @staticmethod
    def add_user(_first_name, _last_name, _username, _email, _password):
        new_user = User(first_name=_first_name, last_name=_last_name, username=_username, email=_email)
        stmt = "SELECT MAX(user_id) FROM users;"
        uid = run_query(stmt)[0][0]
        if uid is None:
            new_user.set_user_id(USER_ID_START_SEQUENCE)
        else:
            new_user.set_user_id(uid + 1)
        new_user.hash_password(_password)
        db.session.add(new_user)
        db.session.commit()

    def get_name(self):
        return self.first_name + " " + self.last_name

    def set_user_id(self, _user_id):
        self.user_id = _user_id

    def hash_password(self, password):
        self.password_hash = encrypt(password)

    def verify_password(self, password):
        return verify(password, self.password_hash)

    def __repr__(self):
        return '<User {}>'.format(self.first_name+" "+ self.last_name)