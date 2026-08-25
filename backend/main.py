from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from db import get_connection, init_db
from seed import seed

app = FastAPI(title="GDG Live Pakistan — Chai aur Code")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    init_db()
    seed()


@app.get("/api/projects")
def list_projects(episode: str | None = None):
    conn = get_connection()
    if episode:
        rows = conn.execute(
            "SELECT * FROM projects WHERE episode = ? ORDER BY id", (episode,)
        ).fetchall()
    else:
        rows = conn.execute("SELECT * FROM projects ORDER BY id").fetchall()
    conn.close()
    return [dict(row) for row in rows]


@app.get("/api/projects/{project_id}")
def get_project(project_id: int):
    conn = get_connection()
    row = conn.execute("SELECT * FROM projects WHERE id = ?", (project_id,)).fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Project not found")
    return dict(row)


@app.get("/api/health")
def health():
    return {"status": "ok"}
