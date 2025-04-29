from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
from src.router.router import global_router
from src.router.callAi import prompt_router
from src.router.broadcast import broadcast_router
import requests
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(global_router)
app.include_router(prompt_router)
app.include_router(broadcast_router)


def check_if_model_exist(model_name, model_array):
    for model in model_array:
        if (model['name'] == model_name):
           return True
    return False

def check_for_models():
    models_to_install = [{"name": "smollm2:latest"}]
    host = f"ai:{os.getenv("IA_PORT")}"

    get_models_url = f"http://{host}/api/tags"
    install_models_url = f"http://{host}/api/pull"

    for model in models_to_install:
        get_response = requests.get(get_models_url)
        if get_response.status_code == 200:
            models = json.loads(get_response.content.decode("utf-8"))
            if (not check_if_model_exist(model["name"], models["models"])):
                requests.post(install_models_url, json=model)


if __name__ == "__main__":
    print("start")
    check_for_models()
    uvicorn.run(
        "src.main:app",
        host=os.getenv("API_HOST"),
        port=int(os.getenv("API_PORT")),
        reload=True,
    )
