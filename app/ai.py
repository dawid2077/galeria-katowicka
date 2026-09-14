#ai.py
from schemas import ChatHistory
from config import settings
from openai import AsyncOpenAI
import structlog
from typing import cast
from openai.types.chat import ChatCompletionMessageParam
logger = structlog.get_logger()
client = AsyncOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=settings.OPENROUTER_API_KEY
)
async def llm_call(chat_data: ChatHistory):
    try:
        messages = cast(
            list[ChatCompletionMessageParam],
            [m.model_dump() for m in chat_data.conversation],
        )

        stream = await client.chat.completions.create(
            model=settings.MODEL,
            messages=messages,
            stream=True,
        )

        async for chunk in stream:
            if not chunk.choices:
                continue

            delta = chunk.choices[0].delta
            content = getattr(delta, "content", None)

            if content:
                yield {"event": "streamingResponse", "data": content}

    except Exception as e:
        logger.error("LLM stream call failed", error=str(e))
        yield {"event": "error", "data": str(e)}
        return

    yield {"event": "done", "data": ""}
async def full_response(chat_data: ChatHistory):
    """Accumulates the entire streamed response and yields it once, at the end."""
    full_text = ""
    try:
        async for chunk in llm_call(chat_data):
            event = chunk.get("event")
            data = chunk.get("data", "")

            if event == "streamingResponse":
                full_text += data
            elif event == "error":
                yield {"event": "error", "data": data}
                return  # stop here, don't send a "done" with partial text

        yield {"event": "done", "data": full_text}
    except Exception as e:
        yield {"event": "error", "data": str(e)}