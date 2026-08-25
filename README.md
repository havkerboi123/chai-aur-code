# GDG Live Pakistan — Chai aur Code Showcase

A project showcase site for GDG Live Pakistan's monthly "Chai aur Code" series.
Episode 1 collected ~100 project submissions via Google Forms; this site lists
them so people can browse what everyone built.

## Structure

- `frontend/` — React + Vite + TypeScript, minimal green/light UI
- `backend/` — FastAPI + SQLite

## Running locally

**Backend**

```bash
cd backend
python3 -m venv venv        # if not already created
./venv/bin/pip install -r requirements.txt
./venv/bin/uvicorn main:app --reload --port 8000
```

The API auto-seeds a handful of sample projects on first run so the frontend
has something to show immediately.

**Frontend**

```bash
cd frontend
npm install
npm run dev
```

Opens at http://localhost:5173, talking to the API at http://localhost:8000
(override with a `VITE_API_URL` env var / `.env` file if needed).

## Importing the real Episode 1 submissions

Once you have the Google Sheet of form responses, publish/share it and run:

```bash
cd backend
./venv/bin/python import_sheet.py "<google sheet url>"
```

It matches columns loosely (project name, description, GitHub link, deployed
URL, submitter name) so slightly different header wording is fine. It adds to
whatever's already in the DB — delete `backend/gdg.db` first if you want to
start fresh instead of appending.

## Notes / next steps

- Comments on projects were intentionally left out of this first version —
  add them later once there's a plan for moderation/auth.
- Deploy the backend anywhere that runs Python (Railway, Render, Fly.io) and
  the frontend anywhere static (Vercel, Netlify, GitHub Pages), pointing
  `VITE_API_URL` at the deployed backend.
