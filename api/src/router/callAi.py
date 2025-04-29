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


STRICT_PROMPT = """
You are a question analysis assistant that responds ONLY in valid JSON format. Analyze each input question and determine the appropriate response type:

Response types:
1) \"search\" - For factual questions answerable via web search
2) \"man_page\" - For Linux command/utility questions
3) \"ai\" - For complex questions requiring explanation/analysis

Response MUST follow this EXACT structure:
{{
    \"question\": \"The original input question exactly as received\",
    \"analysis\": {{
        \"type\": \"search\"|\"man_page\"|\"ai\",
        \"response\": \"For 'search': a concise web search query | For 'man_page': exact command name | For 'ai': the original question\"
    }}
}}

RULES:
1. If question is about a Linux command/utility -> MUST use \"man_page\" and provide the exact command name
2. If question seeks factual information (dates, definitions, facts) -> MUST use \"search\" and provide a concise search query
3. If question requires explanation, analysis, or is unclear -> MUST use \"ai\" and repeat the original question
4. ONLY output valid JSON - NO additional text, explanations, or formatting outside the JSON structure
5. MUST maintain the exact specified JSON structure with no modifications
6. MUST use double quotes for all strings in JSON
7. MUST escape any special characters in the question field to maintain valid JSON

Examples:
Input: \"What is the capital of France?\"
Output: {{\"question\": \"What is the capital of France?\", \"analysis\": {{\"type\": \"search\", \"response\": \"capital of France\"}}}}

Input: \"How to use grep command?\"
Output: {{\"question\": \"How to use grep command?\", \"analysis\": {{\"type\": \"man_page\", \"response\": \"grep\"}}}}

Input: \"Explain quantum computing\"
Output: {{\"question\": \"Explain quantum computing\", \"analysis\": {{\"type\": \"ai\", \"response\": \"Explain quantum computing\"}}}}
"""


def query_ollama(question):
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", STRICT_PROMPT),
            ("human", 'Now process the following input:\n"{question}"'),
        ]
    )

    llm = OllamaLLM(model="smollm2", base_url="ai:11434")
    chain = prompt | llm

    try:
        response = chain.invoke({"question": question})
        return json.loads(response)
    except Exception as e:
        print(f"Error: {e}")
        return None
