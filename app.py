from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from openai import OpenAI
import httpx
import os
from dotenv import load_dotenv

# Load env vars from .env in local development
load_dotenv()

# Custom HTTP client with proxies disabled
http_client = httpx.Client(proxy=None)

# Initialize OpenAI client with env vars
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL"),  # e.g., https://aipipe.org/openai/v1
    http_client=http_client
)

app = FastAPI()

@app.post("/")
async def answer_questions(questions_file: UploadFile = File(...)):
    text = (await questions_file.read()).decode("utf-8")

    prompt = f"""
You are a question answering assistant.
Below is some text that may include context and a list of questions.

{text}

Instructions:
1. Read the text and find the answers to the questions.
2. Answer each question in order.
3. Respond ONLY as a valid JSON array of answers in the same order.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    model_output = response.choices[0].message.content.strip()

    return JSONResponse(
        content=model_output,
        headers={"X-Email": "23f3001468@ds.study.iitm.ac.in"}
    )
