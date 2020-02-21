# Prerequisite
pip install flask

# App Setup & Run on Windows
set FLASK_APP=app.py
flask run

# App Setup & Run on Linux
env FLASK_APP=app.py
flask run

# Build & Run Docker App
docker build --rm -f recommender-api/Dockerfile -t recommender-api:v1 recommender-api

docker run --rm -d -p 5000:5000 recommender-api:v1