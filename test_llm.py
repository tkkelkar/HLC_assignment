# import pytest
from fastapi.testclient import TestClient
from main import app
import tiktoken


client = TestClient(app)


def num_tokens_from_string(string: str, encoding_name: str =  "cl100k_base") -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens


def test_query():
    request_data = {"content": "Write me a poem about the mighty Himalayas."}
    response = client.post("/query", json=request_data)

    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert  num_tokens_from_string(data["response"]) <= 128

def test_query_stream():
    request_data = {"content": "Write me a poem about the mighty Himalayas."}
    response = client.post("/query_stream", json=request_data)

    assert response.status_code == 200
    chunks = [chunk for chunk in response.iter_text()]
    response_text = "".join(chunks)
    assert num_tokens_from_string(response_text) <= 128
