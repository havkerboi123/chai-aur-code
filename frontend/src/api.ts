import projectsData from './data/projects.json';

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

export function getProjects(): Project[] {
  return projectsData as Project[];
}
