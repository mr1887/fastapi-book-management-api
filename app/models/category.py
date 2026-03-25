from sqlalchemy import Column, Integer,String, Text , text # truy cập vào các lớp và hàm cần thiết từ SQLAlchemy để định nghĩa mô hình cơ sở dữ liệu
from sqlalchemy.orm import relationship # để thiết lập mối quan hệ giữa các bảng trong cơ sở dữ liệu

from app.db.base import Base

class Category(Base): # định nghĩa lớp Author kế thừa từ Base, đây sẽ là mô hình cơ sở dữ liệu cho bảng tác giả
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True) # cột id là khóa chính và có chỉ mục để tăng tốc độ truy vấn
    name = Column(String(255), nullable = False, unique = True,index = True)
    description = Column(Text, nullable = True)

    # mối quan hệ 1-n với Book
    books = relationship("Book", back_populates="category") # thiết lập mối quan hệ với bảng sách, mỗi thể loại có thể có nhiều sách