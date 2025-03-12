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
