from flask import Flask, render_template, request, redirect, url_for
from datamanager.json_data_manager import JSONDataManager
import requests

app = Flask(__name__)
data_manager = JSONDataManager("sample.json")

API_URL = 'http://www.omdbapi.com/?apikey={}&t={}'
API_KEY = '68c0c4ab'


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/users")
def list_users():
    users = data_manager.get_all_users()
    return render_template("users.html", users=users)


@app.route("/users/<user_id>")
def user_movies(user_id):
    users = data_manager.get_all_users()
    username = users.get(user_id)

    movies = data_manager.get_user_movies(user_id)

    return render_template("user.html", user_id=user_id, username=username, movies=movies)


@app.route("/add_user", methods=["GET", "POST"])
def add_user():
    if request.method == "POST":
        username = request.form.get("username")
        data_manager.add_user(username)

        return redirect(url_for("list_users"))

    return render_template("add_user.html")


@app.route("/users/<user_id>/add_movie", methods=["GET", "POST"])
def add_movie(user_id):
    users = data_manager.get_all_users()
    username = users.get(user_id)

    if request.method == "POST":
        movie_title = request.form.get("title")
        api_call = requests.get(API_URL.format(API_KEY, movie_title)).json()

        if api_call["Response"] == "False":
            print("Could not connect to the API. Please try again.")
        else:
            title = api_call["Title"]
            director = api_call["Director"]
            year = api_call["Year"]
            rating = float(api_call["imdbRating"])

            data_manager.add_movie_data(user_id, title, director, year, rating)

        return redirect(url_for("user_movies", user_id=user_id))

    return render_template("add_movie.html", user_id=user_id,
                           username=username)


@app.route("/users/<user_id>/update_movie/<movie_id>", methods=["GET", "POST"])
def update_movie(user_id, movie_id):
    users = data_manager.get_all_users()
    username = users.get(user_id)

    movies = data_manager.get_user_movies(user_id)
    movie = movies.get(movie_id)

    if request.method == "POST":
        title = request.form.get("title")
        director = request.form.get("director")
        year = request.form.get("year")
        rating = float(request.form.get("rating"))

        data_manager.update_movie_data(user_id, movie_id, title, director, year, rating)

        return redirect(url_for("user_movies", user_id=user_id))

    return render_template("update_movie.html", user_id=user_id,
                           movie_id=movie_id, username=username, movie=movie)


@app.route("/users/<user_id>/delete_movie/<movie_id>", methods=["GET", "POST"])
def delete_movie(user_id, movie_id):
    users = data_manager.get_all_users()
    username = users.get(user_id)

    movies = data_manager.get_user_movies(user_id)
    movie = movies.get(movie_id)

    if request.method == "POST":
        data_manager.delete_movie_data(user_id, movie_id)

        return redirect(url_for("user_movies", user_id=user_id))

    return render_template("delete_movie.html", user_id=user_id,
                           movie_id=movie_id, username=username, movie=movie)


@app.errorhandler(400)
def bad_request(error):
    return render_template("400.html"), 400


@app.errorhandler(401)
def unauthroized(error):
    return render_template("401.html"), 401


@app.errorhandler(403)
def forbidden(error):
    return render_template("403.html"), 403


@app.errorhandler(404)
def not_found(error):
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_server_error(error):
    return render_template("500.html"), 500


if __name__ == "__main__":
    app.run("0.0.0.0", debug=True)
