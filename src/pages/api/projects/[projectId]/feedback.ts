import { NextApiRequest, NextApiResponse } from 'next';
import prisma from '@/lib/db/prisma';
import { TrackingSystem } from '@/lib/tracking';
import { FeedbackData } from '@/types';

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
        
        let feedback;
        if (type && typeof type === 'string') {
          feedback = await trackingSystem.feedbackCollector.getFeedbackByType(projectId, type);
        } else {
          feedback = await trackingSystem.feedbackCollector.getProjectFeedback(projectId);
        }
        
        res.status(200).json(feedback);
      } catch (error) {
        console.error('Error fetching feedback:', error);
        res.status(500).json({ error: 'Failed to fetch feedback' });
      }
      break;

    case 'POST':
      try {
        const feedbackData: FeedbackData = req.body;
        
        if (!feedbackData.type || !feedbackData.content) {
          return res.status(400).json({ 
            error: 'Missing required fields: type and content are required' 
          });
        }

        const feedback = await trackingSystem.feedbackCollector.collectFeedback(
          projectId,
          feedbackData
        );
        
        res.status(201).json(feedback);
      } catch (error) {
        console.error('Error collecting feedback:', error);
        res.status(500).json({ error: 'Failed to collect feedback' });
      }
      break;

    default:
      res.setHeader('Allow', ['GET', 'POST']);
      res.status(405).end(`Method ${req.method} Not Allowed`);
  }
}