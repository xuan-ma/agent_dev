# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## CRITICAL: Security and file access rules

1. **NEVER read `.env` files.** `.env` files (in this repo or any subdirectory) contain secret API keys for LLM providers (DeepSeek, OpenRouter, DashScope, ZhiPu, OpenAI, etc.). Reading them could leak credentials into conversation logs. This is a hard rule — do not read, search, open, or cat any `.env` file under any circumstances.

2. **Respect `.gitignore`.** Files and patterns listed in `.gitignore` are intentionally excluded from version control and must not be read or analyzed. Currently this includes `.env` and `*.pyc`. If `.gitignore` is updated with new entries, honor those as well.

3. **Actively evolving codebase.** This repository is under active, ongoing development. Its architecture, module layout, and patterns change in real time. The documentation below is a snapshot that may become stale. Always verify the current state of the code rather than relying solely on the documented architecture. When the code and this document disagree, **the code is authoritative**.

## Project overview

A Python toolkit for working with multiple LLM providers (DeepSeek, OpenAI, Anthropic, OpenRouter, DashScope, ZhiPu) through a unified OpenAI SDK-compatible interface. The project explores API calling patterns, prompt engineering, conversation memory management, function calling, multi-modal inputs, and image generation.

## Environment & dependencies

- **Python**: Standard Python environment (no virtual env wrapper specified)
- **Install**: `pip install -r requirements.txt`
- **Config**: Copy `.env` to `model_api/.env` with API keys (`DEEPSEEK_API_KEY`, `OPENROUTER_API_KEY`, `DASHSCOPE_API_KEY`, `ZHIPU_API_KEY`, etc.)
- The active platform is set by the `model_platform` variable in `model_api/config.py` — default is `"DeepSeek"`

## Architecture

```
model_api/           # Core module: multi-provider LLM API abstraction
├── config.py        # Platform definitions, API keys, model selection (single source of truth)
├── openai_method.py # Main sync API: call_model → safe_call_model → conversation + multi-turn loop
├── async_openai_method.py  # Async client + asyncio.gather concurrency demo
├── function_calling.py     # Tool-use loop: call → detect tool_calls → execute → call again
├── multi_modalities.py     # Vision: build messages with image_url content blocks
├── image_gen.py            # Image generation via extra_body={"modalities": ["image","text"]}
├── image_utils.py          # PIL-based base64 encode/decode for local images
├── openai_embedding.py     # Text embeddings via DashScope (Aliyun)
├── fee_info.py             # Token usage printing + account balance HTTP query
├── requests_method.py      # Raw HTTP requests alternative to the SDK
├── functions/              # Tool definitions and mock implementations for function calling
│   ├── tools_config.py     # JSON Schema tool definitions
│   └── get_weather.py      # Mock weather function
memory/              # Conversation context management strategies
├── sliding_window.py       # Keep last N turns, discard older ones
└── summarize_history.py    # LLM-powered summarization of older turns (preserves key info)
prompt_engineering/  # Demo scripts for prompt techniques (role definition, few-shot, CoT, format output)
```

## Key patterns

### Calling a model

The standard path is `conversation()` in `model_api/openai_method.py`, which wraps `safe_call_model()` (retry with exponential backoff for rate limits, connection errors). The `call_model()` function is the raw caller — use it when you need full control.

All functions accept `messages`, `stream`, `temperature`, `tools`, `max_tokens`, `timeout`, and arbitrary `**kw_args` forwarded to the OpenAI SDK.

### Adding a new platform

Edit `PLATFORMS_CONFIG` in `model_api/config.py` — add a new entry with `base_url`, `api_key`, and `model_name`. The platform is selected by changing `model_platform` at the top of the file.

### Function calling flow

1. Define tool schemas in `model_api/functions/tools_config.py`
2. Pass `tools=tools` to `conversation()`
3. Check `response.choices[0].message.tool_calls` on the response
4. Execute the requested function, append the result as a `{"role": "tool", ...}` message
5. Call `conversation()` again for the final answer

### Conversation memory

Two strategies in `memory/`:
- **Sliding window** (`sliding_window.py`): Keep system message + last N turns, drop the rest. Simple but loses early context.
- **Summary compression** (`summarize_history.py`): Use an LLM call to compress old turns into a summary, inject it as a system message, keep recent turns intact. Preserves key information across long conversations.

## Multiple provider support

The `config.py` defines these platforms (model name comments indicate what each is typically used for):

| Platform | Base URL pattern | Use case |
|----------|-----------------|----------|
| DeepSeek | `api.deepseek.com` | General chat (v4-flash/v4-pro) |
| OpenRouter | `openrouter.ai/api/v1` | Multi-model access (Gemini image gen, GPT, GLM) |
| DashScope | `dashscope.aliyuncs.com` | Text embeddings (text-embedding-v3) |
| ZhiPu | `open.bigmodel.cn` | GLM series models |
| OpenAI | `api.openai.com/v1` | GPT models |

## Notes

- The `.env` file (which MUST NOT be read — see security rules at the top of this file) lives in `model_api/` (not repo root) — `config.py` loads it from `Path(__file__).parent / ".env"`
- `openai_embedding.py` and `requests_method.py` use a top-level `from config import ...` / `from utils import ...` import style (without the `model_api.` prefix) — these are older files that may need path fixes to run from the repo root
- `async_openai_method.py` demonstrates both sync-batch and async-concurrent calling with a performance comparison
- The `prompt_engineering/` scripts each create their own standalone client (not using `model_api.openai_method`) — they are self-contained demos
