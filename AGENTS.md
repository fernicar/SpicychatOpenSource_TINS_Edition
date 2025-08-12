# TINS Documentation for this Project

## `main.py`

### Description

This is the main entry point of the FastAPI application. It imports the `app` object from the `app.api` module, which is expected to be a `FastAPI` instance. This file is responsible for starting the web server when executed.

### Functionality

- Imports the FastAPI application instance.
- When run with a web server like Uvicorn, it will serve the application.

### Technical Implementation

- **Framework:** FastAPI
- **Dependencies:** `fastapi`, `uvicorn` (for running)
- **Structure:** Imports the `app` object from `app.api`.

## `app/api/ai.py`

### Description

This module defines the `AI` class, which is responsible for handling chat interactions with a Large Language Model (LLM). It is designed to be stateful, with a specific character and model loaded for each instance.

### Functionality

- **`AI` class:**
  - Initializes with a `character_id` and a `model` name.
  - `set_character(character_id)`: Fetches character details and settings using `get_character` from `app.api.bs`.
  - `set_model(model)`: Sets the language model to be used.
  - `chat(message, history)`:
    - Takes a user message and conversation history as input.
    - Constructs a message payload for the LLM, including system prompts from character settings.
    - Uses the `ollama` library to make an asynchronous request to the LLM's API.
    - Streams the response from the LLM.
- It can be configured with a `DEFAULT_MODEL` through an environment variable.

### Technical Implementation

