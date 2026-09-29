from google import genai

import pathlib
import os

key = os.getenv('API_KEY')

client= genai.Client(api_key=key)

# img =  client.files.upload(file="images.jpg")

# response = client.interactions.create(
#     model='gemini-3.8-flash',
#     input=[
#         {
#             'type':'text',
#             'text':'tell me the name of all the objects in this image.'
#         },
#         {
#             'type':'image',
#             'uri':img.uri,
#              "mime_type": img.mime_type
#         }
#     ]
# )

file_path = pathlib.Path('Shoveet_Singh_Resume_AI.docx')

sample_file=client.files.upload(file=file_path)

response =client.interactions.create(
    model='gemini-3.8-flash',
    input = [
        {
            'type':'text',
            'text':'rate my resume on a scale of 1 to 10.Also suggest improvements!'
        },
        {
            'type':'document',
            'uri':sample_file.uri,
            'mime_type':sample_file.mime_type
        }
    ]
)

print(response.output_text)