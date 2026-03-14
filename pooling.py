import asyncio
import os
import re
import time

import httpx

BASE_URL = "https://adventure.wietsevenema.eu"
API_KEY = os.getenv(
    "ADK_API_KEY",
    "fc73378f4efaf73c809944522a0e04370b2a5a3f1d57124be211dd363beaf3ad",
)


async def run_adventure():
    headers = {
        "Authorization": f"ApiKey {API_KEY}",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }

    start_time = time.perf_counter()

    async with httpx.AsyncClient(
        base_url=BASE_URL,
        headers=headers,
        http2=True,
        timeout=10,
    ) as client:

        async def fire(path, payload):
            return await client.post(path, json=payload)

        await fire("/game/start", {"level_id": "level-1"})

        await fire("/game/take", {"item_name": "amber chunk"})
        await fire("/game/take", {"item_name": "flint"})
        await fire("/game/take", {"item_name": "steel striker"})

        await fire(
            "/game/use", {"direct_object": "steel striker", "indirect_object": "flint"}
        )
        await fire("/game/move", {"exit_name": "north"})
        await fire("/game/drop", {"item_name": "thermal override flare"})
        await fire("/game/move", {"exit_name": "east"})
        await fire("/game/take", {"item_name": "brass control key"})
        await fire("/game/move", {"exit_name": "west"})
        await fire("/game/move", {"exit_name": "west"})
        await fire(
            "/game/use",
            {
                "direct_object": "brass control key",
                "indirect_object": "manual override slot",
            },
        )
        await fire("/game/move", {"exit_name": "north"})
        await fire(
            "/game/use",
            {"direct_object": "steel striker", "indirect_object": "amber chunk"},
        )

        r = await fire(
            "/game/take",
            {"item_name": "Heliostat Automation Module"},
        )

    elapsed = time.perf_counter() - start_time

    score_match = re.search(r"score of (\d+)", r.text)
    if score_match:
        print(score_match.group(1))
    else:
        print("Score not found in final response.")

    print(f"{elapsed:.3f}s")


if __name__ == "__main__":
    asyncio.run(run_adventure())
