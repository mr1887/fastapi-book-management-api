from pydantic import BaseModel

class CategoryBase(BaseModel):
    name: str
    description: str | None = None

class CategoryCreate(CategoryBase):
    """Schema for creating a new category."""
    pass 

class CategoryUpdate(CategoryBase):
    """Schema for updating an existing category.    """
    name: str | None = None
    description: str | None = None
class CategoryINDBase(CategoryBase):
    id: int
    class Config:
        orm_mode = True # cho phép sử dụng mô hình ORM để trả về dữ liệu từ cơ sở dữ liệu dưới dạng đối tượng Pydantic

class Category(CategoryINDBase):
    """Schema return for client"""
    pass

