const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export interface Project {
  id: number;
  name: string;
  description: string;
  github_url: string;
  deployed_url: string | null;
  submitter: string | null;
  episode: string;
  created_at: string;
}

export async function fetchProjects(): Promise<Project[]> {
  const res = await fetch(`${API_URL}/api/projects`);
  if (!res.ok) throw new Error('Failed to load projects');
  return res.json();
}
