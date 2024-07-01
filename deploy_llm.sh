#!/bin/bash

source .env

# deploy model
docker run -d --rm --name llamacpp-container \
-p 8080:8080 \
-v $MODEL_DIR:/models \
ghcr.io/ggerganov/llama.cpp:server \
-m /models/models-gguf/$MODEL_PATH \
--ctx-size 8192 \
--cont-batching \
--embeddings \
--host 0.0.0.0 \
--port 8080