import { NextApiRequest, NextApiResponse } from 'next';
import { BoltIntegration } from '@/lib/ai/BoltIntegration';
import { memoryStore } from '@/lib/db/memory-store';

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  if (req.method !== 'POST') {
    res.setHeader('Allow', ['POST']);
    return res.status(405).end(`Method ${req.method} Not Allowed`);
  }

  try {
    const { projectId, prompt, type = 'full_page' } = req.body;

    if (!projectId || !prompt) {
      return res.status(400).json({ 
        error: 'Missing required fields: projectId and prompt are required' 
      });
    }

    // Generate content using Bolt integration
    const bolt = new BoltIntegration();
    const generationData = await bolt.generateWebsite(prompt, type);
    
    // Store the generation in memory
    const generation = memoryStore.createGeneration({
      projectId,
      ...generationData,
    });

    res.status(200).json({
      generation,
      content: generationData.output,
    });
  } catch (error) {
    console.error('Error in generate API:', error);
    res.status(500).json({ 
      error: 'Failed to generate content',
      message: error instanceof Error ? error.message : 'Unknown error',
    });
  }
}