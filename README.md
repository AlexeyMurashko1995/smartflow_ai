# Smartflow AI — Asynchronous AI-Powered Expense Tracker API & Bot 🚀

An asynchronous REST API and Telegram bot designed for automated expense tracking, natural language text processing, and voice message parsing powered by Artificial Intelligence.

## 🎯 Goal
This project demonstrates a production-ready asynchronous microservice architecture featuring JWT authentication, Redis caching, audio transcription via OpenAI Whisper, structured LLM expense parsing via Groq AI, and full Docker Compose orchestration.

## 🛠 Tech Stack
* **Backend Framework:** FastAPI (Asynchronous REST API)
* **Telegram Bot:** Aiogram 3 (Async Bot Framework)
* **Database & ORM:** PostgreSQL with Async SQLAlchemy 2.0 & Alembic migrations
* **Caching Layer:** Async Redis
* **AI & Speech Integration:** Groq AI API (`llama-3.3-70b-specdec`) & OpenAI Whisper (`whisper-large-v3-turbo`)
* **Security & Auth:** JWT Tokens (PyJWT), Password Hashing (Passlib / Bcrypt)
* **Containerization:** Docker & Docker Compose

## 🌟 Key Features
* **Asynchronous Architecture:** High-performance non-blocking database operations powered by `asyncpg` and `AsyncSession`.
* **Natural Language AI Parsing:** Automatically extracts amount, category, and description from freeform text input using Groq AI.
* **Voice-to-Text Expense Logging:** Downloads `.ogg` voice notes, transcribes speech via Whisper API, and saves parsed financial records.
* **JWT & Telegram Authentication:** Dual-mode authentication supporting standard email/password credentials and direct Telegram ID login.
* **High-Performance Caching:** Accelerates category management and summary endpoints using Redis with automatic cache invalidation.
* **Interactive Telegram Interface:** Built with Aiogram 3 utilizing FSM state management and dynamic inline keyboards.
* **Robust Docker Orchestration:** Fully containerized setup with PostgreSQL healthchecks to prevent startup race conditions.

## 🚀 API Endpoints & Bot Capabilities

### User Management (`/users`)
* `POST /users/` — Register a new user account.
* `POST /users/login` — Authenticate user and receive a JWT access token.
* `GET /users/me` — Retrieve current user profile (Protected).
* `POST /users/telegram-login` — Authenticate or auto-register user by Telegram ID.

### Categories Manager (`/categories`)
* `GET /categories/` — List user expense categories (Redis cached).
* `POST /categories/` — Create a new expense category.

### Expenses Manager (`/expenses`)
* `POST /expenses/` — Create an expense record manually.
* `GET /expenses/summary` — Retrieve aggregated expense summaries grouped by category (Redis cached).
* `POST /expenses/ai` — Parse natural language text into a structured expense record via AI.
* `POST /expenses/ai_voice` — Transcribe voice notes and save parsed expense records.

### Telegram Bot Commands
* `/start` — Authenticate user and store JWT access token.
* `/categories` — Fetch available user categories.
* `/add_expense` — Step-by-step manual expense entry with inline category selection.
* `/summary` — Display aggregated expense breakdown.
* `Text / Voice Message` — Direct AI expense parsing via Groq AI and Whisper.

## 🐳 Quick Start

1. Clone the repository and configure your `.env` file:

```env
DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/smartflow_db
SECRET_KEY=your_super_secret_key_123
BOT_TOKEN=your_telegram_bot_token
OPENAI_API_KEY=your_groq_api_key
```

2. Launch the fully isolated containerized stack:

```bash
docker compose up --build -d
```

3. Check service health and logs:

```bash
docker compose ps
docker compose logs -f
```

## 🌍 About Me
Based in Warsaw, Poland, focused on building clean, scalable Python backends, asynchronous data pipelines, and practical AI automation.
*Last updated: August 2026*