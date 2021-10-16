from flask import Flask, jsonify
import csv
from final_demographic import output
from final_content_based import getRecomm, cosine_sim
import itertools

all_movies = []

with open("movies.csv", newline='', encoding="utf8") as f:
    reader = list(csv.reader(f))
    all_movies = reader[1:]

app = Flask(__name__)

liked_movies = []
disliked_movies = []
did_not_watch = []

@app.route('/get-movies')
def getAllMovies():
    movie_data = {
        "Title": all_movies[0][3],
        "Overview": all_movies[0][12],
        "Release_Date": all_movies[0][16] or "N/A",
        "Duration": all_movies[0][18],
        "Vote_Count": all_movies[0][24],
        "Ratings": all_movies[0][23],
        "Poster_Link": all_movies[0][27],
    }
    return jsonify({
        'data': movie_data,
        'message': 'success'
    }), 200

@app.route('/liked', methods = ['POST'])
def liked():
    movie = all_movies[1]
    liked_movies.append(movie)
    all_movies.pop(1)
    return jsonify({
        'data': liked_movies,
        'message': 'success'
    }), 200

@app.route('/disliked', methods=['POST'])
def disliked():
    movie = all_movies[0]
    disliked_movies.append(movie)
    all_movies.pop(0)
    return jsonify({
        'message': 'success'
    }), 200

@app.route('/did_not_watch', methods=['POST'])
def didNotWatch():
    movie = all_movies[0]
    did_not_watch.append(movie)
    all_movies.pop(0)
    return jsonify({
        'message': 'success'
    }), 200

@app.route("/popular-movies")
def popular_movies():
    movie_data = []
    for movie in output:
        data = {
            "title": movie[0],
            "poster_link": movie[1],
            "release_date": movie[2] or "N/A",
            "duration": movie[3],
            "rating": movie[4],
            "overview": movie[5]
        }
        movie_data.append(data)
    return jsonify({
        "data": movie_data,
        "status": "success"
    }), 200

print(liked_movies, "Movie")

@app.route("/recommended-movies")
def recommended_movies():
    all_recommended = []
    for liked_movie in liked_movies:
        print(liked_movie)
        output = getRecomm(liked_movie[3], cosine_sim)
        for data in output:
            all_recommended.append(data)
    all_recommended.sort()
    all_recommended = [all_recommended for all_recommended, _ in itertools.groupby(all_recommended)]

    movie_data = []
    for recommended in all_recommended:
        data = {
            "title": recommended[0],
            "poster_link": recommended[1],
            "release_date": recommended[2] or "N/A",
            "duration": recommended[3],
            "rating": recommended[4],
            "overview": recommended[5]
        }
        movie_data.append(data)
    return jsonify({
        "data": movie_data,
        "status": "success"
    }), 200

if __name__ == '__main__':
    app.run(debug = True)