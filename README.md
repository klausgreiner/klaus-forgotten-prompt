# klaus-forgotten-prompt

https://adventure.wietsevenema.eu/leaderboards/9ffbf65d-c398-458c-8f86-3c5844fd563c
https://adventure.wietsevenema.eu/
https://wietsevenema.eu/blog/2025/adding-a-tool-to-your-adk-agent/
https://console.cloud.google.com/

## Running the agent

```bash
uv run python main.py <message>
```

Example: `uv run python main.py look`

The agent can read per-level tips from `.agent_tips/level0_tips.txt`, `level1_tips.txt`, and `level2_tips.txt` via the `read_tips(level)` tool (e.g. `read_tips(0)` for level 0).

## Play level (scripted bot)

Runs a level using instructions from `.agent_tips/levelN_tips.txt`. Prints only the final score unless `--curl` is used.

```bash
uv run python play_level.py [level_id]
uv run python play_level.py level-0
uv run python play_level.py level-1
uv run python play_level.py level-2
```

- **`--curl`** — Run the level, then print a bash script you can save and run to replay the same sequence (with resolved `$open_vent` / `$hash_tunnel` for level-2).
- **`--fast`** / **`-q`** — Quiet: no extra output, only the score.

Set `ADK_API_KEY` in the environment to use a different API key.

### Example `.env` file (`agent/.env`)

````
GOOGLE_GENAI_USE_VERTEXAI=1
GOOGLE_CLOUD_PROJECT=your-gcp-location
GOOGLE_CLOUD_LOCATION=us-central1
ADK_API_KEY=fakeapikey1234567890

You can copy this to `agent/.env` and adjust as needed.
## Google Cloud (gcloud)

```bash
gcloud config set project klaus-garden-forgotten-prompt
gcloud auth application-default login
gcloud auth login
````

## ADK web UI

```bash
uv run adk web
```
