from google import genai
import faiss
import os

key = os.getenv('API_KEY')

client= genai.Client(api_key=key)

response = client.interactions.create(
    model="gemini-3.8-flash",
    input="""
    Extract information from this resume:

    John is a Python developer with 3 years of experience.
    He knows Python, FastAPI, Docker and PostgreSQL.
           """,
    response_format={
         'type':'array',
        'items':{
            'type':'object',
              "properties": {
                "name": {
                    "type": "string"
                },
                "experience_years": {
                    "type": "integer"
                },
                "skills": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    }
                }
            },
            'required':[
                'name','experience_years','skills'
            ]
        }
    },
)

print(response.output_text)