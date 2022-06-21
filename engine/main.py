from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, FileResponse, HTMLResponse
from core import Core
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from uuid import UUID
import os


class Item(BaseModel):
    path: str


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="./static"), name="static")

pipeline = Core(os.path.join(os.getcwd(), 'corpus'))
pipeline.start()


@app.get("/", response_class=FileResponse)
def read_index(request: Request):
    path = 'static/index.html'
    return FileResponse(path)


@app.get("/query")
def query_docs(value: str = ""):
    q_w = pipeline.process_query(value)
    file_paths_and_ids = pipeline.retrieve_id_docs(q_w)
    s = pipeline.get_subjects(file_paths_and_ids)
    response = pipeline.make_response(file_paths_and_ids, s)
    print(s)

    return response


@app.get("/document/id/{id}")
def read_file(id: str):
    return pipeline.retrieve_doc(UUID(id))
