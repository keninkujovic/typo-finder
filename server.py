from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import HTMLResponse

from main import TST, findTypos, loadDictionary

class Text(BaseModel):
    text: str

app = FastAPI()
tst = TST()

@app.on_event("startup")
async def startup_event():
    loadDictionary(tst, "dictionary.txt")

@app.post("/api/typo-check/")
async def post(body: Text):
    return findTypos(tst, body.text)

@app.get("/")
async def home():
    with open("index.html", "r") as file:
            html_content = file.read()
    return HTMLResponse(content=html_content)
