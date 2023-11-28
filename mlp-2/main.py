# Installed packages
import tmdbsimple as tmdb
import pandas as pd
import requests
import uvicorn

from fastapi import FastAPI


################## Constants of the Movie handler ##################
TMDB_KEY = '6cd475d6493bd4fb6ead9f2919db145a'
URL_MOVIE = "https://api.themoviedb.org/3/search/movie"

################## Global settings ##################
tmdb.API_KEY = TMDB_KEY


################## Functions ##################


def get_movies(movie_title: str, year_released: str = None) -> list[dict]:
    """Get the movie from the movie title.
        Args:
            movie_title: The title of the movie.
            year_released: The year the movie was released.

        Returns:
            movie: The movie from the movie title.
    """
    # initialisation
    params = {"api_key": TMDB_KEY, "query": movie_title}

    # make the request to the movie API
    response = requests.get(URL_MOVIE, params=params)

    # check if the request was successful
    if response.status_code != 200 or not response.json().get('results'):
        return None

    # get the movie
    if year_released:
        for movie in response.json()['results']:
            if movie['release_date'].split('-')[0] == year_released:
                return movie

    movie = response.json()['results']
    return movie


app = FastAPI()


@app.get("/get_movies_review")
def get_movies_review():
    """Transform the movie in a dataFrame.
        Args:
            movie_title: The movie's title.
        Returns:
            movies' reviews: The movie reviews in a json.
    """
    # initialisation
    movies = get_movies('The Matrix')
    movies_reviews = []

    for movie in movies:
        print(movie)
        movies_reviews.append(movie["overview"])

    # put the movies' reviews in a json
    movies_reviews = pd.DataFrame(movies_reviews).to_json(orient='records')

    return movies_reviews


@app.get("/get_movies_genre")
def get_genre():
    """Get the genre of the movie.
        Args:
            movie: The movie from the movie title.
        Returns:
            genre: The genre of the movie.
    """
    # initialisations
    movies = get_movies('The Matrix')
    genres_movies = [movie['genre_ids'] for movie in movies]
    genres_names = []

    # get the genre of the movie
    for genres_movie in genres_movies:
        genres_movies = tmdb.Genres()
        response = genres_movies.movie_list()

        for g in response['genres']:
            for genre in genres_movie:
                if g['id'] == genre:
                    genres_names.append(g['name'])
    # put the genres in a json
    genres_names = pd.DataFrame(genres_names).to_json(orient='records')

    return genres_names


if __name__ == '__main__':
    # use the api read_root
    uvicorn.run(app, host="0.0.0.0", port=8000)
