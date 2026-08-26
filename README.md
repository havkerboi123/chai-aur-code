# GDG Live Pakistan — Chai aur Code Showcase

A project showcase site for GDG Live Pakistan's monthly "Chai aur Code" series.
Episode 1 collected ~100 project submissions via Google Forms; this site lists
them so people can browse what everyone built.

Static site, no backend — project data lives in
[`frontend/src/data/projects.json`](frontend/src/data/projects.json) and ships
with the build.

## Running locally

```bash
cd frontend
npm install
npm run dev
```

Opens at http://localhost:5173 (or whatever port Vite picks).

## Updating project data

Edit `frontend/src/data/projects.json` directly and redeploy. Each entry:

```json
{
  "id": 1,
  "name": "Project Name",
  "description": "...",
  "github_url": "https://github.com/...",
  "deployed_url": "https://...",
  "submitter": "Full Name",
  "episode": "Episode 1"
}
```

## Deploying

```bash
cd frontend
vercel --prod
```

## Notes / next steps

- Comments on projects were intentionally left out of this first version —
  add them later once there's a plan for moderation/auth (would need a
  backend again at that point).
