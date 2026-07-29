# LLM Tools Demo: Recipe Agent & Langfuse Observability Demo

This repository is a practical demonstration of integrating modern LLM tools. It focuses on using **Pydantic** for structured data validation and **Langfuse** for comprehensive LLM observability and tracing.

## 1. Environment Setup (using uv)

This project uses [uv](https://github.com/astral-sh/uv), an extremely fast Python package manager, to handle dependencies.

### Install uv
```bash
pip install uv
```
Verify the installation: `uv --version`

### Install Dependencies
This project includes a `pyproject.toml` file. To install everything, run:
```bash
uv sync
```
> **Note:** `uv sync` reads the dependencies in `pyproject.toml` and installs them into a virtual environment. It works similarly to `pip install -r requirements.txt` but performs parallel downloads, making it significantly faster. This will install `pydantic`, `langfuse`, `openai`, and other necessary libraries.

### Activate Virtual Environment
After running `uv sync`, a virtual environment folder `.venv/` is created. You can activate it manually:
- **Linux / Mac:**
  ```bash
  source .venv/bin/activate
  ```
- **Windows:**
  ```powershell
  .\.venv\Scripts\Activate.ps1
  ```
- **To exit:** Type `deactivate`.

**Documentation References:**
- [Pydantic AI Documentation](https://pydantic.dev/docs/ai/overview/install/)
- [Langfuse SDK Documentation](https://langfuse.com/docs/observability/sdk/overview)

---

## 2. Self-Hosting Langfuse with Docker

We use a self-hosted instance of Langfuse to monitor the LLM generation process.

### Prerequisites (Docker)
Ensure you have Docker installed. If not, download it here:
[Get Docker](https://www.docker.com/get-started/)

### Start the Service
A `docker-compose.yml` file is already included in this repo (sourced from the [Langfuse Self-Hosting Guide](https://langfuse.com/self-hosting/deployment/docker-compose)).

Run the following command to start the stack:
```bash
# Start in background mode
docker compose up -d
```
> **Note:** On the first run, Docker will pull several images (Minio, Postgres, Clickhouse, Redis, Langfuse). This may take at least 2 minutes. Once finished, access the dashboard at: [http://localhost:3000](http://localhost:3000)

---

## 3. Langfuse Initial Configuration

1. **Sign Up:** Access `http://localhost:3000`. You will need to create an account. Since this is self-hosted, you can use any name and email (e.g., `test@test.com`). Your data remains local.
2. **Create Project:** Once logged in, create an **Organization** and then a **Project**.
3. **Get API Keys:**
   - Go to **Settings** in the sidebar.
   - Under **API Keys**, click **Create New API Keys**.
   - Copy the `LANGFUSE_PUBLIC_KEY`, `LANGFUSE_SECRET_KEY`, and `LANGFUSE_HOST`.

---

## 4. Environment Variables (.env)

Copy the template file to create your `.env` file:
```bash
cp .env-template .env
```

Open `.env` and fill in your credentials:
```env
# OpenAI API Key
OPENAI_API_KEY=sk-proj-...

# Langfuse Configuration
LANGFUSE_PUBLIC_KEY=pk-lf-...
LANGFUSE_SECRET_KEY=sk-lf-...
LANGFUSE_HOST=http://localhost:3000
```

---

## 5. Running the Recipe Agent

Execute the main script to start the interactive Agent:
```bash
python main.py
```

### How it works:
1. **Interactive Prompt:** The script will ask: `What do you like to eat today?`.
2. **AI Logic:** The Agent generates a detailed recipe including difficulty (easy/medium/hard), ingredients (name/amount), step-by-step instructions, cooking time, and a brief chef's comment.
3. **Structured Output:** The output is strictly controlled by a **Pydantic Model**, ensuring the LLM always returns a valid schema.
4. **Local Storage:** Every generated recipe is saved as a JSON file in the `./output/` directory.

---

## 6. Monitoring and Tracing

After interacting with the Agent, go to your Langfuse dashboard ([localhost:3000](http://localhost:3000)):

- Click on the **Tracing** tab.
- You will see a trace for every request made to the Agent.
- Drill down into a trace to see exactly how the `recipe_agent` called the `llm_generation` function.
- You can inspect the raw Input/Output, Token usage, Latency, and verify that the `@observe` decorators are capturing the flow correctly.

---

## Advanced Exploration

Once you are comfortable with the basics, try exploring other Langfuse features:
- **Prompt Version Control:** Manage and version your prompts through the UI.
- **Tracing Tags:** Categorize your traces for better filtering.
- **Evaluation:** Set up manual or automated scoring to grade the quality of the recipes.

Enjoy building with **Pydantic** and **Langfuse**!