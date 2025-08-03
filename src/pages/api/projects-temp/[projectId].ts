import { NextApiRequest, NextApiResponse } from 'next';
import { memoryStore } from '@/lib/db/memory-store';

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  const { projectId } = req.query;
  
  if (!projectId || typeof projectId !== 'string') {
    return res.status(400).json({ error: 'Invalid project ID' });
  }

  switch (req.method) {
    case 'GET':
      try {
        const project = memoryStore.getProject(projectId);
        
        if (!project) {
          return res.status(404).json({ error: 'Project not found' });
        }

        res.status(200).json(project);
      } catch (error) {
        console.error('Error fetching project:', error);
        res.status(500).json({ error: 'Failed to fetch project' });
      }
      break;

    default:
      res.setHeader('Allow', ['GET']);
      res.status(405).end(`Method ${req.method} Not Allowed`);
  }
}