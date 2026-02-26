Test the Game API
Every action you took in the web interface corresponds to a specific HTTP request sent to the Game API. Some examples include looking around in the room, moving through an exit, and examining an item. Your agent will play the game by sending these same requests.

Authentication
To interact with the API, you need to prove who you are. This is done using an API Key. You must include this key in the Authorization header of every request, using the following format: Authorization: ApiKey YOUR_KEY.

Your personal API Key is:

fc73378f4efaf73c809944522a0e04370b2a5a3f1d57124be211dd363beaf3ad
The API is Stateful
Important: The Game API is stateful. The server remembers which level you are playing and your current location within it. You can only have one active game session at a time. If you call /game/start while a session is already active, the old session will be cancelled and a new one will begin.

Hands-on with curl
Now, try starting a level and executing a look command from your terminal using curl. This will help you understand exactly what your agent sees.

1. Start a Level
   First, you'll need to ensure you are in a valid state. Run this command to start (or restart) Level 0:

curl -X POST \
 https://adventure.wietsevenema.eu/game/start \
 -H "Authorization: ApiKey fc73378f4efaf73c809944522a0e04370b2a5a3f1d57124be211dd363beaf3ad" \
 -H "Content-Type: application/json" \
 -d '{"level_id": "level-0"}'
Expected Output:

2. Look Around
   Now that the level is active, ask the server for a description of the room:

curl -X GET \
 https://adventure.wietsevenema.eu/game/look \
 -H "Authorization: ApiKey fc73378f4efaf73c809944522a0e04370b2a5a3f1d57124be211dd363beaf3ad"
Expected Output:

You've just played the game without a browser! This JSON response is exactly what your agent will receive and analyze to decide its next move.

Available Endpoints
Here are the main endpoints your agent will use:

POST /game/start: Start a specific level.
GET /game/look: Get a description of your current location.
POST /game/move: Move in a direction (e.g., "north").
POST /game/take: Pick up an item.
POST /game/drop: Drop an item.
POST /game/use: Use an item, or two items together.
POST /game/examine: Get details about an item or feature.
GET /game/inventory: List items you are carrying.
Ready to Automate?
Manually sending API requests is tedious. It's time to build an AI agent that can do this for you. In the next section, you'll set up your development environment and create your first agent.
