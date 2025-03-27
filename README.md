This example contains a simple starter project which includes two different agents, one written in Python and one in JavaScript.
## Running the Agent

First, install the backend dependencies:

### Python SDK

```sh
cd agent-py
poetry install
```

Then, copy a `.env` file from `.env.example` inside `.agent`.

IMPORTANT:
Make sure the OpenAI API Key you provide, supports gpt-4o.

Then, run the demo:

Python

```sh
poetry run demo
```


## Running the UI

First, install the dependencies:

```sh
cd ./ui
pnpm i
```

Then, copy a `.env` file from `.env.example` inside `./ui`.


```sh
pnpm run dev
```

## Usage

Navigate to [http://localhost:3000](http://localhost:3000).

# LangGraph Studio

Run LangGraph studio, then load the `./agent` folder into it.

Make sure to create the `.env` mentioned above first!

```docker
docker build -t chatagent_backend .
➜ docker buildx build \                                                                              
  --platform linux/amd64,linux/arm64 \
  -t bangnguyen781209/chatagent_backend:latest \
  --push .
docker pull bangnguyen781209/chatagent_backend:latest
docker run -d --name backend --network agent-network --env-file ./backend/.env -p 8000:8000 chatagent_backend
-------------------
docker build -t chatagent_coplilot .
➜ docker buildx build \                                                                              
  --platform linux/amd64,linux/arm64 \
  -t bangnguyen781209/chatagent_copilotkit:latest \
  --push .
docker pull bangnguyen781209/chatagent_copilotkit:latest
docker run -d --network agent-network --env-file ./ui/.env -p 3000:3000 chatagent_copilotkit
docker compose -f docker-compose.yml up -d
docker compose -f docker-compose.yml down -v
---------------------
docker save -o chatagent_backend.tar chatagent_backend:latest
docker save -o chatagent_copilot.tar chatagent_copilot:latest
```
