import re
from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline

app = FastAPI(title="AMD AI Inference Server")

sentiment_model = pipeline("sentiment-analysis")

class TextInput(BaseModel):
    text: str


def calculator(expr: str):
    try:
        return eval(expr)
    except:
        return "Invalid math expression."


def agent_router(query: str):
    # crude routing logic
    if re.search(r"\d", query):
        return {
            "tool": "calculator",
            "output": calculator(query)
        }

    sentiment = sentiment_model(query)
    return {
        "tool": "sentiment_model",
        "output": sentiment
    }


@app.post("/agent")
def run_agent(data: TextInput):
    return agent_router(data.text)
