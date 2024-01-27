import redis
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.concurrency import run_in_threadpool

from main import TST, findTypos, loadDictionary

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
tst = TST()

app.add_middleware(CounterMiddleware)

@app.on_event("startup")
async def startup_event():
    loadDictionary(tst, "dictionary.txt")

@app.get("/total-calls/")
async def total_calls():
    return await run_in_threadpool(Redis.get, "total_api_calls")

@app.post("/api/typo-check/")
async def post(body: Text):
    return findTypos(tst, body.text)

@app.get("/")
async def home():
    with open("index.html", "r") as file:
            html_content = file.read()
    return HTMLResponse(content=html_content)
