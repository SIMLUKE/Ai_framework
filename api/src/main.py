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


def create_model(ai_info):
    """
    Create a new model in Ollama using a Modelfile

    Args:
        modelfile_path (str): Path to the Modelfile
        model_name (str): Name for the new model
    """
    host = f"ai:{os.getenv('IA_PORT')}"
    url = f"http://{host}/api/create"

    with open(ai_info["SystemPath"], "r") as file:
        sys_content = file.read()

    payload = {
        "name": ai_info["name"],
        "from": ai_info["Source"],
        "system": sys_content,
    }

    response = requests.post(url, json=payload, stream=True)

    for line in response.iter_lines():
        if line:
            print(line.decode("utf-8"))


def check_if_model_exist(model_name, model_array):
    for model in model_array:
        if model["name"] == model_name:
            return True
    return False


def check_for_models():
    models_to_install = [{"name": "smollm2:latest"}]
    models_to_create = [
        {
            "name": "question_bot",
            "SystemPath": "./QuestionBotSystem",
            "Source": "smollm2:latest",
        }
    ]

    host = f"ai:{os.getenv('IA_PORT')}"
    get_models_url = f"http://{host}/api/tags"
    install_models_url = f"http://{host}/api/pull"

    get_response = requests.get(get_models_url)
    if get_response.status_code == 200:
        models = json.loads(get_response.content.decode("utf-8"))
        for model in models_to_install:
            if not check_if_model_exist(model["name"], models["models"]):
                requests.post(install_models_url, json=model)
        for model in models_to_create:
            if not check_if_model_exist(model["name"], models["models"]):
                create_model(model)


if __name__ == "__main__":
    print("start")
    check_for_models()
    uvicorn.run(
        "src.main:app",
        host=os.getenv("API_HOST"),
        port=int(os.getenv("API_PORT")),
        reload=True,
    )
