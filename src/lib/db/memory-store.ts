// Temporary in-memory store for testing when database is unavailable
interface Project {
  id: string;
  name: string;
  clientName?: string | null;
  description?: string | null;
  status: string;
  createdAt: Date;
  updatedAt: Date;
}

interface Generation {
  id: string;
  projectId: string;
  prompt: string;
  output: string;
  model: string;
  temperature?: number | null;
  generationType: string;
  metadata?: string | null;
  createdAt: Date;
}

class MemoryStore {
  private projects: Map<string, Project> = new Map();
  private generations: Map<string, Generation> = new Map();
  private feedbacks: Map<string, any> = new Map();
  private edits: Map<string, any> = new Map();

  createProject(data: { name: string; clientName?: string; description?: string }) {
    const project: Project = {
      id: `proj_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      name: data.name,
      clientName: data.clientName || null,
      description: data.description || null,
      status: 'ACTIVE',
      createdAt: new Date(),
      updatedAt: new Date(),
    };
    
    this.projects.set(project.id, project);
    return project;
  }

  getProject(id: string) {
    return this.projects.get(id) || null;
  }

  getProjects(status?: string) {
    const projects = Array.from(this.projects.values());
    if (status) {
      return projects.filter(p => p.status === status);
    }
    return projects;
  }

  createGeneration(data: any) {
    const generation: Generation = {
      id: `gen_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      ...data,
      createdAt: new Date(),
    };
    
    this.generations.set(generation.id, generation);
    return generation;
  }

  getProjectGenerations(projectId: string) {
    return Array.from(this.generations.values())
      .filter(g => g.projectId === projectId)
      .sort((a, b) => b.createdAt.getTime() - a.createdAt.getTime());
  }
}

// Global singleton for Next.js hot reloading
declare global {
  var memoryStoreInstance: MemoryStore | undefined;
}

// This ensures the same instance is used across hot reloads
export const memoryStore = global.memoryStoreInstance || (global.memoryStoreInstance = new MemoryStore());