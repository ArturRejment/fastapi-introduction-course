from fastapi import FastAPI

from blog.schemas import BlogSchema
from blog.models import BlogModel
from blog.database import engine


app = FastAPI()

BlogModel.metadata.create_all(bind=engine)


@app.post('/blog')
def create_blog(blog: BlogSchema):
    return {'new_blog': blog}
