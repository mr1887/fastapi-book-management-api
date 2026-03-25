from sqlalchemy import Column, DateTime, ForeignKey, Integer,String, Text, func , text # truy cập vào các lớp và hàm cần thiết từ SQLAlchemy để định nghĩa mô hình cơ sở dữ liệu
from sqlalchemy.orm import relationship # để thiết lập mối quan hệ giữa các bảng trong cơ sở dữ liệu
from sqlalchemy.sql import func
from app.db.base import Base

class Book(Base): # định nghĩa lớp Author kế thừa từ Base, đây sẽ là mô hình cơ sở dữ liệu cho bảng tác giả
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True) # cột id là khóa chính và có chỉ mục để tăng tốc độ truy vấn
    title = Column(String(255), nullable = False, index = True)
    description = Column(Text, nullable = True)
    published_years = Column(Text, nullable = True)

    author_id = Column(Integer, ForeignKey("authors.id", ondelete= "RESTRICT"), nullable = False) # khóa ngoại liên kết với bảng tác giả, mỗi sách phải thuộc về một tác giả
    category_id = Column(Integer, ForeignKey("categories.id", ondelete= "RESTRICT"), nullable = False) # khóa ngoại liên kết với bảng thể loại, mỗi sách phải thuộc về một thể loại

    cover_image = Column(String(255), nullable = True) # cột để lưu đường dẫn đến ảnh bìa của sách, có thể để trống nếu không có ảnh
    # lưu path, ví dụ "static/covers/book1.jpg"

    created_at = Column(DateTime(timezone = True), server_default = func.now(),nullable = False) # cột để lưu thời gian tạo bản ghi, mặc định là thời gian hiện tại khi bản ghi được tạo
    updated_at = Column(DateTime(timezone = True), server_default = func.now(), onupdate=func.now(),nullable = False) # cột để lưu thời gian cập nhật bản ghi, mặc định là thời gian hiện tại khi bản ghi được tạo và sẽ tự động cập nhật khi bản ghi được sửa đổi

    # mối quan hệ 1-n với Book
    author = relationship("Author", back_populates="books") # thiết lập mối quan hệ với bảng sách, mỗi tác giả có thể có nhiều sách
    category = relationship("Category", back_populates="books") # thiết lập mối quan hệ với bảng sách, mỗi thể loại có thể có nhiều sách