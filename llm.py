from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

key = os.getenv('API_KEY')

app = FastAPI()

client = genai.Client(api_key=key)
class Request(BaseModel):
    input:str=''
    model:str='gemini-3.8-flash'

class Response(BaseModel):
   output_text:str

@app.post('/output',response_model=Response)
async def output(question:Request):
    response =  client.interactions.create(
        model=question.model,
        input=question.input,
    )
    return response.output_text

@app.get('/ask_ai/{question}')
async def ask_ai(question:str):
  
  response=await output(Request(input=question))
  return response