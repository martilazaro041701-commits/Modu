# bark

BARK: Body-Shop Analytics & Reporting Kernel 🐾  BARK is a full-stack workflow app transitioning automotive shops from static sheets to real-time data. It provides a centralized "Kernel" for managing repair lifecycles and technician assignments. As the operational base for the COVY ecosystem, BARK turns manual logs into actionable analytics.

## Stack
- Backend: Python, Django, Django REST Framework, MySQL (via PyMySQL)
- Frontend: React + Vite + React Router
- Tooling: virtualenv (`.venv`)

## Quickstart
1) Create your `.env` files  
   - Backend: `cd backend && cp .env.example .env` and fill `MYSQL_*` creds + `DJANGO_SECRET_KEY`.  
     - CORS defaults allow `http://localhost:5173`; adjust `CORS_ALLOWED_ORIGINS`/`CSRF_TRUSTED_ORIGINS` as needed.  
   - Frontend: `cd frontend && cp .env.example .env` to point to your API base URL.

2) Backend (Django + DRF)  
   ```bash
   cd backend
   ../.venv/bin/python manage.py migrate   # requires a running MySQL instance
   ../.venv/bin/python manage.py runserver
   ```
   The API health endpoint is at `http://localhost:8000/api/health/`.

3) Frontend (React + Vite)  
   Node.js (>=18) is required. Once installed:  
   ```bash
   cd frontend
   npm install
   npm run dev
   ```
   Vite serves the app on `http://localhost:5173/` by default.

## Notes
- MySQL: Install MySQL server/client locally and create a `bark` database (or adjust env values). If you want `mysqlclient`, install MySQL client libs so `mysql_config` is available; current setup uses pure-Python `PyMySQL`.
- Virtualenv: All Python packages are installed into `.venv`. Use `source .venv/bin/activate` (or call `../.venv/bin/python ...`) when working in `backend/`.
- Frontend: React Router is pre-wired with an API status page. Axios requests go through `frontend/src/api/client.js`.
