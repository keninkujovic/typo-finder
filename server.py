import aioredis
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from starlette.middleware.base import BaseHTTPMiddleware

from main import TST, findTypos, loadDictionary

redis = aioredis.from_url("redis://redis", encoding="utf-8", decode_responses=True)

class CounterMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        response = await call_next(request)
        await redis.incr("total_api_calls")
        return response

class Text(BaseModel):
    text: str

app = FastAPI()
tst = TST()

app.add_middleware(CounterMiddleware)

@app.on_event("startup")
async def startup_event():
    loadDictionary(tst, "dictionary.txt")

@app.get("/total-calls/")
async def total_calls():
    return await redis.get("total_api_calls")

@app.post("/api/typo-check/")
async def post(body: Text):
    return findTypos(tst, body.text)

@app.get("/")
async def home():
    with open("index.html", "r") as file:
            html_content = file.read()
    return HTMLResponse(content=html_content)
