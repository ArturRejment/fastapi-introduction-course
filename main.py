from typing import  Optional

from fastapi import FastAPI

app = FastAPI()


@app.get('/blog')
def index(limit: int = 10, published: bool = True, sort: Optional[str] = None):
    if published:
        return {'data': f'{limit} published blogs from the db'}

    return {'data': f'{limit} unpublished blogs from the db'}


@app.get('/blog/{blog_id}')
def show(blog_id: int):
    return {'blog': blog_id}
