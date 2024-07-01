from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai.chat_models.base import ChatOpenAI
from app.schemas import QueryRequest, QueryResponse


router = APIRouter(tags=["LLM"])

llm = ChatOpenAI(
    base_url="http://localhost:8080/v1",
    api_key="not-needed",
    model="gpt-3.5-turbo-0613",
    max_tokens=128,
    temperature=0.2,
    streaming=True,
)

# helper functions
# async def event_generator(messages):
def event_generator(messages):
    for chunk in llm.stream(messages):
        yield chunk.content

@router.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    messages = [
        SystemMessage(
            content="""
            You are a helpful Assistant, you can handle complex, logic-based queries.
            Always provide helpful answers only and your answer should be within 80 words limit.
            """
        ),
        HumanMessage(content=request.content),
    ]

    response = llm.invoke(messages)
    print(response)
    return {"response": response.content}


@router.post("/query_stream")
async def query_stream(request: QueryRequest):
    messages = [
        SystemMessage(
            content="""
            You are a helpful Assistant, you can handle complex, logic-based queries.
            Always provide helpful answers only and your answer should be within 80 words limit.
            """
        ),
        HumanMessage(content=request.content),
    ]

    return StreamingResponse(
        event_generator(messages=messages),
        # media_type="text/plain",
        media_type="text/event-stream",
        )
