import asyncio
import sys
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from agent.agent import root_agent

APP_NAME = "forgotten-prompt"
USER_ID = "default"
SESSION_ID = "default"


def _extract_text(content):
    if not content or not getattr(content, "parts", None):
        return ""
    return " ".join((getattr(p, "text", "") or "" for p in content.parts)).strip()


async def run_agent(message: str) -> str:
    session_service = InMemorySessionService()
    await session_service.create_session(
        app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
    )
    runner = Runner(
        agent=root_agent,
        app_name=APP_NAME,
        session_service=session_service,
    )
    msg = types.Content(role="user", parts=[types.Part(text=message)])
    final = ""
    async for event in runner.run_async(
        user_id=USER_ID, session_id=SESSION_ID, new_message=msg
    ):
        if getattr(event, "is_final_response", None) and event.is_final_response():
            final = _extract_text(getattr(event, "content", None))
            break
    return final or ""


def main():
    if len(sys.argv) < 2:
        print("Usage: uv run python main.py <message>")
        print("Example: uv run python main.py look")
        return
    message = " ".join(sys.argv[1:])
    response = asyncio.run(run_agent(message))
    print(response)


if __name__ == "__main__":
    main()
