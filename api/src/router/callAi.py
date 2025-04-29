import requests
from pydantic import BaseModel
from src.router.broadcast import broadcast
from fastapi import APIRouter
from fastapi import HTTPException
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
import asyncio


class Item(BaseModel):
    baseLanguage: str
    text: str


class TradPanel:
    baseLanguage: str
    destinationLanguage: str
    text: str

    def __init__(self, baseLanguage, destinationLanguage, text):
        self.baseLanguage = baseLanguage
        self.destinationLanguage = destinationLanguage
        self.text = text


prompt_router = APIRouter()

language_map = {
    "EN": "english",
    "FR": "french",
    "CH": "chinese",
    "ES": "spanish",
}


@prompt_router.post("/prompt")
async def prompt(item: Item):
    tasks = []

    for code, _ in language_map.items():
        tasks.append(
            generate(
                TradPanel(
                    baseLanguage=item.baseLanguage,
                    destinationLanguage=code,
                    text=item.text,
                )
            )
        )
    await asyncio.gather(*tasks)


async def generate(item: TradPanel):
    model = "7shi/llama-translate:8b-q4_K_M"
    try:
        llm = OllamaLLM(model=model, base_url="ai:11434")

        template = """### Instruction:
Translate {baseLanguage} to {destinationLanguage}.

### Input:
{text}

### Response:
"""

        prompt = ChatPromptTemplate.from_template(template)
        chain = prompt | llm
        idx = 0
        async for chunk in chain.astream(
            {
                "baseLanguage": item.baseLanguage,
                "destinationLanguage": language_map[item.destinationLanguage],
                "text": item.text,
            }
        ):
            await broadcast(
                item.destinationLanguage,
                f'{{"start": {str(idx == 0).lower()}, "data": "{chunk}"}}',
            )
            idx += 1
    except requests.RequestException as e:
        raise HTTPException(
            status_code=500, detail=f"Error communicating with Ollama: {str(e)}"
        )
