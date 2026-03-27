from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api.endpoints import authors, books, categoryes
from app.core.config import settings
# Create FastAPI application instance
app = FastAPI(
    title = "Book Management API",
    description = "A simple FastAPI to managebook,authors,categories and book covers",
    version = "1.0.0" # API version
)
app.mount("/static", StaticFiles(directory = "app/static"),name ="static")
# them router cho các endpoint liên quan đến sách, tác giả và thể loại
app.include_router(authors.router, prefix="/authors", tags=["authors"])
app.include_router(books.router, prefix="/books", tags=["books"])
app.include_router(categoryes.router, prefix="/categories", tags=["categories"])

# static files for cover image 
@app.get("/") # đây là route gốc, khi truy cập vào đường dẫn gốc của API sẽ trả về thông tin này
def read_root():
    return {"message": "Welcome to the Book Management API!1"}