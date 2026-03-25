from sqlalchemy.orm import declarative_base


Base  = declarative_base()
# Import models từ Alembic sẽ tự động nhận diện các mô hình cơ sở dữ liệu được định nghĩa trong thư mục models và tạo bảng tương ứng trong cơ sở dữ liệu khi chạy lệnh migration.


