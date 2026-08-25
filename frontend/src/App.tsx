import { useEffect, useMemo, useState } from 'react';
import { fetchProjects, type Project } from './api';
import './App.css';

function ProjectCard({ project }: { project: Project }) {
  return (
    <article className="card">
      <h3 className="card-title">{project.name}</h3>
      <p className="card-desc">{project.description}</p>
      {project.submitter && <p className="card-submitter">by {project.submitter}</p>}
      <div className="card-links">
        <a href={project.deployed_url || project.github_url} target="_blank" rel="noreferrer">
          {project.deployed_url ? 'Live site' : 'View code'}
        </a>
        {project.deployed_url && (
          <a href={project.github_url} target="_blank" rel="noreferrer">
            Source
          </a>
        )}
      </div>
    </article>
  );
}

export default function App() {
  const [projects, setProjects] = useState<Project[]>([]);
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchProjects()
      .then(setProjects)
      .catch(() => setError('Could not reach the backend. Is it running?'))
      .finally(() => setLoading(false));
  }, []);

  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase();
    if (!q) return projects;
    return projects.filter(
      (p) =>
        p.name.toLowerCase().includes(q) ||
        p.description.toLowerCase().includes(q) ||
        (p.submitter ?? '').toLowerCase().includes(q),
    );
  }, [projects, query]);

  return (
    <div className="page">
      <header className="hero">
        <p className="hero-kicker">GDG Live Pakistan</p>
        <h1>
          Chai <span className="urdu">اور</span> Code
        </h1>
        <p className="hero-event-desc">
          A monthly building series from GDG Live Pakistan, meant to push developers to stop
          planning and actually ship something cool.
        </p>
        <p className="hero-sub">
          {projects.length > 0 ? projects.length : '100'} projects from the community, built and
          submitted for episode one. Have a look around.
        </p>
        <input
          className="search"
          type="text"
          placeholder="Search by project, idea, or builder"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
      </header>

      <main className="content">
        <h2 className="section-heading">Episode 1: Projects</h2>
        {loading && <p className="state-msg">Loading projects…</p>}
        {error && <p className="state-msg state-error">{error}</p>}
        {!loading && !error && filtered.length === 0 && (
          <p className="state-msg">Nothing matches "{query}".</p>
        )}
        {!loading && !error && filtered.length > 0 && (
          <div className="grid">
            {filtered.map((p) => (
              <ProjectCard key={p.id} project={p} />
            ))}
          </div>
        )}

        <h2 className="section-heading section-heading-muted">Episode 2: Coming soon</h2>
        <p className="coming-soon">Submissions aren't open yet. Check back after the next meetup.</p>
      </main>

      <footer className="footer">GDG Live Pakistan · Chai aur Code</footer>
    </div>
  );
}
