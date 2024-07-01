import requests

url = "http://localhost:8000/query_stream"
data = {"content": "wirte me a poem about mighty Himalayas."}

response = requests.post(url, json=data, stream=True)
for chunk in response.iter_content(chunk_size=None):
    if chunk:
        print(chunk.decode(), end='', flush=True)