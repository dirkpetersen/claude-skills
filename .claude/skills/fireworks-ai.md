---
name: fireworks-ai
description: High performance inference API for open-source LLMs with OpenAI-compatible chat, streaming, function calling, structured JSON output, and vision capabilities
---

# Fireworks AI

Fireworks AI provides high-performance inference for open-source LLMs via an OpenAI-compatible API.

## Setup

Set the `FIREWORKS_API_KEY` environment variable.

## API Overview

- **Base URL**: `https://api.fireworks.ai/inference/v1/chat/completions`
- **Authentication**: `Authorization: Bearer $FIREWORKS_API_KEY`
- **Content-Type**: `application/json`

## Popular Models

| Model | Use Case |
|-------|----------|
| `accounts/fireworks/models/deepseek-v3p1` | General text generation |
| `accounts/fireworks/models/kimi-k2-instruct-0905` | Function calling |
| `accounts/fireworks/models/qwen2p5-vl-32b-instruct` | Vision/multimodal |

Browse all models:
- Text: https://app.fireworks.ai/models?filter=Text
- Vision: https://app.fireworks.ai/models?filter=Vision

## Basic Chat Completion

```bash
curl https://api.fireworks.ai/inference/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $FIREWORKS_API_KEY" \
  -d '{
    "model": "accounts/fireworks/models/deepseek-v3p1",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```

## Streaming

Add `"stream": true` for real-time token streaming (SSE format):

```bash
curl https://api.fireworks.ai/inference/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $FIREWORKS_API_KEY" \
  -d '{
    "model": "accounts/fireworks/models/deepseek-v3p1",
    "messages": [{"role": "user", "content": "Tell me a story"}],
    "stream": true
  }'
```

## Function Calling (Tool Use)

Define tools for the model to call:

```bash
curl https://api.fireworks.ai/inference/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $FIREWORKS_API_KEY" \
  -d '{
    "model": "accounts/fireworks/models/kimi-k2-instruct-0905",
    "messages": [{"role": "user", "content": "What is the weather in Paris?"}],
    "tools": [{
      "type": "function",
      "function": {
        "name": "get_weather",
        "description": "Get current weather for a location",
        "parameters": {
          "type": "object",
          "properties": {
            "location": {"type": "string", "description": "City name"}
          },
          "required": ["location"]
        }
      }
    }]
  }'
```

## Structured Output (JSON Schema)

Force responses to match a JSON schema:

```bash
curl https://api.fireworks.ai/inference/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $FIREWORKS_API_KEY" \
  -d '{
    "model": "accounts/fireworks/models/deepseek-v3p1",
    "messages": [{"role": "user", "content": "Extract: John is 30 years old"}],
    "response_format": {
      "type": "json_schema",
      "json_schema": {
        "name": "person",
        "schema": {
          "type": "object",
          "properties": {
            "name": {"type": "string"},
            "age": {"type": "number"}
          },
          "required": ["name", "age"]
        }
      }
    }
  }'
```

## Vision (Multimodal)

Send images with text using vision models:

```bash
curl https://api.fireworks.ai/inference/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $FIREWORKS_API_KEY" \
  -d '{
    "model": "accounts/fireworks/models/qwen2p5-vl-32b-instruct",
    "messages": [{
      "role": "user",
      "content": [
        {"type": "text", "text": "Describe this image"},
        {"type": "image_url", "image_url": {"url": "https://example.com/image.png"}}
      ]
    }]
  }'
```

## Python Example

```python
import os
import requests

response = requests.post(
    "https://api.fireworks.ai/inference/v1/chat/completions",
    headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.environ['FIREWORKS_API_KEY']}"
    },
    json={
        "model": "accounts/fireworks/models/deepseek-v3p1",
        "messages": [{"role": "user", "content": "Hello!"}]
    }
)
print(response.json()["choices"][0]["message"]["content"])
```

## OpenAI SDK Compatibility

Fireworks works with the OpenAI Python SDK:

```python
from openai import OpenAI

client = OpenAI(
    base_url="https://api.fireworks.ai/inference/v1",
    api_key=os.environ["FIREWORKS_API_KEY"]
)

response = client.chat.completions.create(
    model="accounts/fireworks/models/deepseek-v3p1",
    messages=[{"role": "user", "content": "Hello!"}]
)
```

## Documentation

- Text Models: https://docs.fireworks.ai/guides/querying-text-models
- Vision Models: https://docs.fireworks.ai/guides/querying-vision-language-models
- Function Calling: https://docs.fireworks.ai/guides/function-calling
- Structured Output: https://docs.fireworks.ai/structured-responses/structured-response-formatting
- Embeddings: https://docs.fireworks.ai/guides/querying-embeddings-models
- Batch Inference: https://docs.fireworks.ai/guides/batch-inference
- Reasoning: https://docs.fireworks.ai/guides/reasoning
- Prompt Caching: https://docs.fireworks.ai/guides/prompt-caching
- Error Codes: https://docs.fireworks.ai/guides/inference-error-codes
