from typing import Generator
from app.db.session import SessionLocal
def get_db() -> Generator:
    db = SessionLocal() # tạo một phiên làm việc mới với cơ sở dữ liệu
    try:
        yield db # trả về phiên làm việc này để sử dụng trong các endpoint
    finally:
        db.close() # đảm bảo rằng phiên làm việc được đóng sau khi sử dụng xong, tránh rò rỉ kết nối