from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from app import db, models
from app.api.deps import get_db
from app.schemas.author import Author as AuthorSchema, AuthorCreate # Đây là Pydantic Schema
from app.models.author import Author as AuthorModel   # Đây là SQLAlchemy Model
router = APIRouter() # tạo một router mới để quản lý các endpoint liên quan đến tác giả
@router.get("/", response_model=List[AuthorSchema]) # định nghĩa một endpoint GET tại đường dẫn gốc của router này, tức là /authors/
def list_authors(skip: int =0, limit: int = 100 , db = Depends(get_db)):
    # truy vấn cơ sở dữ liệu để lấy danh sách các tác giả, áp dụng phân trang
    authors = db.query(AuthorModel).offset(skip).limit(limit).all() # truy vấn cơ sở dữ liệu để lấy danh sách các tác giả, áp dụng phân trang
    return authors # trả về danh sách các tác giả dưới dạng JSON
@router.post("/", response_model = AuthorSchema) # định nghĩa một endpoint POST tại đường dẫn gốc của router này, tức là /authors/
def create_author(author_in: AuthorCreate, db: Session = Depends(get_db)):
    new_author = AuthorModel(
        name = author_in.name,
        bio = author_in.bio
    )
    db.add(new_author)
    db.commit() # commit phiên làm việc để lưu thay đổi vào cơ sở dữ liệu
    db.refresh(new_author) # làm mới đối tượng để lấy thông tin đã được cập nhật từ cơ sở dữ liệu
    return new_author # trả về thông tin của tác giả vừa được tạo dưới dạng JSON
@router.get("/{author_id}", response_model = AuthorSchema) # định nghĩa một endpoint GET tại đường dẫn /{author_id}, tức là /authors/{author_id}
def get_author(author_id : int, db: Session = Depends(get_db)):
    author = db.query(AuthorModel).filter(AuthorModel.id == author_id).first() # truy vấn cơ sở dữ liệu để lấy thông tin chi tiết của tác giả có ID tương ứng
    if not author: # nếu không tìm thấy tác giả nào có ID tương ứng, trả về lỗi 404 Not Found
        raise HTTPException(status_code=404, detail="Not found")
    return author # trả về thông tin của tác giả dưới dạng JSON
@router.put("/{author_id}", response_model = AuthorSchema) # định nghĩa một endpoint PUT tại đường dẫn /{author_id}, tức là /authors/{author_id}
def update_author(author_id: int, author: AuthorSchema, db: Session = Depends(get_db)):
    db_author = db.query(AuthorModel).filter(AuthorModel.id == author_id).first() # truy vấn cơ sở dữ liệu để lấy thông tin chi tiết của tác giả có ID tương ứng
    if not db_author: # nếu không tìm thấy tác giả nào có ID tương ứng, trả về lỗi 404 Not Found
        raise HTTPException(status_code=404, detail="Not found")
    db_author.name = author.name # cập nhật tên của tác giả với giá trị mới được gửi trong yêu cầu
    db_author.bio = author.bio # cập nhật tiểu sử của tác giả với giá trị mới được gửi trong yêu cầu
    db.commit() # commit phiên làm việc để lưu thay đổi vào cơ sở dữ liệu
    db.refresh(db_author) # làm mới đối tượng để lấy thông tin đã được cập nhật từ cơ sở dữ liệu
    return db_author # trả về thông tin của tác giả đã được cập nhật dưới dạng JSON
@router.delete("/{author_id}", status_code=204) # định nghĩa một endpoint DELETE tại đường dẫn /{author_id}, tức là /authors/{author_id}
def delete_author(author_id: int, db: Session = Depends(get_db)):
    db_author = db.query(AuthorModel).filter(AuthorModel.id == author_id).first() # truy vấn cơ sở dữ liệu để lấy thông tin chi tiết của tác giả có ID tương ứng
    if not db_author: # nếu không tìm thấy tác giả nào có ID tương ứng, trả về lỗi 404 Not Found
        raise HTTPException(status_code=404, detail="Not found")
    db.delete(db_author) # xóa tác giả khỏi cơ sở dữ liệu
    db.commit() # commit phiên làm việc để lưu thay đổi vào cơ sở dữ liệu
    return None # trả về None để chỉ ra rằng tác giả đã được xóa thành công
