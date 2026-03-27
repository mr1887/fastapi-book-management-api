from fastapi import APIRouter
router = APIRouter() # tạo một router mới để quản lý các endpoint liên quan đến tác giả
@router.get("/", response_model=List[BookSchema]) # định nghĩa một endpoint GET tại đường dẫn gốc của router này, tức là /books/
def list_books(db: Session = Depends(get_db),
               skip : int = 0, limit : int = 100,
               author_id: int| None = Query(None),
               category_id: int| None = Query(None),
               
               year: int | None = Query(None),
               keyword: str | None = Query(None)):
    """
    lấy danh sách tất cả các sách, có hỗ trợ phân trang thông qua các tham số skip và limit.
    - author_id để lọc sách theo tác giả
    - category_id để lọc sách theo thể loại
    - year(published_year)
    - keyword(tìm kiếm theo tiêu đề hoặc mô tả)
    """
    query = db.query(BookModel) # bắt đầu một truy vấn để lấy danh sách các sách từ cơ sở dữ liệu
    if author_id is not None:
        query = query.filter(BookModel.author_id == author_id)
    if category_id is not None:
        query = query.filter(BookModel.category_id == category_id)
    if year is not None:
        query = query.filter(BookModel.published_years == year)
    if keyword is not None:
        like_pattern = f"%{keyword}%" # tạo mẫu tìm kiếm với ký tự đại diện % để tìm kiếm chuỗi con trong tiêu đề hoặc mô tả
        query = query.filter(
            (BookModel.title.ilike(like_pattern)) | (BookModel.description.ilike(like_pattern))
        )
     # lọc sách dựa trên tiêu đề hoặc mô tả chứa từ khóa tìm kiếm, sử dụng ilike để thực hiện tìm kiếm không phân biệt chữ hoa chữ thường
    books = query.offset(skip).limit(limit).all() # truy vấn cơ sở dữ liệu để lấy danh sách các sách, áp dụng phân trang
    return books

@router.post("/", response_model = BookSchema) # định nghĩa một endpoint POST tại đường dẫn gốc của router này, tức là /books/
def create_book(book_in: BookCreate, db: Session = Depends(get_db)):
    new_book = BookModel(
        title = book_in.title,
        description = book_in.description,
        published_years = book_in.published_years,
        cover_image = book_in.cover_image,
        author_id = book_in.author_id,
        category_id = book_in.category_id
    )
    db.add(new_book)
    db.commit() # commit phiên làm việc để lưu thay đổi vào cơ sở dữ liệu
    db.refresh(new_book) # làm mới đối tượng để lấy thông tin đã được cập nhật từ cơ sở dữ liệu
    return new_book # trả về thông tin của sách vừa được tạo dưới dạng JSON

@router.get("/{book_id}", response_model = BookSchema) # định nghĩa một endpoint GET tại đường dẫn /{book_id}, tức là /books/{book_id}
def get_book(book_id : int, db: Session = Depends(get_db)):
    book = db.query(BookModel).filter(BookModel.id == book_id).first() # truy vấn cơ sở dữ liệu để lấy thông tin chi tiết của sách có ID tương ứng
    if not book: # nếu không tìm thấy sách nào có ID tương ứng, trả về lỗi 404 Not Found
        raise HTTPException(status_code=404, detail="Not found")
    return book # trả về thông tin của sách dưới dạng JSON

@router.put("/{book_id}", response_model = BookSchema) # định nghĩa một endpoint PUT tại đường dẫn /{book_id}, tức là /books/{book_id}
def update_book(book_id: int, book: BookUpdate, db: Session = Depends(get_db)):
    db_book = db.query(BookModel).filter(BookModel.id == book_id).first() # truy vấn cơ sở dữ liệu để lấy thông tin chi tiết của sách có ID tương ứng
    # ... đoạn trên giữ nguyên ...
    if not db_book:
        raise HTTPException(status_code=404, detail="Not found")

    # Lấy dữ liệu thực tế được gửi lên
    update_data = book.model_dump(exclude_unset=True)

    # Cập nhật tự động và thông minh
    for key, value in update_data.items():
        # Chặn các giá trị mặc định gây hại từ Swagger
        if value != "string" and (not isinstance(value, int) or value != 0): 
            # chỉ cập nhật những trường có giá trị thực sự được gửi lên, tránh ghi đè dữ liệu bằng các giá trị mặc định không mong muốn
            setattr(db_book, key, value)

    db.commit()
    db.refresh(db_book)
    return db_book

@router.delete("/{book_id}", status_code=204) # định nghĩa một endpoint DELETE tại đường dẫn /{book_id}, tức là /books/{book_id}
def delete_book(book_id: int, db: Session = Depends(get_db)):   

    db_book = db.query(BookModel).filter(BookModel.id == book_id).first()
    if not db_book: # nếu không tìm thấy sách nào có ID tương ứng, trả về lỗi 404 Not Found
        raise HTTPException(status_code=404, detail="Not found")
    db.delete(db_book)
    db.commit() # commit phiên làm việc để lưu thay đổi vào cơ sở dữ liệu
    db.refresh(db_book) # làm mới đối tượng để lấy thông tin đã được cập nhật từ cơ sở dữ liệu
    return None # trả về None để chỉ ra rằng sách đã được xóa thành công

@router.post("/{book_id}/covers", response_model = BookSchema)
async def up_load_book_cover(
    book_id : int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    up ảnh bìa 
    - allow jpg/png
    - save file in path: app/static/covers
    - update book.cover_image to URL/static/covers 

    """
    book = db.query(BookModel).filter(BookModel.id == book_id).first()
    if not book:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND ,
            detail ="Book not found"

        )
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail ="Invalid image type. Only JPEG and PNG are allowed"

        )
    contents = await file.read() # đọc file 
    max_size = 2 * 1024*1024 # 2mb
    if len(contents) > max_size:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "file so large. Max size is 2mb"

        )
    ext = os.path.splitext(file.filename)[1] # lấy đuôi file 
    filename = f"book_{book_id}_{uuid.uuid4().hex}{ext}" #tạo tên file duy nhất 
    file_path = COVERS_DIR /filename

    with open(file_path,"wb") as f:
        f.write(contents)
    book.cover_image = f"/static/covers/{filename}"
    db.add(book)
    db.commit()
    db.refresh(book)
    return book
    
