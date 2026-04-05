# Athletiq Backend

FastAPI + PostgreSQL async REST API for the Athletiq athlete performance tracking platform.

## Tech Stack

- **FastAPI** — async Python web framework
- **SQLAlchemy 2.0** — async ORM with `asyncpg`
- **PostgreSQL** — primary database
- **Alembic** — database migrations
- **Passlib + bcrypt** — password hashing
- **python-jose** — JWT authentication
- **Pydantic v2** — data validation

## Project Structure

```
Athletiq_backend/
├── app/
│   ├── db/           # Database engine, session, base models
│   ├── models/       # SQLAlchemy ORM models
│   ├── routers/      # FastAPI route handlers
│   ├── schemas/      # Pydantic request/response schemas
│   ├── services/     # Business logic (analytics, comparison, auth)
│   └── utils/        # Security helpers (JWT, hashing)
├── main.py           # FastAPI app entrypoint
├── requirements.txt
└── .env.example
```

## API Overview

| Prefix | Description |
|---|---|
| `/auth` | Register, login, OTP verify, forgot/reset password |
| `/athletes` | CRUD for athlete profiles |
| `/athletes/{id}/metrics/{type}` | Log and retrieve metrics (speed, stamina, strength, heart-rate, vo2-max, sleep, recovery, fatigue) |
| `/athletes/{id}/training` | Training session logging |
| `/athletes/{id}/analytics` | Per-athlete trends, heatmap, averages |
| `/analytics/global-summary` | Platform-wide stats |
| `/analytics/team-summary` | Bulk athlete summaries |
| `/compare` | Radar and metric comparison across athletes |

## Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/RakshaKirishnan/Athletiq-backend.git
cd Athletiq-backend
```

### 2. Create and configure `.env`

```bash
cp .env.example .env
```

Edit `.env` and fill in your values:

```env
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/athletiq
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# Email (for OTP)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your@email.com
SMTP_PASSWORD=your-app-password
EMAIL_FROM=your@email.com
```

### 3. Set up virtual environment

**macOS / Linux**
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**Windows**
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### 4. Run database migrations

```bash
alembic upgrade head
```

### 5. Start the server

```bash
python main.py
```

The API will be live at `http://localhost:8000`  
Interactive docs: `http://localhost:8000/docs`

## Development

```bash
# Run with auto-reload
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Notes

- All endpoints (except `/auth/*`) require a `Bearer` JWT token in the `Authorization` header
- OTP codes expire after 5 minutes with a 60-second resend cooldown
- Metrics support both underscore (`heart_rate`) and hyphen (`heart-rate`) URL formats
