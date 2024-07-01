#!/bin/bash

# create dir for models
mkdir llm_models

# create venv
python3 -m venv env

# install pkgs
source env/bin/activate && pip install -r requirements.txt

# download gguf llm model
python download.py