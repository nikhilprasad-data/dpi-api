from fastapi import APIRouter, UploadFile, File, HTTPException, status
from src.schemas import UploadResponse
import os
import shutil

upload_router = APIRouter()

DATA_DIR = "src/data"

@upload_router.post('/upload', response_model=UploadResponse, status_code=status.HTTP_201_CREATED)
async def upload(file: UploadFile = File(...)):
     
     if not file.filename.endswith(".pdf"):
          raise HTTPException(
               status_code=status.HTTP_400_BAD_REQUEST,
               detail="Only PDF files are allowed for RAG ingestion."
          )

     os.makedirs(DATA_DIR, exist_ok=True)
     file_path = os.path.join(DATA_DIR, file.filename)

     try:
          with open(file_path, "wb") as buffer:
               shutil.copyfileobj(file.file, buffer)
     
     except Exception as e:
          raise HTTPException(
               status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
               detail=f"Could not save the file: {str(e)}"
          )
     
     finally:
          file.file.close()

     return {
          "message": "File uploaded successfully",
          "filename": file.filename,
          "path": file_path
     }
