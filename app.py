from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token

from user import User, get_user_by_email
from movie_rec.svd_recommend import top_n_movie

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = 'super-secret' # change in production

jwt = JWTManager(app)


@app.route("/", methods=["GET"])
def home():
    return "Hello From API"


# TODO : Need to add support for password validation
@app.route("/login", methods=["POST"])
def login():
    if request.is_json:
        email = request.json['email']
        password = request.json['password']
    else:
        email = request.form['email']
        password = request.form['password']

    user = get_user_by_email(email)
    if user:
        test = True if password == user.get_password() else False
        if test:
            access_token = create_access_token(identity=email)
            return jsonify(message="Login succeeded!", access_token=access_token, full_name=user.get_name())
        return jsonify(message="Bad email or password"), 401
    else:
        return jsonify(message="Bad email or password"), 401


@app.route("/register", methods=["POST"])
def register():
    email = request.form['email']
    test_email_exist = get_user_by_email(email)
    if test_email_exist:
        return jsonify(message="That email already exists."), 409
    else:
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        password = request.form['password']
        user = User(first_name=first_name, last_name=last_name, email=email, password=password)
        user.create_new_user()
        return jsonify(message="User created successfully."), 201


@app.route("/top-n-movie", methods=["GET"])
def recommend_movie():
    movies = top_n_movie("Star Wars (1977)")
    return str(movies)


if __name__ == "__main__":
    app.run(host="localhost", port=5000)