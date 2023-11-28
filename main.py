# Installed packages
import pandas as pd
import requests
import uvicorn

from fastapi import FastAPI


################## Constants of the Movie handler ##################
TMDB_KEY = '6cd475d6493bd4fb6ead9f2919db145a'
URL_MOVIE = "https://api.themoviedb.org/3/search/movie"


def get_movie(movie_title: str, year_released: str = None) -> list[dict]:
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


def tranform_movie(movie: list[dict]) -> pd.DataFrame:
    """Transform the movie in a dataFrame.
        Args:
            movie: The movie from the movie title.
        Returns:
            movie_df: The movie in a dataFrame.
    """
    movie_df = pd.DataFrame(movie).to_json(orient='records')
    return movie_df


app = FastAPI()


@app.get("/create_movie")
def read_root():
    movie = get_movie('The Matrix')
    movie_tranformed = tranform_movie(movie)

    return movie_tranformed


if __name__ == '__main__':
    # use the api read_root
    uvicorn.run(app, host="0.0.0.0", port=8000)
