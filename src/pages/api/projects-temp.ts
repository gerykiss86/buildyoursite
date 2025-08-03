import { NextApiRequest, NextApiResponse } from 'next';
import { memoryStore } from '@/lib/db/memory-store';

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  switch (req.method) {
    case 'GET':
      try {
        const { status } = req.query;
        const projects = memoryStore.getProjects(status as string);
        res.status(200).json(projects);
      } catch (error) {
        console.error('Error fetching projects:', error);
        res.status(500).json({ error: 'Failed to fetch projects' });
      }
      break;

    case 'POST':
      try {
        const { name, clientName, description } = req.body;
        
        if (!name) {
          return res.status(400).json({ error: 'Project name is required' });
        }

        const project = memoryStore.createProject({ name, clientName, description });
        console.log('Project created in memory:', project);
        
        res.status(201).json(project);
      } catch (error) {
        console.error('Error creating project:', error);
        res.status(500).json({ error: 'Failed to create project' });
      }
      break;

    default:
      res.setHeader('Allow', ['GET', 'POST']);
      res.status(405).end(`Method ${req.method} Not Allowed`);
  }
}