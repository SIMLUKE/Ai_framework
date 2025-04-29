import json
import re
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


def parseResponse(response):
    man_pref = "https://fr.manpages.org/"
    google_pref = "https://www.google.com/search?q="
    new_response = {}
    new_response["type"] = response["analysis"]["type"]
    new_response["valid"] = response["valid"]
    if response["analysis"]["type"] == "code":
        new_response["response"] = Query_bigollama(response["analysis"]["query"])
    if response["analysis"]["type"] == "man_page":
        new_response["response"] = f"{man_pref}{response['analysis']['query']}"
    if response["analysis"]["type"] == "search":
        new_response["response"] = (
            f"{google_pref}{response['analysis']['query'].replace(' ', '+')}"
        )
    if response["analysis"]["type"] == "error":
        new_response["response"] = response["analysis"]["query"]
    return new_response


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
        print(response)
        return parseResponse(json.loads(response))
    except Exception as e:
        print(f"Error: {e}")
        return None


def Query_bigollama(question):
    prompt = ChatPromptTemplate.from_messages(
        [
            ("human", 'Awnser this:\n"{question}"'),
        ]
    )

    llm = OllamaLLM(model="deepseek-r1:1.5b", base_url="ai:11434")
    chain = prompt | llm

    try:
        response = chain.invoke({"question": question})
        return re.sub(r"<think>.*?</think>", "", response, flags=re.DOTALL)
    except Exception as e:
        print(f"Error: {e}")
        return None
