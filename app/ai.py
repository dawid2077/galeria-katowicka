#ai.py
from schemas import ChatHistory,SessionQuery
from config import settings
from openai import AsyncOpenAI
import structlog
from typing import cast
from openai.types.chat import ChatCompletionMessageParam
from methods import SessionMethods
logger = structlog.get_logger()
#TODO dont hardcode openrouter in future
client = AsyncOpenAI(
    base_url=settings.LLM_URL,
    api_key=settings.OPENROUTER_API_KEY
)
async def llm_call(session: SessionQuery):

    full_response_chunks: list[str] = []

    try:
        messages = cast(
            list[ChatCompletionMessageParam],
            [m.model_dump(exclude_none=True) for m in session.chat_history.conversation],
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
                full_response_chunks.append(content)
                yield {"event": "streamingResponse", "data": content}

        full_text = "".join(full_response_chunks)

        #okay so for it i need session id to query also user_id a
        # here is a mock example will do it in a moment await save_to_db(chat_data.conversation_id, full_text)
        await SessionMethods.save_or_update(
            db=db,
            session_query=session,
            full_llm_response=full_text
        )
    except asyncio.CancelledError:
        logger.info("Client disconnected mid-stream", session_id=str(session.session_id))
        raise  

    except Exception as e:
        logger.error("LLM stream call failed", error=str(e))
        yield {"event": "error", "data": "error"}
        return
    
    yield {"event": "done", "data": ""}

#update it with upper code
#this is for dev dont use it in prod

#! here its outdated
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
    except asyncio.CancelledError:
        logger.info("Client disconnected mid-stream", session_id=str(session.session_id))
        raise  
    except Exception as e:
        yield {"event": "error", "data": str(e)}