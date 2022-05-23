from pydantic import BaseModel


class BlogSchema(BaseModel):
    title: str
    body: str


class ShowBlogSchema(BaseModel):
    title: str
    body: str

    class Config:
        orm_mode = True
