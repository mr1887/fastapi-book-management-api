from pydantic import BaseModel
from typing import List, Optional
from app.schemas.author import Author
from app.schemas.category import Category
from datetime import datetime
class BookBase(BaseModel):
    title: str
    description: Optional[str] = None
    published_years: int
    cover_image: Optional[str] = None
    author_id: int
    category_id: int
class BookCreate(BookBase):
    pass
class BookUpdate(BookBase):
    title: Optional[str] = None
    description: Optional[str] = None
    published_years: Optional[int] = None
    cover_image: Optional[str] = None
    author_id: Optional[int] = None
    category_id: Optional[int] = None
class BookInDB(BookBase):
    id: int 
    title : str
    description: Optional[str] = None
    published_years: int
    cover_image: Optional[str] = None
    author_id: int
    cover_image: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True # orm cho phep tuong tac voi cac doi tuong ORM nhu SQLAlchemy, cho phep chuyen doi giua cac doi tuong ORM va cac doi tuong Pydantic.

# schema trả về thông tin chi tiết của sách, bao gồm cả thông tin về tác giả và thể loại
class Book(BookInDB):
    author: Optional[Author] = None # thông tin chi tiết về tác giả của sách, có thể để trống nếu không có thông tin
    category: Optional[Category] = None # thông tin chi tiết về thể loại của sách
