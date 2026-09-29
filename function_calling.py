import requests
from google import genai
import json
import os
from dotenv import load_dotenv

load_dotenv()

key = os.getenv('API_KEY')

client= genai.Client(api_key=key)


