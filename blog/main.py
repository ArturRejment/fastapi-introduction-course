from typing import List

from fastapi import FastAPI, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session

from blog.schemas import BlogSchema, ShowBlogSchema
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


@app.delete('/blog/{blog_id}', status_code=status.HTTP_200_OK)
def delete_blog(blog_id: int, db: Session = Depends(get_db)):
    blog = db.query(BlogModel).filter(BlogModel.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Blog with id {blog_id} does not exist.")
    db.delete(blog)
    db.commit()
    return {'detail': 'Blog deleted successfully.'}


@app.put('/blog/{blog_id}', status_code=status.HTTP_200_OK)
def update_blog(blog_id: int, request: BlogSchema, db: Session = Depends(get_db)):
    blog = db.query(BlogModel).filter(BlogModel.id == blog_id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Blog with id {blog_id} does not exist.")
    blog.update(request.dict())
    db.commit()
    return {'detail': 'Blog updated successfully.'}


@app.get('/blog', response_model=List[ShowBlogSchema])
def all_blogs(db: Session = Depends(get_db)):
    blogs = db.query(BlogModel).all()
    return blogs


@app.get('/blog/{blog_id}', status_code=status.HTTP_200_OK, response_model=ShowBlogSchema)
def specific_blog(blog_id: int, db: Session = Depends(get_db)):
    blog = db.query(BlogModel).filter(BlogModel.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Blog with id {blog_id} does not exist.")
    return blog
