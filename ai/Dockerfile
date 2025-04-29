FROM ollama/ollama:latest

EXPOSE 11434

VOLUME /root/.ollama

RUN apt-get update && apt-get install -y curl

RUN OLLAMA_NUM_PARALLEL=20

RUN ollama serve &
