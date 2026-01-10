
Fireworks AI is a high performance provider of Opensource LLM

It requires and var FIREWORKS_API_KEY to be set 

Quick Start --- In it's most simple form it works like this: 

```
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

Streaming responses : 

```
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

Function calling : 


```
curl https://api.fireworks.ai/inference/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $FIREWORKS_API_KEY" \
  -d '{
    "model": "accounts/fireworks/models/kimi-k2-instruct-0905",
    "messages": [
      {
        "role": "user",
        "content": "What'\''s the weather in Paris?"
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

Structured output (Json) 

```
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

Vision Models

```
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
            "text": "What'\''s in this image?"
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


More info on Models: 

* Current Text Models:  https://app.fireworks.ai/models?filter=Text
* Current Vision Models:  https://app.fireworks.ai/models?filter=Vision


More Info ---- Guides:

https://docs.fireworks.ai/guides/querying-text-models
https://docs.fireworks.ai/guides/querying-vision-language-models
https://docs.fireworks.ai/guides/querying-asr-models
https://docs.fireworks.ai/guides/querying-embeddings-models
https://docs.fireworks.ai/guides/function-calling
https://docs.fireworks.ai/guides/batch-inference
https://docs.fireworks.ai/structured-responses/structured-response-formatting
https://docs.fireworks.ai/guides/reasoning
https://docs.fireworks.ai/guides/predicted-outputs
https://docs.fireworks.ai/guides/prompt-caching
https://docs.fireworks.ai/guides/completions-api
https://docs.fireworks.ai/guides/response-api
https://docs.fireworks.ai/guides/inference-error-codes


