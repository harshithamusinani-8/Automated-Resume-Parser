from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from parser.pdf_parser import extract_text_from_pdf
from parser.nlp_parser import parse_resume

import os


app = FastAPI()

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    with open(
        "templates/index.html",
        "r",
        encoding="utf-8"
    ) as file:
        return file.read()


@app.post("/upload-resume")
async def upload_resume(
    file: UploadFile = File(...)
):
    if not file.filename.lower().endswith(".pdf"):
        return {
            "message": "Only PDF files are supported currently"
        }

    file_path = os.path.join(
        UPLOAD_FOLDER,
        file.filename
    )

    contents = await file.read()

    with open(file_path, "wb") as f:
        f.write(contents)

    text = extract_text_from_pdf(file_path)

    parsed_data = parse_resume(text)

    return {
        "filename": file.filename,
        "message": "Resume uploaded and analyzed successfully",
        "data": parsed_data
    }
