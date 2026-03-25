from fastapi import APIRouter
router = APIRouter() # tạo một router mới để quản lý các endpoint liên quan đến tác giả
@router.get("/") # định nghĩa một endpoint GET tại đường dẫn gốc của router này, tức là /books/
def list_books():
    return {"message": "List of books"}