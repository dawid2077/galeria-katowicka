#ai.py
from schemas import ChatHistory
from config import settings
from openai import AsyncOpenAI
client = AsyncOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=settings.OPENROUTER_API_KEY
)
async def llm_call(chat_data: ChatHistory):
    try:
        stream = await client.chat.completions.create(
            model=settings.MODEL,
            messages=[m.model_dump() for m in chat_data.conversation],
            stream=True,
        )
        async for chunk in stream:
            if not chunk.choices:
                continue
            content = chunk.choices[0].delta.content
            if content:
                yield {"event": "streamingResponse", "data": content}
    except Exception as e:
        yield {"event": "error", "data": str(e)}
    finally:
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