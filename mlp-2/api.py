# Installed packages
from fastapi import FastAPI

# Internal packages
from main import get_movie, tranform_movie

app = FastAPI()


@app.post("/create_movie")
def read_root():
    movie = get_movie('The Matrix')

    print(tranform_movie(movie))
    return {"Hello": "World"}
