from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, FileResponse, HTMLResponse
from pipeline import Pipeline
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
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

pipeline = Pipeline(os.path.join(os.getcwd(), 'corpus'))
pipeline.start()


@app.get("/", response_class=FileResponse)
def read_index(request: Request):
    path = 'static/index.html'
    return FileResponse(path)


@app.get("/query")
def query_docs(value: str = ""):
    pipeline.process_query(value)
    return pipeline.retrive_docs()


@app.get("/readfile")
def read_file(id: str):
    pass
