import os

from huggingface_hub import snapshot_download

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(PROJECT_DIR, "llm_models")

access_token = "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"


all_model = {
    "models-gguf": [
        # "TheBloke/zephyr-7B-beta-GGUF",
        "TheBloke/Mistral-7B-Instruct-v0.2-GGUF",
        # "lmstudio-community/Meta-Llama-3-8B-Instruct-GGUF",
        # "TheBloke/phi-2-GGUF",
        # "google/gemma-2b-it", # 10GB
        # "google/gemma-7b-it", # 34GB
        # "google/codegemma-7b-it-GGUF",  # 34GB
        # "Qwen/CodeQwen1.5-7B-Chat-GGUF",  #
    ],
    "models-tgi": [
        # "HuggingFaceH4/zephyr-7b-beta",
        # "google/codegemma-7b",
        # "google/gemma-2b-it",
        # "google/recurrentgemma-2b-it" # if gguf available downlaod that
    ],
    "models-embd": [
        # "sentence-transformers/all-MiniLM-L6-v2",
        # "BAAI/bge-base-en-v1.5",
        # "BAAI/bge-small-en-v1.5",
        # "BAAI/bge-large-en-v1.5",
    ],
    "models-reranker": [
        # "BAAI/bge-reranker-large",
    ],
}


# select a single file download or a list of patterns
select_allow_patterns_dict = {
    "TheBloke/zephyr-7B-beta-GGUF": "*Q6*",
    "TheBloke/Mistral-7B-Instruct-v0.2-GGUF": "*Q6*",
    "lmstudio-community/Meta-Llama-3-8B-Instruct-GGUF": "*Q6*",
    "TheBloke/phi-2-GGUF": ["*Q6*", "*Q8*"],
    "google/gemma-2b-it": "*.gguf",
    "google/gemma-7b-it": "*.gguf",
    "google/codegemma-7b-it-GGUF": "*it.gguf",
    # "google/codegemma-7b-it-GGUF": "*it-f16.gguf",
    "Qwen/CodeQwen1.5-7B-Chat-GGUF": "q5_k",
}


def download_model(model_id, local_dir, allow_patterns=None):
    snapshot_download(
        repo_id=model_id,
        local_dir=local_dir,
        local_dir_use_symlinks=False,
        revision="main",
        token=access_token,
        allow_patterns=allow_patterns,
    )


for folder_name, model_ids in all_model.items():
    for model_id in model_ids:
        local_dir = os.path.join(MODEL_DIR, f"{folder_name}", model_id)
        print(f"Downloading {model_id} into {local_dir} folder...")
        try:
            allow_patterns = select_allow_patterns_dict[model_id]
            download_model(
                model_id=model_id, local_dir=local_dir, allow_patterns=allow_patterns
            )
        except Exception:
            download_model(model_id=model_id, local_dir=local_dir)
