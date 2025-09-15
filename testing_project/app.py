from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
import os

# Define the data model for the incoming request for better validation
class UserRequest(BaseModel):
    message: str

# Initialize the FastAPI app
app = FastAPI()

# Add CORS middleware to allow cross-origin requests
# This is important for when you have a separate frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Define the root endpoint for a simple health check
@app.get("/")
def read_root():
    return {"status": "API is running"}

# Define the chatbot endpoint
@app.post("/chatbot")
async def chatbot(request: UserRequest):
    """
    Receives a user message, processes it with a LangChain chain,
    and returns the model's reply.
    """
    # Note: OPENAI_API_KEY is read from Vercel's environment variables
    llm = ChatOpenAI(model="gpt-4o-mini")
    
    # Create the chain
    chain = llm | StrOutputParser()
    
    # Get the message from the validated request
    message = request.message
    
    # Invoke the chain with the user's message
    result = chain.invoke(message)
    
    return {"reply": result}
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))  # must use $PORT
    uvicorn.run(app, host="0.0.0.0", port=port)