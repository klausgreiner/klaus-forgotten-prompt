import os
import httpx
import requests
from google.adk.agents.llm_agent import Agent
from google.adk.agents.loop_agent import LoopAgent
from google.adk.tools.openapi_tool import OpenAPIToolset
from google.adk.tools.openapi_tool.auth.auth_helpers import token_to_scheme_credential

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


# player_agent = Agent(
#     model="gemini-2.5-flash",
#     name="player_agent",
#     description="An expert adventure game player.",
#     instruction=(
#         "You are player use the current of sets of tools to look, move, take, use, and examine,fetch_url",
#         "Explore thoroughly and interact with everything.A successful adventurer is both quick and curious. Good luck!",
#         "Available commands: look (l, ls, view, see) - Look around in the room; inventory (i, bag, items) - List your inventory; examine <thing> (x, inspect, check) - Describe an item or exit; move <exit> (m, go, cd, walk, mv) - Move through an exit; take <item> (t, get, grab, pick) - Take an item; use <item> [on <target>] (u, apply) - Use an item, or an item on a target; drop <item> (d, discard, release) - Drop an item from your inventory; quit (q, exit, :q!, ESC, Ctrl+C) - Quit the level; help (h, ?, man, info) - Show a list of commands.",
#     ),
#     tools=[adventure_game_toolset, fetch_url],
# )


# critic_agent = Agent(
#     model="gemini-2.5-flash",
#     name="critic_agent",
#     description="A strategic critic who reviews actions taken by the player agent and guides them to improve their results.",
#     instruction=(
#         "You are the CRITIC agent, observing every action taken by the player_agent in the adventure game 'The Garden of the Forgotten Prompt.'\n\n"
#         "Your job is to:\n"
#         "- Analyze and critique each move the player_agent makes, focusing on efficiency, creativity, and how well it follows leaderboard optimization strategy.\n"
#         "- Point out missed opportunities for micro-awards, exploration, or faster progression, and suggest alternative actions if needed.\n"
#         "- Help the player maintain an optimal game strategy by detecting patterns of inefficiency, overlooked clues, or repeated mistakes.\n"
#         "- Ensure the player_agent always executes one strategic action per turn and avoids unnecessary actions.\n"
#         "You NEVER take direct action in the game, but always reflect on the PLAYER's most recent actions, outcomes, and decisions, giving clear, helpful feedback and guidance for improvement.\n"
#         "If the player_agent reaches a termination state or makes a perfect optimal move, praise or acknowledge this appropriately.\n\n"
#         "Format your response as:\n"
#         '"CRITIQUE": Your strategic feedback and analysis (1-2 paragraphs max).\n'
#         '"GUIDANCE": Concrete advice or an improved next step for the player_agent.'
#     ),
#     tools=[],
# )
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


player_agent = Agent(
    model="gemini-2.5-flash",
    name="player_agent",
    description="An expert adventure game player.",
    instruction=(
        "You are player use the current of sets of tools to look, move, take, use, and examine,fetch_url\n"
        "Always use look and try to go as fast as you can listening to the instructions. A successful adventurer is both quick and curious. Good luck!\n"
        "Available commands: look (l, ls, view, see) - Look around in the room; inventory (i, bag, items) - List your inventory; examine <thing> (x, inspect, check) - Describe an item or exit; move <exit> (m, go, cd, walk, mv) - Move through an exit; take <item> (t, get, grab, pick) - Take an item; use <item> [on <target>] (u, apply) - Use an item, or an item on a target; drop <item> (d, discard, release) - Drop an item from your inventory; quit (q, exit, :q!, ESC, Ctrl+C) - Quit the level; help (h, ?, man, info) - Show a list of commands."
    ),
    tools=[adventure_game_toolset, fetch_url, run_code],
)

root_agent = LoopAgent(
    name="root_agent",
    sub_agents=[player_agent],
    max_iterations=100,
)
