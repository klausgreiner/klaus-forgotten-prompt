#!/usr/bin/env bash
# Replay script; uses cookie jar for session.
set -e
BASE="https://adventure.wietsevenema.eu"
API_KEY="${ADK_API_KEY:-fc73378f4efaf73c809944522a0e04370b2a5a3f1d57124be211dd363beaf3ad}"
JAR=$(mktemp)
trap 'rm -f "$JAR"' EXIT

req() {
  curl -s -c "$JAR" -b "$JAR" -X POST \
    -H "Authorization: ApiKey $API_KEY" \
    -H "Content-Type: application/json" \
    -H "Accept: application/json" \
    -d "$1" "$BASE$2"
}

req '{"level_id":"level-2"}' /game/start >/dev/null
req '{"exit_name":"heavy blast door"}' /game/move >/dev/null
req '{"target":"decaying server racks"}' /game/examine >/dev/null
req '{"item_name":"bright yellow object"}' /game/take >/dev/null
req '{"target":"old CRT monitor"}' /game/examine >/dev/null
req '{"exit_name":"ventilation_shaft_delta"}' /game/move >/dev/null
req '{"target":"air-gapped mainframe"}' /game/examine >/dev/null
req '{"exit_name":"service_hatch_gamma"}' /game/move >/dev/null
req '{"item_name":"root access drive"}' /game/take | grep -oE 'score of [0-9]+' | grep -oE '[0-9]+'