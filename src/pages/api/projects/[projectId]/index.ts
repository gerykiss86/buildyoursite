import { NextApiRequest, NextApiResponse } from 'next';
import prisma from '@/lib/db/prisma';

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
        const project = await prisma.project.findUnique({
          where: { id: projectId },
          include: {
            _count: {
              select: {
                generations: true,
                edits: true,
                feedback: true,
              },
            },
          },
        });

        if (!project) {
          return res.status(404).json({ error: 'Project not found' });
        }

        res.status(200).json(project);
      } catch (error) {
        console.error('Error fetching project:', error);
        res.status(500).json({ error: 'Failed to fetch project' });
      }
      break;

    case 'PUT':
      try {
        const { name, clientName, description, status } = req.body;
        
        const project = await prisma.project.update({
          where: { id: projectId },
          data: {
            name,
            clientName,
            description,
            status,
          },
        });

        res.status(200).json(project);
      } catch (error) {
        console.error('Error updating project:', error);
        res.status(500).json({ error: 'Failed to update project' });
      }
      break;

    default:
      res.setHeader('Allow', ['GET', 'PUT']);
      res.status(405).end(`Method ${req.method} Not Allowed`);
  }
}