import os
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
GROQ_API_KEY = "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"

app = FastAPI()

# ---------- Custom Groq Chat Function ----------
def groq_chat(context, question, model="llama3-8b-8192"):
    client = Groq(api_key=GROQ_API_KEY)
    try:
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant. Answer questions based only on the provided context."},
                {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"}
            ],
            temperature=0.2,
            top_p=1,
            stream=False
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        return f"Error from Groq API: {e}"

# ---------- Request Models ----------
class SummarizeRequest(BaseModel):
    content: str

class ChatRequest(BaseModel):
    question: str
    context: str  # This can be the summarized content

# ---------- Routes ----------
@app.post("/summarize")
async def summarize(request: SummarizeRequest):
    summary = groq_chat(request.content, "Summarize the content above in clear and simple terms.")
    return {"summary": summary}

@app.post("/chat")
async def chat(request: ChatRequest):
    answer = groq_chat(request.context, request.question)
    return {"answer": answer}
