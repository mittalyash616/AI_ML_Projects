from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/chatbot")
async def chatbot(user: dict):
    llm = init_chat_model("gpt-4o-mini", model_provider="openai")
    chain = llm | StrOutputParser()
    message = user["message"]
    result = chain.invoke(message)
    return {"reply": result}
