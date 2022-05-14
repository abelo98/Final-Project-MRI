from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, FileResponse, HTMLResponse
from pipeline import Pipeline
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


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

pipeline = None


@app.get("/", response_class=FileResponse)
def read_index(request: Request):
    path = 'static/index.html'
    return FileResponse(path)


@app.post("/corpus")
async def set_corpus(path: Item):
    print(path.path)
    pipeline = Pipeline(path)
    pipeline.start()


@app.get("/query")
def query_docs(value: str = ""):
    pipeline.process_query(value)
    return pipeline.retrive_docs()
