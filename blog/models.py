from sqlalchemy import Column, Integer, String

from blog.database import Base


class BlogModel(Base):
    __tablename__ = 'blog'
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    body = Column(String)


class UserModel(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)
