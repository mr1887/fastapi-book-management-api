from pydantic import BaseModel
class AuthorBase(BaseModel):
    name: str
    bio: str | None = None

class AuthorCreate(AuthorBase):
    # cac truong du lieu khac neu can thiet
    pass
class AuthorUpdate(AuthorBase):
    name: str | None = None
    bio: str | None = None
class AuthorInDB(AuthorBase):
    id: int
    class Config:
        orm_mode = True # orm cho phep tuong tac voi cac doi tuong ORM nhu SQLAlchemy, cho phep chuyen doi giua cac doi tuong ORM va cac doi tuong Pydantic.
class Author(AuthorInDB):
    # cac truong du lieu khac neu can thiet
    pass