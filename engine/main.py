from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, FileResponse, HTMLResponse
from pipeline import Pipeline
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:8081",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="./static"), name="static")

pipeline = None


@app.get("/", response_class=FileResponse)
def read_index(request: Request):
    pipeline = Pipeline('')
    pipeline.start()

    path = 'static/index.html'
    return FileResponse(path)


@app.get("/query")
def query_docs(value: str = ""):
    pipeline.process_query(value)

    return pipeline.retrive_docs()
