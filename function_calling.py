import requests
from google import genai
import json
import os

key = os.getenv('API_KEY')

client= genai.Client(api_key=key)
