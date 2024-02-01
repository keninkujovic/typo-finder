import redis
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from starlette.concurrency import run_in_threadpool
from starlette.middleware.base import BaseHTTPMiddleware
from symspellpy import SymSpell

from sym import findTypos

Redis = redis.Redis(host="redis", decode_responses=True)

class CounterMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        if request.url.path == "/api/typo-check/":
            await run_in_threadpool(Redis.incr, "total_api_calls")
        return response

class Text(BaseModel):
    text: str

app = FastAPI()
api_router = FastAPI()

app.add_middleware(CounterMiddleware)

@app.on_event("startup")
async def startup_event():
    global sym_spell
    sym_spell = SymSpell()
    dictionary_path = "words.txt"
    sym_spell.create_dictionary(dictionary_path)

@app.get("/total-calls/")
async def total_calls():
    return await run_in_threadpool(Redis.get, "total_api_calls")

@app.post("/api/typo-check/")
async def post(body: Text):
    print(sym_spell.words)
    return findTypos(sym_spell, body.text, max_suggestions=3)

@app.get("/")
async def home():
    with open("index.html", "r") as file:
            html_content = file.read()
    return HTMLResponse(content=html_content)

@app.get("/contact/")
async def contact():
    with open("contact.html", "r") as file:
            html_content = file.read()
    return HTMLResponse(content=html_content)
