from typing import  Optional

from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app = FastAPI()


class Blog(BaseModel):
    title: str
    body: str
    published: Optional[bool]


@app.get('/blog')
def index(limit: int = 10, published: bool = True, sort: Optional[str] = None):
    if published:
        return {'data': f'{limit} published blogs from the db'}

    return {'data': f'{limit} unpublished blogs from the db'}


@app.get('/blog/{blog_id}')
def show(blog_id: int):
    return {'blog': blog_id}


@app.post('/blog')
def create_blog(blog: Blog):
    return {'blog': blog}


if __name__ == "__main__":
    uvicorn.run(app, host='127.0.0.1', port=9000)
