from pydantic import BaseModel


# schemas
class QueryRequest(BaseModel):
    content: str = "wirte me a poem about mighty Himalayas."

class QueryResponse(BaseModel):
    response: str
