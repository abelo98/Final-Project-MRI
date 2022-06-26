import re

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from constants import *
from core import Core


class FeedbackBody(BaseModel):
    type: int
    query: str


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="./static"), name="static")

core = Core(CRAN_CORPUS)


@app.get("/", response_class=FileResponse)
def read_index(request: Request):
    path = 'static/index.html'
    return FileResponse(path)


@app.get("/vect/query")
def query_vect_docs(value: str = "", corpus: str = "CRAN CORPUS"):
    core.load_vectorial_model(Core.process_corpus_name(corpus))

    q_w = core.vsm.process_query(value, query_process=core.query_processor)
    file_paths_and_ids = core.vsm.retrieve_id_docs(q_w)
    s = core.get_subjects(file_paths_and_ids)
    response = core.make_response(file_paths_and_ids, s)

    return response


@app.get("/bool/query")
def query_bool_docs(value: str = "", corpus: str = "CRAN CORPUS"):
    core.load_boolean_model(Core.process_corpus_name(corpus))

    file_paths_and_ids_boolean = core.boolean_model.boolean_model_retrieve_docs(value)
    subjects = core.get_subjects(file_paths_and_ids_boolean)
    response = core.make_response(file_paths_and_ids_boolean, subjects)

    return response


@app.get("/document/id/{id}")
def read_file(id: str):
    text = core.retrieve_doc(id)
    return re.sub('\n', '', text)


@app.put("/feedback/{doc_id}")
def feedback(doc_id: int, body: FeedbackBody):
    return core.set_feedback(body.type, doc_id, None)


@app.get("/query/similar")
def get_similar():
    return core.get_similar()
