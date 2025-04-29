import json
from pydantic import BaseModel
from fastapi import APIRouter
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate


class Item(BaseModel):
    text: str


prompt_router = APIRouter()


@prompt_router.post("/prompt")
async def prompt(item: Item):
    return query_ollama(item.text)


def query_ollama(question):
    prompt = ChatPromptTemplate.from_messages(
        [
            ("human", 'Now process the following input:\n"{question}"'),
        ]
    )

    llm = OllamaLLM(model="question_bot", base_url="ai:11434")
    chain = prompt | llm

    try:
        response = chain.invoke({"question": question})
        return json.loads(response)
    except Exception as e:
        print(f"Error: {e}")
        return None
