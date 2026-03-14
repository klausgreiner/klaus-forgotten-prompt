import os
import httpx
import requests
from google.adk.agents.llm_agent import Agent
from google.adk.agents.loop_agent import LoopAgent
from google.adk.tools.openapi_tool import OpenAPIToolset
from google.adk.tools.openapi_tool.auth.auth_helpers import token_to_scheme_credential

from .memory import get_level_tips


def read_tips(level: int = 0) -> str:
    """Returns optimization tips for the given level. Call read_tips(0) for level 0, read_tips(1) for level 1, read_tips(2) for level 2. Tips are read from .agent_tips/level0_tips.txt, level1_tips.txt, level2_tips.txt."""
    if level not in (0, 1, 2):
        return f"Level must be 0, 1, or 2; got {level}."
    out = get_level_tips(level)
    return out or f"No tips file for level {level} yet."


openapi_spec = requests.get("https://adventure.wietsevenema.eu/openapi.json").text


auth_scheme, auth_credential = token_to_scheme_credential(
    "apikey",
    "header",
    "Authorization",
    f"ApiKey {os.environ.get('ADK_API_KEY')}",
)

adventure_game_toolset = OpenAPIToolset(
    spec_str=openapi_spec,
    auth_scheme=auth_scheme,
    auth_credential=auth_credential,
)


def fetch_url(url: str) -> str:
    """Fetches the content of a URL."""
    with httpx.Client(follow_redirects=True) as client:
        response = client.get(url)
        response.raise_for_status()
        return response.text


def run_code(code: str) -> str:
    """
    Executes the provided Python code string and returns its output or error message.
    Use for quick in-game calculations, puzzles, or automations.
    """
    import sys
    import io
    import traceback

    old_stdout = sys.stdout
    old_stderr = sys.stderr
    sys.stdout = io.StringIO()
    sys.stderr = io.StringIO()
    try:
        import hashlib

        global_vars = {"hashlib": hashlib}
        local_vars = {}
        exec(code, global_vars, local_vars)
        output = sys.stdout.getvalue()
        error = sys.stderr.getvalue()
        if error:
            return f"Error:\n{error.strip()}"
        if output.strip():
            return output.strip()
        # Optionally return "No output." if nothing was printed
        return "Code ran with no output."
    except Exception as e:
        tb = traceback.format_exc()
        return f"Exception:\n{tb.strip()}"
    finally:
        sys.stdout = old_stdout
        sys.stderr = old_stderr


shared_tools = [adventure_game_toolset, fetch_url, run_code, read_tips]

instruction_agent = Agent(
    model="gemini-2.5-flash",
    name="instruction_agent",
    description="Follows the given instructions and tips strictly. Use when the user wants to complete the level as fast as possible by following a plan.",
    instruction=(
        "You strictly follow the instructions. Call read_tips(0,1,2) and do exactly what the tips say.\n"
        "Finish as fast as possible with bonus points. Do not wander or try unrelated actions. Use look, move, take, use, examine, fetch_url as needed to execute the plan.\n"
    ),
    tools=shared_tools,
)

exploratory_agent = Agent(
    model="gemini-2.5-flash",
    name="exploratory_agent",
    description="Exploratory player that examines and tries everything. Use when the user wants to discover the environment, try things, or find secrets.",
    instruction=(
        "You are player use the current of sets of tools to look, move, take, use, and examine,fetch_url\n"
        "A successful adventurer is both quick and curious. use the instructions but don't forget to explore a little\n"
    ),
    tools=shared_tools,
)

root_agent = LoopAgent(
    name="root_agent",
    sub_agents=[exploratory_agent],  # , exploratory_agent],
    max_iterations=50,
)
