from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from app import models
from app import models
from app.api.deps import get_db
from app.schemas.category import Category as CategorySchema, CategoryCreate # Đây là Pydantic Schema
from app.models.category import Category as CategoryModel   # Đây là SQLAlchemy Model

router = APIRouter() # tạo một router mới để quản lý các endpoint liên quan đến tác giả
@router.get("/", response_model=List[CategorySchema]) # định nghĩa một endpoint GET tại đường dẫn gốc của router này, tức là /categories/
def list_categories(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)

): 
    """
    lấy danh sách tất cả các thể loại sách, có hỗ trợ phân trang thông qua các tham số skip và limit.
    """
    categories = db.query(CategoryModel).offset(skip).limit(limit).all() # truy vấn cơ sở dữ liệu để lấy danh sách các thể loại sách, áp dụng phân trang
    return categories # trả về danh sách các thể loại sách dưới dạng JSON
@router.get("/{category_id}", response_model=CategorySchema) # định nghĩa một endpoint GET tại đường dẫn /{category_id}, tức là /categories/{category_id}
def get_category(category_id: int, db: Session = Depends(get_db)):
    try:
        category = db.query(CategoryModel).filter(CategoryModel.id == category_id).first()
        if not category:
            raise HTTPException(status_code=404, detail="Not found")
        return category
    except Exception as e:
        print(f"Lỗi rồi : {e}") # Xem lỗi ở Terminal
        raise e
@router.post("/", response_model=CategorySchema, status_code=status.HTTP_201_CREATED) # định nghĩa một endpoint POST tại đường dẫn gốc của router này, tức là /categories/
def create_category(category_in: CategoryCreate, db: Session = Depends(get_db)):
    """
    Tạo một thể loại sách mới.
    """
    # 1. Tạo đối tượng Model (Dùng đúng tên đã import là CategoryModel)
    new_category = CategoryModel(
        name=category_in.name, 
        description=category_in.description
    )
    
    # 2. Lưu vào Database
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    
    # 3. Trả về đối tượng vừa tạo
    return new_category
@router.put("/{category_id}", response_model=CategorySchema) # định nghĩa một endpoint PUT tại đường dẫn /{category_id}, tức là /categories/{category_id}
def update_category(category_id: int, category: CategorySchema, db: Session = Depends(get_db)):
    """
    cập nhật thông tin của một thể loại sách dựa trên ID của nó và dữ liệu mới được gửi trong yêu cầu.
    """
    db_category = db.query(CategoryModel).filter(CategoryModel.id == category_id).first() # truy vấn cơ sở dữ liệu để lấy thông tin chi tiết của thể loại sách có ID tương ứng
    if not db_category: # nếu không tìm thấy thể loại sách nào có ID tương ứng, trả về lỗi 404 Not Found
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    
    db_category.name = category.name # cập nhật tên của thể loại sách với giá trị mới được gửi trong yêu cầu
    db_category.description = category.description # cập nhật mô tả của thể loại sách với giá trị mới được gửi trong yêu cầu
    db.commit() # commit phiên làm việc để lưu thay đổi vào cơ sở dữ liệu
    db.refresh(db_category) # làm mới đối tượng để lấy thông tin đã được cập nhật từ cơ sở dữ liệu
    return db_category # trả về thông tin của thể loại sách đã được cập nhật dưới dạng JSON
@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT) # định nghĩa một endpoint DELETE tại đường dẫn /{category_id}, tức là /categories/{category_id}
def delete_category(category_id: int, db: Session = Depends(get_db)):
    """
    xóa một thể loại sách dựa trên ID của nó.
    """
    db_category = db.query(CategoryModel).filter(CategoryModel.id == category_id).first() # truy vấn cơ sở dữ liệu để lấy thông tin chi tiết của thể loại sách có ID tương ứng
    if not db_category: # nếu không tìm thấy thể loại sách nào có ID tương ứng, trả về lỗi 404 Not Found
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    db.delete(db_category) # xóa đối tượng CategoryModel khỏi phiên làm việc của SQLAlchemy
    db.commit() # commit phiên làm việc để lưu thay đổi vào cơ sở dữ liệu
    return None # trả về None để chỉ ra rằng thể loại sách đã được xóa thành công