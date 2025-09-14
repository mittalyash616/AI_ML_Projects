from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
import os
from mangum import Mangum  # ✅ Needed for Vercel/AWS Lambda

app = FastAPI()

llm = ChatOpenAI(model="gpt-4o-mini", api_key=os.getenv("OPENAI_API_KEY"))

# ✅ Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this to your frontend domain later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Query(BaseModel):
    question: str

@app.post("/ask")
async def ask_agent(query: Query):
    try:
        response = llm.invoke(query.question)
        return {"answer": response.content}
    except Exception as e:
        return {"error": str(e)}

# ✅ Vercel entrypoint
handler = Mangum(app)
