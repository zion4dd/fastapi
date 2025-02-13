from fastapi import FastAPI, UploadFile
from fastapi.responses import FileResponse, StreamingResponse

app = FastAPI()


@app.post("/file/")
async def upload_file(uploaded_file: UploadFile):
    file = uploaded_file.file
    filename = uploaded_file.filename
    size = uploaded_file.size
    with open(f"1_{filename}", "wb") as f:
        f.write(file.read())


@app.post("/files/")
async def upload_files(uploaded_files: list[UploadFile]):
    for uploaded_file in uploaded_files:
        file = uploaded_file.file
        filename = uploaded_file.filename
        with open(f"1_{filename}", "wb") as f:
            f.write(file.read())


@app.get("/files/{filename}/")
async def get_file(filename: str):
    return FileResponse(filename)


def iterfile(filename: str):
    with open(filename, "rb") as f:
        while chunk := f.read(1024 * 1024):
            yield chunk


@app.get("/files/stream/{filename}/")
async def get_file_streaming(filename: str):
    return StreamingResponse(iterfile(filename), media_type="video/mp4")


# тип файла нужно указывать для каждого файла. брать из файла или БД
