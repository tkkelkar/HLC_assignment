step 1:
    choose a robust llm model.
    I have choosen TheBloke/Mistral-7B-Instruct-v0.2-GGUF with 6-bit quantization for my task.

step 2:
    Integrate LangChain:
        Used Langchian for chatopenai client to talk to locally hosted LLM. and used Langchain for RAG pipeline.

step 3:
    Develop the User Interface:
        As it is not my area of expertise, I am leaving this section.

step 4:
    API Endpoints:
        Used Fastapi to develop api endpoints
            llm
                - query
                - query_stream
            rag
                - upload
                - rag
step 5:
    Process query, Handle request and response:
        - every thing is done in FastAPI

step 6:
    Test and validate:
        pytest has been used to perform unittests of application.

step 7:
    Deployment:
        application is containarized. devloper can take this to deployment environment with following appropriate steps.
