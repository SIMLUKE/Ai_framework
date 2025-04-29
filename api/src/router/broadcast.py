import os
from fastapi import APIRouter, WebSocket, Request, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from dataclasses import dataclass
from typing import Dict
import uuid
import json
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
import asyncio

templates = Jinja2Templates(directory="templates")


@dataclass
class ConnectionManager:
    def __init__(self) -> None:
        self.active_connections: dict = {}

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        id = str(uuid.uuid4())
        self.active_connections[id] = websocket

    async def send_message(self, ws: WebSocket, message: str):
        await ws.send_text(message)

    def find_connection_id(self, websocket: WebSocket):
        websocket_list = list(self.active_connections.values())
        id_list = list(self.active_connections.keys())

        pos = websocket_list.index(websocket)
        return id_list[pos]

    async def broadcast(self, data: str):
        for connection in self.active_connections.values():
            await connection.send_text(data)

    def disconnect(self, websocket: WebSocket):
        id = self.find_connection_id(websocket)
        del self.active_connections[id]

        return id


broadcast_router = APIRouter()
connection_manager_map = {
    "EN": ConnectionManager(),
    "FR": ConnectionManager(),
    "CH": ConnectionManager(),
    "ES": ConnectionManager(),
}


async def send_message(connection_manager: ConnectionManager, websocket: WebSocket):
    await connection_manager.connect(websocket)

    try:
        while True:
            await asyncio.sleep(1)
            await websocket.receive_text()
    except WebSocketDisconnect:
        id = connection_manager.disconnect(websocket)
        return RedirectResponse("/")


@broadcast_router.websocket("/message/EN")
async def websocket_endpoint_en(websocket: WebSocket):
    await send_message(connection_manager_map["EN"], websocket)


@broadcast_router.websocket("/message/FR")
async def websocket_endpoint_fr(websocket: WebSocket):
    await send_message(connection_manager_map["FR"], websocket)


@broadcast_router.websocket("/message/CH")
async def websocket_endpoint_ch(websocket: WebSocket):
    await send_message(connection_manager_map["CH"], websocket)


@broadcast_router.websocket("/message/ES")
async def websocket_endpoint_jp(websocket: WebSocket):
    await send_message(connection_manager_map["ES"], websocket)


async def broadcast(language: str, data: str):
    try:
        await connection_manager_map[language].broadcast(data)
    except:
        print("error with broadcasting language: " + language)
