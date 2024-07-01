from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.llm import router as llm_routers
from app.routes.rag import router as rag_routers
import uvicorn


app = FastAPI(title="HCL Assignment", version="2.0")
app.include_router(llm_routers)
app.include_router(rag_routers)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    uvicorn.run(app="main:app", host="localhost", port=8000, reload=True)
