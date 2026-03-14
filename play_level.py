"""
Bot that plays a level using tips from .agent_tips/levelN_tips.txt.
Usage: uv run python play_level.py [--curl] [level_id]
  --curl   Run requests and at the end print a bash script to replay the level
  level_id level-0, level-1, level-2, or 0, 1, 2
Set ADK_API_KEY in env or it uses the default key.
"""

import hashlib
import json
import os
import re
import sys
from pathlib import Path

import httpx

BASE_URL = "https://adventure.wietsevenema.eu"
API_KEY = os.environ.get(
    "ADK_API_KEY",
    "fc73378f4efaf73c809944522a0e04370b2a5a3f1d57124be211dd363beaf3ad",
)
HEADERS = {
    "Authorization": f"ApiKey {API_KEY}",
    "Content-Type": "application/json",
    "Accept": "application/json",
}
TIPS_DIR = Path(__file__).resolve().parent / ".agent_tips"
OPEN_VENT_PATTERN = re.compile(r"'OPEN':\s*'([^']+)'")
HASH_PREFIX_PATTERN = re.compile(r"HASH PREFIX:\s*[`']?([a-f0-9]+)[`']?", re.I)
TUNNEL_LINE_PATTERN = re.compile(r"^\s*-\s+([a-zA-Z0-9_]+)\s*$", re.M)
SCORE_PATTERN = re.compile(r"score of (\d+)", re.I)


def _curl_cmd(method: str, path: str, body: dict | None) -> str:
    url = f"{BASE_URL}{path}"
    auth = f"ApiKey {API_KEY}"
    parts = [
        "curl",
        "-s",
        "-X",
        method,
        "-H",
        f"Authorization: {auth}",
        "-H",
        "Content-Type: application/json",
        "-H",
        "Accept: application/json",
    ]
    if body:
        raw = json.dumps(body, separators=(",", ":"))
        escaped = raw.replace("'", "'\"'\"'")
        parts.extend(["-d", f"'{escaped}'"])
    parts.append(url)
    return " ".join(parts)


def _path_and_body(action: str, payload_clean: dict) -> tuple[str, dict | None]:
    if action == "start":
        return "/game/start", payload_clean
    if action == "examine":
        return "/game/examine", payload_clean
    if action == "move":
        return "/game/move", payload_clean
    if action == "take":
        return "/game/take", payload_clean
    if action == "drop":
        return "/game/drop", payload_clean
    if action == "use":
        return "/game/use", payload_clean
    return "", None


def _find_tunnel_by_hash(description: str) -> str | None:
    prefix_m = HASH_PREFIX_PATTERN.search(description)
    if not prefix_m:
        return None
    prefix = prefix_m.group(1).lower()
    tunnels = TUNNEL_LINE_PATTERN.findall(description)
    if not tunnels:
        return None
    for name in tunnels:
        if hashlib.sha256(name.encode()).hexdigest().startswith(prefix):
            return name
    return None


def _strip_comment(line: str) -> str:
    return re.sub(r'\s*\([^)"\']*\)\s*$', "", line).strip()


def parse_tips(content: str, level_id: str) -> list[tuple[str, dict]]:
    instructions = []
    for raw in content.splitlines():
        line = raw.strip()
        if not line:
            continue
        line = _strip_comment(line)
        for part in re.split(r"\s*->\s*", line):
            part = part.strip()
            if not part:
                continue
            m = re.match(r'start_level\s*\(\s*["\']([^"\']+)["\']\s*\)', part, re.I)
            if m:
                instructions.append(("start", {"level_id": m.group(1)}))
                continue
            m = re.match(r'examine\s*\(\s*["\']?([^"\'(),]+)["\']?\s*\)', part, re.I)
            if m:
                instructions.append(("examine", {"target": m.group(1).strip()}))
                continue
            m = re.match(r"examine\s+(.+)", part, re.I)
            if m:
                instructions.append(("examine", {"target": m.group(1).strip()}))
                continue
            m = re.match(r'take\s*\(\s*["\']?([^"\'(),]+)["\']?\s*\)', part, re.I)
            if m:
                instructions.append(("take", {"item_name": m.group(1).strip()}))
                continue
            m = re.match(r"take\s+(.+)", part, re.I)
            if m:
                instructions.append(("take", {"item_name": m.group(1).strip()}))
                continue
            m = re.match(r'move\s*\(\s*["\']?([^"\'(),]+)["\']?\s*\)', part, re.I)
            if m:
                instructions.append(("move", {"exit_name": m.group(1).strip()}))
                continue
            m = re.match(r"move\s+(.+)", part, re.I)
            if m:
                instructions.append(("move", {"exit_name": m.group(1).strip()}))
                continue
            m = re.match(r'drop\s*\(\s*["\']?([^"\'(),]+)["\']?\s*\)', part, re.I)
            if m:
                instructions.append(("drop", {"item_name": m.group(1).strip()}))
                continue
            m = re.match(r"drop\s+(.+)", part, re.I)
            if m:
                instructions.append(("drop", {"item_name": m.group(1).strip()}))
                continue
            m = re.match(
                r'use\s*\(\s*["\']?([^"\'(),]+)["\']?\s*,\s*["\']?([^"\'(),]+)["\']?\s*\)',
                part,
                re.I,
            )
            if m:
                instructions.append(
                    (
                        "use",
                        {
                            "direct_object": m.group(1).strip(),
                            "indirect_object": m.group(2).strip(),
                        },
                    )
                )
                continue
            m = re.match(r"use\s+(.+)\s+on\s+(.+)", part, re.I)
            if m:
                instructions.append(
                    (
                        "use",
                        {
                            "direct_object": m.group(1).strip(),
                            "indirect_object": m.group(2).strip(),
                        },
                    )
                )
                continue
            m = re.match(r'use\s*\(\s*["\']?([^"\'(),]+)["\']?\s*\)', part, re.I)
            if m:
                instructions.append(
                    (
                        "use",
                        {"direct_object": m.group(1).strip(), "indirect_object": None},
                    )
                )
                continue
            m = re.match(r"use\s+(.+)", part, re.I)
            if m:
                instructions.append(
                    (
                        "use",
                        {"direct_object": m.group(1).strip(), "indirect_object": None},
                    )
                )
                continue
    if instructions and instructions[0][0] != "start":
        instructions.insert(0, ("start", {"level_id": level_id}))
    return instructions


