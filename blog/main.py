from fastapi import FastAPI, Depends, status, Response
from sqlalchemy.orm import Session

from blog.schemas import BlogSchema
from blog.models import BlogModel
from blog.database import engine, SessionLocal


app = FastAPI()

BlogModel.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/blog', status_code=status.HTTP_201_CREATED)
def create_blog(request: BlogSchema, db: Session = Depends(get_db)):
    new_blog = BlogModel(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.get('/blog')
def all_blogs(db: Session = Depends(get_db)):
    blogs = db.query(BlogModel).all()
    return blogs


@app.get('/blog/{blog_id}', status_code=status.HTTP_200_OK)
def specific_blog(blog_id: int, response: Response, db: Session = Depends(get_db)):
    blog = db.query(BlogModel).filter(BlogModel.id == blog_id).first()
    if not blog:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {'error': f'Blog with id "{blog_id}" does not exist in the database'}
    return blog
