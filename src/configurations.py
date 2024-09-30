from contextlib import asynccontextmanager
from fastapi import FastAPI
from langchain_ollama import OllamaLLM
from openai import OpenAI
import instructor
import os


os.environ["OPENAI_API_KEY"] = "NA"




@asynccontextmanager
async def lifespan(app: FastAPI):

    app.state.llm = OllamaLLM(
        model="llama3.1",
        base_url="http://localhost:11434"
    )
    app.state.client = instructor.patch(
        OpenAI(
            base_url="http://localhost:11434/v1",
            api_key="ollama",
        ),
        mode=instructor.Mode.JSON,
    )


    yield


