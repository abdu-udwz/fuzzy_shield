import json
import logging
import traceback
from contextlib import asynccontextmanager
from asyncio.queues import QueueEmpty

from fastapi import FastAPI, WebSocket
from fastapi.websockets import WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fuzzy_shield.routers import api_router
from fuzzy_shield.services.queues import EXTERNAL_UPDATES_QUEUE
from fuzzy_shield.config import Config
from fuzzy_shield import data
from fuzzy_shield import dependencies
from fuzzy_shield import services

config = Config()
logger = logging.getLogger("fuzzy_shield_app")

# Prepare datasets
data.initialize()  # specify sample sizes

# Webserver initialization

origins = [
    "http://localhost",
    "http://localhost:8080",
]


@asynccontextmanager
async def lifespan(app: FastAPI):
    await dependencies.on_startup(app)
    services.on_startup(app)
    yield
    services.on_shutdown(app)
    await dependencies.on_shutdown(app)


app = FastAPI(lifespan=lifespan)
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.websocket("/api/ws/")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            update = await EXTERNAL_UPDATES_QUEUE.get()
            await websocket.send_text(json.dumps(update))
            EXTERNAL_UPDATES_QUEUE.task_done()

    except WebSocketDisconnect as err:
        print("WebSocketConnection closed")
        print(traceback.format_exc())
        print('sss', err, err.reason, err.code, err.args)
    except Exception as err:
        print('Something went wrong', err)


class SPAStaticFiles(StaticFiles):
    async def get_response(self, path: str, scope):
        response = await super().get_response(path, scope)
        if response.status_code == 404:
            response = await super().get_response('.', scope)
        return response


app.mount('/app/', SPAStaticFiles(directory='public',
          html=True), name='whatever')

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9090)
