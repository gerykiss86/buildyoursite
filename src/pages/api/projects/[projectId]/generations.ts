import { NextApiRequest, NextApiResponse } from 'next';
import prisma from '@/lib/db/prisma';
import { TrackingSystem } from '@/lib/tracking';
import { GenerationData } from '@/types';

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  const { projectId } = req.query;
  
  if (!projectId || typeof projectId !== 'string') {
    return res.status(400).json({ error: 'Invalid project ID' });
  }

  const trackingSystem = new TrackingSystem(prisma);

  switch (req.method) {
    case 'GET':
      try {
        const { type } = req.query;
        
        let generations;
        if (type && typeof type === 'string') {
          generations = await trackingSystem.promptLogger.getGenerationsByType(projectId, type);
        } else {
          generations = await trackingSystem.promptLogger.getProjectGenerations(projectId);
        }
        
        res.status(200).json(generations);
      } catch (error) {
        console.error('Error fetching generations:', error);
        res.status(500).json({ error: 'Failed to fetch generations' });
      }
      break;

    case 'POST':
      try {
        const generationData: GenerationData = req.body;
        
        if (!generationData.prompt || !generationData.output || !generationData.generationType) {
          return res.status(400).json({ 
            error: 'Missing required fields: prompt, output, and generationType are required' 
          });
        }

        const generation = await trackingSystem.promptLogger.logGeneration(
          projectId,
          generationData
        );
        
        res.status(201).json(generation);
      } catch (error) {
        console.error('Error logging generation:', error);
        res.status(500).json({ error: 'Failed to log generation' });
      }
      break;

    default:
      res.setHeader('Allow', ['GET', 'POST']);
      res.status(405).end(`Method ${req.method} Not Allowed`);
  }
}