- **Dependencies:** `ollama`, `requests`
- **Modules:**
  - `os`: To get environment variables.
  - `json`: For data serialization.
  - `typing.Callable`: For type hinting.
  - `ollama`: The primary library for interacting with the LLM.
  - `requests`: Used for making HTTP requests (though not explicitly used in the `chat` method, it's imported).
  - `app.api.bs`: For fetching character and model data.
- **Architecture:** The `AI` class encapsulates the logic for a single chat session with a specific character and model. It's designed to be used within an async environment.

## `app/api/ai2.py`

### Description

This module provides an alternative, more direct implementation for interacting with a chat AI service. Unlike `ai.py`, it does not use the `ollama` library but instead makes asynchronous HTTP requests using `httpx`. It is structured around a `chat` function and includes a command-line test harness. A significant part of this module is a hardcoded, detailed, and explicit persona for the AI character "Sunny".

### Functionality

- `chat(settings, model, messages)`:
  - An asynchronous function that takes system settings, a model name, and a list of messages.
  - Sends a POST request to the AI service endpoint defined by the `AI_URL` environment variable.
  - Streams the response from the service.
- `test()`:
  - An asynchronous function that runs a command-line chat loop.
  - It uses the hardcoded "Sunny" persona and a specific model.
  - It manages the conversation history and prompts the user for input.

### Technical Implementation

- **Dependencies:** `httpx`
- **Modules:**
  - `os`: To get the AI service URL from environment variables.
  - `json`: For parsing the streamed response data.
  - `httpx`: For making asynchronous HTTP requests.
  - `asyncio`: Used to run the `test` function.
- **Data:**
  - It contains a large, hardcoded string `settings` that defines the "Sunny" persona with explicit instructions for role-playing.
  - The `data` dictionary is a template for the API request body.
- **Authentication:** It expects an API key to be provided in the `headers`, but the value is an empty string by default.

## `app/api/bs.py`

### Description

This module serves as a data access layer for the application. It provides a set of functions to perform CRUD (Create, Read, Update, Delete) operations on the database for various entities such as users, AI models, characters, chat rooms, and messages. The name `bs.py` likely stands for "business services" or "backend services".

### Functionality

- **User Management:**
  - `get_user(user_id)`: Retrieves a user by their ID.
  - `create_user(user_id, nickname)`: Creates a new user.
- **AI Model Management:**
  - `get_model_by_name(name)`: Retrieves an AI model's configuration by its name.
  - `get_models()`: Retrieves a list of all available AI models, ordered by `ordinal`.
- **Character Management:**
  - `get_characters()`: Retrieves all characters.
  - `get_character(character_id)`: Retrieves a specific character by its ID.
- **Chat Room Management:**
  - `get_or_create_room(user_id, character_id)`: Retrieves an existing chat room for a user and character, or creates a new one if it doesn't exist.
  - `create_room(user_id, character_id)`: Creates a new chat room.
  - `get_room_history(room_id)`: Fetches the message history for a given room.
  - `clear_room_history(room_id)`: Deletes all messages from a room.
- **Message Management:**
  - `save_message(...)`: Saves a new chat message to the database.

### Technical Implementation

- **Dependencies:** `app.storage.db`
- **Database Interaction:**
  - It uses the `get_cursor()` context manager from `app.storage.db` to execute raw SQL queries.
  - The functions are synchronous and perform blocking database operations.
- **Data Handling:**
  - Functions return data fetched from the database, typically as dictionaries or lists of dictionaries.
  - Timestamps are handled using the `datetime` module.

## `app/api/chat.py`

### Description

This module implements the real-time chat functionality using WebSockets. It defines the `Message` class for standardizing message formats and the `Room` class, which manages the lifecycle of a WebSocket connection for a single user's chat session.

### Functionality

- **`Message` class:**
  - A data class to represent a single message in the chat.
  - `to_json()`: Serializes the message object into a JSON-compatible dictionary.
- **`Room` class:**
  - Manages a WebSocket connection for a user.
  - `wait_message()`: An infinite loop that waits for incoming JSON messages from the client's WebSocket.
  - `receive_message(message)`: A message dispatcher that routes incoming messages to the appropriate handler based on the `event` field.
  - **Event Handlers:**
    - `invite(message)`: Handles the initial setup of a chat room with a character. It creates a room in the database if one doesn't exist and sends the user their ID.
    - `set_model(message)`: Updates the AI model used for the chat.
    - `send_history()`: Fetches the chat history from the database and sends it to the client.
    - `clear_history()`: Clears the chat history for the room.
    - `chat(message)`:
      - Takes a user's message.
      - Gets the current chat history.
      - Calls the `AI.chat()` method to get a streamed response from the LLM.
      - Streams the response back to the client word by word (`message_stream`).
      - Sends a `message_end` event when the full response is received.
      - Saves both the user's message and the AI's full response to the database.

### Technical Implementation

- **Dependencies:** `fastapi`, `app.api.bs`, `app.api.ai`
- **Protocol:** Uses WebSockets for real-time, bidirectional communication.
- **State Management:** The `Room` class instance holds the state for a single chat session, including the user ID, character ID, model, and the `AI` instance.
- **Asynchronicity:** The entire module is built around `async/await` to handle WebSocket communication and AI model streaming non-blockingly.

## `app/api/session.py`

### Description

This module provides a custom ASGI middleware, `RedisSessionMiddleware`, for managing user sessions in a FastAPI application. It uses a Redis backend to store session data, making sessions persistent across multiple requests and application restarts.

### Functionality

- **`RedisSessionMiddleware` class:**
  - An ASGI middleware that intercepts HTTP and WebSocket connections.
  - **Session Creation:** If a session cookie is not found in the request, it creates a new session with a unique ID (UUID4) and an empty session dictionary in the request `scope`.
  - **Session Loading:** If a session cookie is present, it uses the cookie's value as a session ID to retrieve session data from the Redis database. The deserialized data is then attached to the request `scope['session']`.
  - **Session Persistence:** After the request is processed, it checks if the `scope['session']` has been modified.
    - If the session has data, it is serialized to JSON and stored in Redis with the session ID as the key. A `Set-Cookie` header is sent to the client with the session ID.
    - If the session is empty but was not initially empty (i.e., the session was cleared), it sends a `Set-Cookie` header that expires the client's session cookie.
  - **Configuration:** The middleware is configurable for the session cookie name, session duration (`max_age`), cookie path, `SameSite` attribute, `https_only` flag, and domain.

### Technical Implementation

- **Dependencies:** `redis`, `starlette`
- **Protocol:** It's an ASGI middleware, designed to work with any ASGI-compliant framework like FastAPI or Starlette.
- **Storage:** Uses a Redis client (`redis.Redis`) to store session data as JSON strings.
- **Security:** It includes security features for cookies like `httponly`, `samesite`, and `secure` flags.

## `app/storage/db.py`

### Description

This module is responsible for managing the connection to the PostgreSQL database. It initializes a database client and provides helper functions to access the database connection and cursors.

### Functionality

- **Database Connection:**
  - It establishes a connection to a PostgreSQL database using the `psycopg2` library.
  - The connection details are provided via the `DATABASE_URL` environment variable. A default connection string is used if the environment variable is not set.
  - The connection is configured to use `DictCursor`, which means database rows are returned as dictionary-like objects.
  - `autocommit` is set to `True`, so every database operation is immediately committed.
- **Accessor Functions:**
  - `get_db()`: Returns the global database connection object.
  - `get_cursor()`: Returns a new database cursor for executing queries.

### Technical Implementation

- **Dependencies:** `psycopg2-binary` (or `psycopg2`)
- **Modules:** `os`, `psycopg2`
- **Architecture:** It creates a single, global connection pool (`postgres_client`) when the module is first imported. This connection is then shared across the application. This pattern can be problematic in multi-threaded or highly concurrent applications.

## `app/storage/redis.py`

### Description

This module manages the connection to a Redis server. It initializes a Redis client and provides helper functions for session management, which are likely used by the `RedisSessionMiddleware`.

### Functionality

- **Redis Connection:**
  - It creates a connection to a Redis server using the `redis-py` library.
  - Connection parameters (host, port, and database number) are configured via environment variables (`REDIS_HOST`, `REDIS_PORT`, `REDIS_DB`), with default values for a local Redis instance.
  - The client is configured with `decode_responses=True`, so responses from Redis are automatically decoded from bytes to UTF-8 strings.
- **Session Functions:**
  - `get_session(session_id)`: Retrieves a session from Redis by its ID. It expects the session data to be stored as a JSON string and deserializes it into a dictionary.
  - `save_session(session_id, session)`: Serializes a session dictionary into a JSON string and stores it in Redis with the session ID as the key.

### Technical Implementation

- **Dependencies:** `redis`
- **Modules:** `os`, `redis`, `json`
- **Architecture:** Similar to `db.py`, it creates a single global Redis client instance (`redis_client`) that is shared across the application.

## `app/utils/templates.py`

### Description

This module provides a configured instance of `Jinja2Templates` for use throughout the FastAPI application. This allows for server-side rendering of HTML templates.

### Functionality

- It creates a single, global `templates` object of type `Jinja2Templates`.
- The `Jinja2Templates` instance is configured to look for templates in the `app/templates` directory.

### Technical Implementation

- **Dependencies:** `fastapi` (specifically `fastapi.templating`)
- **Modules:** `fastapi.templating.Jinja2Templates`
- **Usage:** This `templates` object can be imported into API route modules to render and return HTML responses (e.g., `return templates.TemplateResponse("index.html", {"request": request})`).

## `hall/server.py`

### Description

This module sets up a FastAPI application to serve a static frontend application. It is likely the web server for the "hall" part of the project, which appears to be a Single-Page Application (SPA).

### Functionality

- It creates a FastAPI application instance.
- It mounts a `StaticFiles` server at the root path (`/`).
- The server is configured to serve files from the `dist` directory.
- The `html=True` option enables it to serve `index.html` for requests to `/`, which is characteristic of an SPA server.

### Technical Implementation

- **Dependencies:** `fastapi`, `uvicorn` (for running)
- **Modules:** `fastapi.FastAPI`, `fastapi.staticfiles.StaticFiles`
- **Architecture:** This is a minimal web server designed solely to serve the compiled frontend assets. It does not contain any API endpoints itself. The frontend code is expected to be in the `src` directory, compiled into the `dist` directory by a build tool like Vite (as suggested by `vite.config.js`).

## `hall/test.py`

### Description

This file is a small, standalone Python script that appears to be a test or example snippet for interacting with an OpenAI-compatible API. It is not an automated test and is not integrated into the main application.

### Functionality

- It demonstrates how to initialize the `openai.OpenAI` client.
- It shows how to configure the client with a custom `api_key` and `base_url`.
- It includes a sample call to `client.chat.completions.create` to generate chat completions.

### Technical Implementation

- **Dependencies:** `openai`
- **Modules:** `openai`
- **Note:** The code in this file is incomplete and contains placeholder text ("你的API密钥" which means "your API key") and an example `base_url`. It cannot be run as-is without modification.

## Project File Structure

```
.
├── Dockerfile
├── README.md
├── app
│   ├── __init__.py
│   ├── ai
│   │   ├── ds14b
│   │   ├── ds32b
│   │   ├── mistral
│   │   └── qwq
│   ├── api
│   │   ├── __init__.py
│   │   ├── ai.py
│   │   ├── ai2.py
│   │   ├── bs.py
│   │   ├── chat.py
│   │   └── session.py
│   ├── static
│   │   ├── 1e833650-4f20-4361-ab01-4af3cc38c690.png
│   │   ├── main.css
│   │   └── main.js
│   ├── storage
│   │   ├── __init__.py
│   │   ├── db.py
│   │   └── redis.py
│   ├── templates
│   │   ├── chat.html
│   │   ├── global.css
│   │   ├── index.jinja2
│   │   └── style.css
│   └── utils
│       ├── __init__.py
│       └── templates.py
├── hall
│   ├── Dockerfile
│   ├── index.html
│   ├── package-lock.json
│   ├── package.json
│   ├── server.py
│   ├── src
│   │   ├── App.vue
│   │   ├── main.js
│   │   └── page
│   │       ├── anime.css
│   │       ├── anime.vue
│   │       ├── chat.css
│   │       ├── chat.vue
│   │       ├── girls.css
│   │       └── girls.vue
│   ├── test.py
│   └── vite.config.js
├── main.py
├── requirements.txt
└── sync.sh
```
