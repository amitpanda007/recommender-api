import logging.config

import os
from flask import Flask, Blueprint
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from rec_app import settings
from rec_app.api.auth.authorization import ns as auth_namespace
from rec_app.api.recommend.recommender import ns as rec_namespace
from rec_app.api.movies.movies import ns as movie_namespace
from rec_app.api.ratings.rating import ns as rating_namespace
from rec_app.api.restplus import api
from rec_app.database import db, init_database, reset_database

app = Flask(__name__)
# logging_conf_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '../logging.conf'))
# logging.config.fileConfig(logging_conf_path)
log = logging.getLogger(__name__)
jwt = JWTManager(app)
CORS(app) #spefic usgae for path : cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


def configure_app(flask_app):
    # flask_app.config['SERVER_NAME'] = settings.FLASK_SERVER_NAME
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = settings.SQLALCHEMY_DATABASE_URI_MYSQL
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = settings.SQLALCHEMY_TRACK_MODIFICATIONS
    flask_app.config['SWAGGER_UI_DOC_EXPANSION'] = settings.RESTPLUS_SWAGGER_UI_DOC_EXPANSION
    flask_app.config['RESTPLUS_VALIDATE'] = settings.RESTPLUS_VALIDATE
    flask_app.config['RESTPLUS_MASK_SWAGGER'] = settings.RESTPLUS_MASK_SWAGGER
    flask_app.config['ERROR_404_HELP'] = settings.RESTPLUS_ERROR_404_HELP
    flask_app.config["JWT_SECRET_KEY"] = settings.JWT_SECRET_KEY


def initialize_app(flask_app):
    configure_app(flask_app)

    blueprint = Blueprint('api-v1', __name__, url_prefix='/api/v1')
    api.init_app(blueprint)
    api.add_namespace(auth_namespace)
    api.add_namespace(rec_namespace)
    api.add_namespace(movie_namespace)
    api.add_namespace(rating_namespace)
    flask_app.register_blueprint(blueprint)

    db.init_app(flask_app)
    # reset_database(flask_app)
    with flask_app.app_context():
        db.create_all()
    print("App Initialization Complete!")


def main():
    initialize_app(app)
    log.info('>>>>> Starting development server at http://{}/api/ <<<<<'.format(app.config['SERVER_NAME']))
    app.run(host=settings.FLASK_SERVER_HOST, port=settings.FLASK_SERVER_PORT, debug=settings.FLASK_DEBUG)


if __name__ == "__main__":
    main()