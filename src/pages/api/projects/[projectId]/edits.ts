import { NextApiRequest, NextApiResponse } from 'next';
import prisma from '@/lib/db/prisma';
import { TrackingSystem } from '@/lib/tracking';
import { EditData } from '@/types';

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
        
        let edits;
        if (type && typeof type === 'string') {
          edits = await trackingSystem.editTracker.getEditsByType(projectId, type);
        } else {
          edits = await trackingSystem.editTracker.getProjectEdits(projectId);
        }
        
        res.status(200).json(edits);
      } catch (error) {
        console.error('Error fetching edits:', error);
        res.status(500).json({ error: 'Failed to fetch edits' });
      }
      break;

    case 'POST':
      try {
        const editData: EditData = req.body;
        
        if (!editData.originalContent || !editData.editedContent || !editData.editType) {
          return res.status(400).json({ 
            error: 'Missing required fields: originalContent, editedContent, and editType are required' 
          });
        }

        const edit = await trackingSystem.editTracker.trackEdit(projectId, editData);
        res.status(201).json(edit);
      } catch (error) {
        console.error('Error tracking edit:', error);
        res.status(500).json({ error: 'Failed to track edit' });
      }
      break;

    default:
      res.setHeader('Allow', ['GET', 'POST']);
      res.status(405).end(`Method ${req.method} Not Allowed`);
  }
}