---
name: fireworks-ai
description: Use this skill whenever the user wants to work with Fireworks AI, including querying text models, vision models, implementing function calling, structured JSON responses, streaming, batch inference, embeddings, ASR, reasoning models, prompt caching, predicted outputs, and completions API calls. Use the fireworks-ai skill for building applications with open-source LLMs via the Fireworks API, setting up FIREWORKS_API_KEY authentication, and integrating high-performance inference into workflows.
---

## Setup

Fireworks AI provides high-performance access to open-source LLMs. To get started, you'll need to set your API key as an environment variable:

```bash
export FIREWORKS_API_KEY="your_api_key_here"
```

The API key is required for all requests to the Fireworks API endpoint at `https://api.fireworks.ai/inference/v1/`.

## Quick Start

The simplest way to query Fireworks is with a basic chat completion request:

```bash
curl https://api.fireworks.ai/inference/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $FIREWORKS_API_KEY" \
  -d '{
    "model": "accounts/fireworks/models/deepseek-v3p1",
    "messages": [
      {
        "role": "user",
        "content": "Say hello in Spanish"
      }
    ]
  }'
```

## Examples

### Streaming Responses

Enable streaming to get responses token-by-token:

```bash
curl https://api.fireworks.ai/inference/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $FIREWORKS_API_KEY" \
  -d '{
    "model": "accounts/fireworks/models/deepseek-v3p1",
    "messages": [
      {
        "role": "user",
        "content": "Tell me a short story"
      }
    ],
    "stream": true
  }'
```

### Function Calling

Use tools to enable the model to call functions:

```bash
curl https://api.fireworks.ai/inference/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $FIREWORKS_API_KEY" \
  -d '{
    "model": "accounts/fireworks/models/kimi-k2-instruct-0905",
    "messages": [
      {
        "role": "user",
        "content": "What is the weather in Paris?"
      }
    ],
    "tools": [
      {
        "type": "function",
        "function": {
          "name": "get_weather",
          "description": "Get the current weather for a location",
          "parameters": {
            "type": "object",
            "properties": {
              "location": {
                "type": "string",
                "description": "City name, e.g. San Francisco"
              }
            },
            "required": ["location"]
          }
        }
      }
    ]
  }'
```

### Structured Output (JSON)

Request structured JSON responses using a schema:

```bash
curl https://api.fireworks.ai/inference/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $FIREWORKS_API_KEY" \
  -d '{
    "model": "accounts/fireworks/models/deepseek-v3p1",
    "messages": [
      {
        "role": "user",
        "content": "Extract the name and age from: John is 30 years old"
      }
    ],
    "response_format": {
      "type": "json_schema",
      "json_schema": {
        "name": "person",
        "schema": {
          "type": "object",
          "properties": {
            "name": {
              "type": "string"
            },
            "age": {
              "type": "number"
            }
          },
          "required": ["name", "age"]
        }
      }
    }
  }'
```

### Vision Models

Process images with vision models:

```bash
curl https://api.fireworks.ai/inference/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $FIREWORKS_API_KEY" \
  -d '{
    "model": "accounts/fireworks/models/qwen2p5-vl-32b-instruct",
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text": "What is in this image?"
          },
          {
            "type": "image_url",
            "image_url": {
              "url": "https://storage.googleapis.com/fireworks-public/image_assets/fireworks-ai-wordmark-color-dark.png"
            }
          }
        ]
      }
    ]
  }'
```

## Key Concepts

**Models**: Fireworks provides access to various open-source models. Text models handle conversational tasks and reasoning, while vision models process images alongside text.

**Authentication**: All requests require the `Authorization: Bearer $FIREWORKS_API_KEY` header with your API key.

**Streaming**: Set `"stream": true` in requests to receive responses as a stream of tokens rather than waiting for the complete response.

**Function Calling**: Define tools in the request to enable models to request specific function invocations.

**Structured Responses**: Use `response_format` with a JSON schema to enforce structured output from the model.

## References

- Current Text Models: https://app.fireworks.ai/models?filter=Text
- Current Vision Models: https://app.fireworks.ai/models?filter=Vision
- Querying Text Models: https://docs.fireworks.ai/guides/querying-text-models
- Querying Vision Language Models: https://docs.fireworks.ai/guides/querying-vision-language-models
- Querying ASR Models: https://docs.fireworks.ai/guides/querying-asr-models
- Querying Embeddings Models: https://docs.fireworks.ai/guides/querying-embeddings-models
- Function Calling: https://docs.fireworks.ai/guides/function-calling
- Batch Inference: https://docs.fireworks.ai/guides/batch-inference
- Structured Response Formatting: https://docs.fireworks.ai/structured-responses/structured-response-formatting
- Reasoning: https://docs.fireworks.ai/guides/reasoning
- Predicted Outputs: https://docs.fireworks.ai/guides/predicted-outputs
- Prompt Caching: https://docs.fireworks.ai/guides/prompt-caching
- Completions API: https://docs.fireworks.ai/guides/completions-api
- Response API: https://docs.fireworks.ai/guides/response-api
- Inference Error Codes: https://docs.fireworks.ai/guides/inference-error-codes