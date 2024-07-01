import os
import shutil
from fastapi import APIRouter
from fastapi import File, UploadFile
from fastapi.responses import StreamingResponse, JSONResponse
from langchain_openai.chat_models.base import ChatOpenAI
from app.config import settings
from pathlib import Path

from langchain import hub
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough



# Directory where uploaded files will be stored
UPLOAD_DIR = Path(os.path.join(settings.APP_DIR,"data"))
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)  # Create directory if it doesn't exist


llm = ChatOpenAI(
    base_url="http://localhost:8080/v1",
    api_key="not-needed",
    model="gpt-3.5-turbo-0613",
    max_tokens=128,
    temperature=0.2,
    streaming=True,
)


model_name = "BAAI/bge-small-en"
model_kwargs = {"device": "cpu"}
encode_kwargs = {"normalize_embeddings": True}
hf = HuggingFaceBgeEmbeddings(
    model_name=model_name, model_kwargs=model_kwargs, encode_kwargs=encode_kwargs
)

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

router = APIRouter(tags=["RAG"])

@router.post("/upload")
async def upload_files(files: list[UploadFile] = File(...)):
    for file in files:
        file_path = UPLOAD_DIR / file.filename
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
    return JSONResponse(content={"message": "Files uploaded successfully"})

@router.post("/rag")
async def rag(query : str ):
    # load pdfs
    pdf_folder_path = os.path.join(settings.APP_DIR,"data")
    docs = []
    for file in os.listdir(pdf_folder_path):
        if file.endswith('.pdf'):
            pdf_path = os.path.join(pdf_folder_path, file)
            loader = PyPDFLoader(pdf_path)
            docs.extend(loader.load())
    if len(docs)>0:
        # split pdf
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        splits = text_splitter.split_documents(docs)
        # save and embed into vector DB
        vectorstore = Chroma.from_documents(documents=splits, embedding=hf)
        # retriever
        retriever = vectorstore.as_retriever()
        prompt = hub.pull("rlm/rag-prompt")

        rag_chain = (
            {"context": retriever | format_docs, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
        )
        result = rag_chain.invoke(query)

        return {
            "response" : result
        }
    else:
        return {
            "response": "No file is uploaded."
        }