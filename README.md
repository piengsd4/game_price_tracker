# Game Price Tracker

Track Steam titles, search live prices, and manage a wishlist with a Vue + Django stack.

## What’s inside
- Django 5 + DRF backend with session auth, CSRF protection, and Postgres (trigram search on game titles).
- Vue 3 + Vite frontend with Pinia state, Vue Router, and toast notifications.
- Wishlist management (view/add), Steam search with fuzzy matching, and price badges for tracked games.

## Project structure
- `backend/` – Django project (base app is called `config/`) and `tracker` app with auth + wishlist API.
- `frontend/` – Vite/Vue SPA with components for search, wishlist, header/footer.

## Prerequisites
- Python 3.13+
- Node 20+ (or 22+)
- PostgreSQL with `pg_trgm` extension enabled for trigram search.

## Backend setup
1) `cd backend`
2) Install deps (Poetry): `poetry install`  
3) Ensure Postgres is running and matches `config/settings.py` (DB `game_price_tracker`, user `pieng`, password `pieng_test`, host `localhost`).
4) Enable trigram: `psql -d game_price_tracker -c "CREATE EXTENSION IF NOT EXISTS pg_trgm;"`
5) Run migrations: `python manage.py migrate`
6) Create a superuser (for login): `python manage.py createsuperuser`
7) Start API: `python manage.py runserver 8000`

CORS/CSRF: `CORS_ALLOWED_ORIGINS`/`CSRF_TRUSTED_ORIGINS` currently expect the frontend on `http://localhost:5173` (add or change ports here if needed).

## Frontend setup
1) `cd frontend`
2) Install deps: `npm install`
3) Run dev server: `npm run dev` (Vite defaults to `http://localhost:5173`)
4) Build: `npm run build`

The frontend expects the API at `http://localhost:8000` and uses session cookies. CSRF is handled via the `useCsrf` composable before POSTs.

## Key API endpoints
- `GET /api/auth/csrf/` – fetch CSRF token cookie
- `POST /api/auth/login/` – session login (username/password)
- `POST /api/auth/logout/` – logout
- `GET /api/auth/session/` – check session
- `GET /api/search/?query=...` – search Steam games (trigram)
- `GET /api/wishlist/steam` – user wishlist (auth required)
- `POST /api/wishlist/add/` – add appid to wishlist (auth + CSRF)
