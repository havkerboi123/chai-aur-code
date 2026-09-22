import { useMemo, useState } from 'react';
import { getProjects, type Project } from './api';
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

function episodeNumber(episode: string): number {
  const match = episode.match(/(\d+)/);
  return match ? parseInt(match[1], 10) : 0;
}

export default function App() {
  const [projects] = useState<Project[]>(getProjects);
  const [query, setQuery] = useState('');

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

  const episodes = useMemo(() => {
    const groups = new Map<string, Project[]>();
    for (const p of filtered) {
      const list = groups.get(p.episode) ?? [];
      list.push(p);
      groups.set(p.episode, list);
    }
    return Array.from(groups.entries()).sort(
      (a, b) => episodeNumber(b[0]) - episodeNumber(a[0]),
    );
  }, [filtered]);

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
          {projects.length} projects from the community, built and submitted across every
          episode. Have a look around.
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
        {episodes.length === 0 && <p className="state-msg">Nothing matches "{query}".</p>}
        {episodes.map(([episode, episodeProjects]) => (
          <section className="episode-section" key={episode}>
            <h2 className="section-heading">
              {episode}
              <span className="section-count">{episodeProjects.length} projects</span>
            </h2>
            <div className="grid">
              {episodeProjects.map((p) => (
                <ProjectCard key={p.id} project={p} />
              ))}
            </div>
          </section>
        ))}
      </main>

      <footer className="footer">GDG Live Pakistan · Chai aur Code</footer>
    </div>
  );
}
