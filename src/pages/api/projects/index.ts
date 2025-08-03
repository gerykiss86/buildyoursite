import { NextApiRequest, NextApiResponse } from 'next';
import prisma from '@/lib/db/prisma';
import { TrackingSystem } from '@/lib/tracking';

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  const trackingSystem = new TrackingSystem(prisma);

  switch (req.method) {
    case 'GET':
      try {
        const { status } = req.query;
        const projects = await trackingSystem.getProjects(
          status as 'ACTIVE' | 'COMPLETED' | 'ARCHIVED' | undefined
        );
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

        console.log('Creating project with data:', { name, clientName, description });
        
        const project = await trackingSystem.createProject(name, clientName, description);
        console.log('Project created successfully:', project);
        
        res.status(201).json(project);
      } catch (error) {
        console.error('Detailed error creating project:', error);
        res.status(500).json({ 
          error: 'Failed to create project',
          details: error instanceof Error ? error.message : 'Unknown error',
        });
      }
      break;

    default:
      res.setHeader('Allow', ['GET', 'POST']);
      res.status(405).end(`Method ${req.method} Not Allowed`);
  }
}