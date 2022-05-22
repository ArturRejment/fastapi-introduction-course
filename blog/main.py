from fastapi import FastAPI, Depends
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


@app.post('/blog')
def create_blog(request: BlogSchema, db: Session = Depends(get_db)):
    new_blog = BlogModel(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog
