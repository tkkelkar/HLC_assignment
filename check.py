from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_openai.chat_models.base import ChatOpenAI
from langchain_openai import OpenAIEmbeddings

# llm = ChatOpenAI(
#     base_url="http://localhost:8080/v1",
#     api_key="not-needed",
#     model="gpt-3.5-turbo-0613",
#     max_tokens=128,
#     temperature=0.2,
#     streaming=True,
# )

# messages = [
#     SystemMessage(
#         content="""
#         You are a helpful Assistant, you can handle complex, logic-based queries.
#         Always provide helpful answers only and your answer should be within 80 words limit.
#         """
#     ),
#     HumanMessage(content="wirte me a poem about mighty Himalayas."),
# ]

# for chunk in llm.stream(messages):
#     print(chunk.content, end="", flush=True)



from langchain_community.embeddings import HuggingFaceBgeEmbeddings

model_name = "BAAI/bge-small-en"
model_kwargs = {"device": "cpu"}
encode_kwargs = {"normalize_embeddings": True}
hf = HuggingFaceBgeEmbeddings(
    model_name=model_name, model_kwargs=model_kwargs, encode_kwargs=encode_kwargs
)

vec = hf.embed_query("what is distance of moon from earth.")
print(vec)