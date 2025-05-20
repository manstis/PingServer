from fastapi import FastAPI, APIRouter, Request
from starlette.responses import PlainTextResponse

router = APIRouter(tags=["api"])
app = FastAPI(
    title="PingServer",
    description="Pong's your message",
    version="0.1.0",
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)

@router.get("/ping")
def handler(request: Request, message: str) -> PlainTextResponse:
    return f"pong, {message}"

app.include_router(router)