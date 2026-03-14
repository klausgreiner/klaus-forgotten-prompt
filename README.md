# Workshop Forgotten Prompt

![Score](
https://private-user-images.githubusercontent.com/17580502/563364090-29521e41-a625-4340-956d-47bd7883cdef.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NzM0NDg2MTUsIm5iZiI6MTc3MzQ0ODMxNSwicGF0aCI6Ii8xNzU4MDUwMi81NjMzNjQwOTAtMjk1MjFlNDEtYTYyNS00MzQwLTk1NmQtNDdiZDc4ODNjZGVmLnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNjAzMTQlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjYwMzE0VDAwMzE1NVomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPTZmZGVlMWJiOWI3YWUxYmEwM2U0ZTkyNGMzNjdkNTM5MWY1YzI3YTU0ZTY2YWI4M2FmOTM4Yzc5NDkxOTc3Y2YmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0In0.QXqPbOCZHXge3fmgTKdNdQOBBYcAcdVrrIcgHbNSBI0)
![Score per Level](
https://private-user-images.githubusercontent.com/17580502/563364131-8e70c66e-5aa7-4e38-9863-c226a74cd5f7.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NzM0NDg2MTUsIm5iZiI6MTc3MzQ0ODMxNSwicGF0aCI6Ii8xNzU4MDUwMi81NjMzNjQxMzEtOGU3MGM2NmUtNWFhNy00ZTM4LTk4NjMtYzIyNmE3NGNkNWY3LnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNjAzMTQlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjYwMzE0VDAwMzE1NVomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPTgxZTk2NWRkNDJiYjY3N2UzODBmMTIwMmVjYzQ1MzlmMDZjMDRjNTU4ZTdmNDlkM2Q0NzdhZmJiOWM5NjA2ODMmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0In0.3R2Uq7kI045I5759eqG6nJnZf7Ea4p8sv1KT04dNxGQ)



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

## Useful Links
https://adventure.wietsevenema.eu/
https://wietsevenema.eu/blog/2025/adding-a-tool-to-your-adk-agent/
https://console.cloud.google.com/
