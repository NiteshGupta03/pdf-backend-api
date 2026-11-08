import os
import shutil
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pdf2docx import Converter

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "PDF Converter API is Active"}

@app.post("/convert")
async def convert(file: UploadFile = File(...)):
    temp_pdf = f"temp_{file.filename}"
    temp_docx = f"converted_{file.filename.replace('.pdf', '.docx')}"

    with open(temp_pdf, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        cv = Converter(temp_pdf)
        cv.convert(temp_docx, start=0, end=None)
        cv.close()

        return FileResponse(
            temp_docx,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            filename=temp_docx
        )
    finally:
        if os.path.exists(temp_pdf):
            os.remove(temp_pdf)
