from fastapi import FastAPI,Body
import os 
from langchain_openai import ChatOpenAI
from langchain_core.prompts import  ChatPromptTemplate
from pydantic import BaseModel

from fastapi.middleware.cors import CORSMiddleware


from dotenv import load_dotenv
load_dotenv()

app=FastAPI()
# Add CORS middleware to allow requests from any origin during development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

#Chat model initialization
model=ChatOpenAI(api_key=os.getenv("OPENAI_API_KEY"),temperature=0.7)

class ChatRequest(BaseModel):
    message: str
    temperature: float = 0.7
    model_name: str = "gpt-4o-mini"

    class Config:
        schema_extra = {
            "example": {
                "message": "Write a short poem about the ocean",
                "temperature": 0.8,
                "model_name": "gpt-4o-mini"
            }
        }

@app.get("/")
def root():
    return {"message": "Welcome to Langchain with FastAPI"}

@app.post("/chat")
def chat_endpoint(chatrequest: ChatRequest = Body(...)):
    model=ChatOpenAI(api_key=os.getenv("OPENAI_API_KEY")
                    ,temperature=chatrequest.temperature
                    ,model_name=chatrequest.model_name
                    ,max_retries=2)
    
    message=chatrequest.message

    prompt=ChatPromptTemplate.from_messages(
        [("system", "You are a helpful assistant."),
         ("user", "{message}")
        ])
    chain=prompt | model 
    return chain.invoke({"message":message})
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)

