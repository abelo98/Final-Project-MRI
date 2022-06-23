import os
from uuid import UUID

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

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

core = Core(os.path.join(os.getcwd(), 'corpus'))
core.start()


@app.get("/", response_class=FileResponse)
def read_index(request: Request):
    path = 'static/index.html'
    return FileResponse(path)


@app.get("/vect/query")
def query_vect_docs(value: str = ""):
    core.load_vectorial_model()

    q_w = core.vsm.process_query(value)
    file_paths_and_ids = core.vsm.retrieve_id_docs(q_w)
    s = core.get_subjects(file_paths_and_ids)
    response = core.make_response(file_paths_and_ids, s)

    return response


@app.get("/bool/query")
def query_bool_docs(value: str = ""):
    core.load_boolean_model()

    file_paths_and_ids_boolean = core.boolean_model.boolean_model_retrieve_docs(value)
    subjects = core.get_subjects(file_paths_and_ids_boolean)
    response = core.make_response(file_paths_and_ids_boolean, subjects)

    return response


@app.get("/document/id/{id}")
def read_file(id: str):
    return core.retrieve_doc(UUID(id))


@app.put("/feedback/{doc_id}")
def feedback(doc_id: int, body: FeedbackBody):
    return core.set_feedback(body.type, doc_id, body.query)
