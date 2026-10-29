# HelloGenAI
Simple Python application using remote GenAI.

`hello_llama.py` connects to a [llama.cpp](https://github.com/ggml-org/llama.cpp) server through its OpenAI-compatible API. It checks the server's health, lists the available models, and sends a chat prompt.

## Setup

```bash
py -m venv .venv
.venv/Scripts/python -m pip install -r requirements.txt
```

Create a `.env` file in the project root (see `.env.example`):

```
LLAMA_ENDPOINT=http://pax186.pax.tufts.edu:10791
LLAMA_API_KEY=your-api-key-here
```

`.env` is git-ignored, so your key stays out of the repo.

## Run

```bash
# Use the default prompt
.venv/Scripts/python hello_llama.py

# Or pass your own prompt
.venv/Scripts/python hello_llama.py "Explain what a large language model is in two sentences."
```

Example output:

```
Connecting to http://pax123.pax.tufts.edu:12345 (api key set)
Health: 200 {"status":"ok"}
Models: <model name>

Prompt: Explain what a large language model is in two sentences.

Response: ...
```

On macOS/Linux, use `.venv/bin/python` instead of `.venv/Scripts/python`.
