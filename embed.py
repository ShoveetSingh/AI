import numpy as np
from google import genai
import faiss
import os
from dotenv import load_dotenv

load_dotenv()

key = os.getenv('API_KEY')

def cosine_similarity(x,y):
    output= np.dot(x,y)/(np.linalg.norm(x)*np.linalg.norm(y))
    return output

client = genai.Client(api_key=key)

documents = [
    "FastAPI is a Python framework for building APIs.",
    "FastAPI supports asynchronous programming.",
    "Bananas are rich in potassium.",
    "Python is commonly used in machine learning."
]

embeddings =[]

for document in documents:
    result=client.models.embed_content(
    model='gemini-embedding-2',
    contents=document
    )
    embeddings.append(result.embeddings[0].values)

query = "What can I use to build a Python API?"

result=client.models.embed_content(
    model='gemini-embedding-2',
    contents=query
    )

scores = []
c=0
query_result=result.embeddings[0].values

for embed in embeddings:
    cosine_score = cosine_similarity(embed,query_result)
    scores.append((documents[c],cosine_score))
    c=c+1
scores.sort(key=lambda x : x[1],reverse=True)

for s in scores:
    print(s[0],s[1])

embed_matrix = np.array(embeddings).astype('float32')

faiss.normalize_L2(embed_matrix)
dimension=embed_matrix.shape[1]
index = faiss.IndexFlatIP(dimension)
index.add(embed_matrix)

query_vector = np.array([query_result]).astype('float32')

faiss.normalize_L2(query_vector)

scores,indices = index.search(query_vector,k=2)

context=[]
for i in indices[0]:
    print(documents[i])
    context.append(documents[i])

prompt = f"""
You are an ai tutor.

 Context:
  {context}

Question:
{query}
"""

response = client.interactions.create(
        model="gemini-3.8-flash",
        input=prompt
)

print(response.output_text)