def load_instructions(level_id: str) -> list[tuple[str, dict]]:
    if level_id in ("0", "1", "2"):
        level_id = f"level-{level_id}"
    num = level_id.replace("level-", "") if level_id.startswith("level-") else level_id
    path = TIPS_DIR / f"level{num}_tips.txt"
    if not path.exists():
        raise SystemExit(f"Tips file not found: {path}")
    text = path.read_text(encoding="utf-8")
    instructions = parse_tips(text, level_id)
    if not instructions:
        raise SystemExit(f"No instructions parsed from {path}")
    if instructions[0][0] == "start":
        instructions[0] = ("start", {"level_id": level_id})
    return instructions


def _emit_bash_script(requests: list[tuple[str, dict]]) -> None:
    if not requests:
        return
    lines = [
        "#!/usr/bin/env bash",
        "# Replay script; uses cookie jar for session.",
        "set -e",
        f'BASE="{BASE_URL}"',
        f'API_KEY="${{ADK_API_KEY:-{API_KEY}}}"',
        "JAR=$(mktemp)",
        "trap 'rm -f \"$JAR\"' EXIT",
        "",
        "req() {",
        '  curl -s -c "$JAR" -b "$JAR" -X POST \\',
        '    -H "Authorization: ApiKey $API_KEY" \\',
        '    -H "Content-Type: application/json" \\',
        '    -H "Accept: application/json" \\',
        '    -d "$1" "$BASE$2"',
        "}",
        "",
    ]
    for i, (path, body) in enumerate(requests):
        raw = json.dumps(body, separators=(",", ":"))
        escaped = raw.replace("'", "'\"'\"'")
        if i < len(requests) - 1:
            lines.append(f"req '{escaped}' {path} >/dev/null")
        else:
            lines.append(
                f"req '{escaped}' {path} | grep -oE 'score of [0-9]+' | grep -oE '[0-9]+'"
            )
    print("\n".join(lines))


def main():
    args = [a for a in sys.argv[1:] if a not in ("--fast", "-q", "--curl")]
    export_curl = "--curl" in sys.argv[1:]
    level_id = args[0] if args else "level-0"
    instructions = load_instructions(level_id)

    last_response = {}
    curl_requests: list[tuple[str, dict]] = []
    with httpx.Client(timeout=15) as client:
        for i, (action, payload) in enumerate(instructions, 1):
            payload_clean = {k: v for k, v in payload.items() if v is not None}
            if action == "move" and payload_clean.get("exit_name") == "$open_vent":
                text = last_response.get("description", "") or str(last_response)
                m = OPEN_VENT_PATTERN.search(text)
                if not m:
                    break
                payload_clean["exit_name"] = m.group(1)
            if action == "move" and payload_clean.get("exit_name") == "$hash_tunnel":
                text = last_response.get("description", "") or str(last_response)
                tunnel = _find_tunnel_by_hash(text)
                if not tunnel:
                    break
                payload_clean["exit_name"] = tunnel
            path, body = _path_and_body(action, payload_clean)
            if export_curl and path and body is not None:
                curl_requests.append((path, body))
            try:
                if action == "start":
                    r = client.post(
                        f"{BASE_URL}/game/start", headers=HEADERS, json=payload_clean
                    )
                elif action == "examine":
                    r = client.post(
                        f"{BASE_URL}/game/examine", headers=HEADERS, json=payload_clean
                    )
                elif action == "move":
                    r = client.post(
                        f"{BASE_URL}/game/move", headers=HEADERS, json=payload_clean
                    )
                elif action == "take":
                    r = client.post(
                        f"{BASE_URL}/game/take", headers=HEADERS, json=payload_clean
                    )
                elif action == "drop":
                    r = client.post(
                        f"{BASE_URL}/game/drop", headers=HEADERS, json=payload_clean
                    )
                elif action == "use":
                    r = client.post(
                        f"{BASE_URL}/game/use", headers=HEADERS, json=payload_clean
                    )
                else:
                    continue
                r.raise_for_status()
                data = r.json() if r.content else {}
                if isinstance(data, dict):
                    last_response = data
                if action == "take" and data.get("level_complete"):
                    msg = data.get("message", "")
                    m = SCORE_PATTERN.search(msg)
                    if m:
                        print(m.group(1))
                    break
            except (httpx.HTTPStatusError, Exception):
                break
    if export_curl and curl_requests:
        _emit_bash_script(curl_requests)


if __name__ == "__main__":
    main()
