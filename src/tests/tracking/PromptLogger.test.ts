import { PrismaClient } from '@prisma/client';
import { PromptLogger } from '@/lib/tracking/PromptLogger';
import { GenerationData } from '@/types';

// Mock PrismaClient
jest.mock('@prisma/client', () => {
  const mockPrismaClient = {
    generation: {
      create: jest.fn(),
      findMany: jest.fn(),
      groupBy: jest.fn(),
    },
  };
  return {
    PrismaClient: jest.fn(() => mockPrismaClient),
  };
});

describe('PromptLogger', () => {
  let prisma: PrismaClient;
  let promptLogger: PromptLogger;

  beforeEach(() => {
    prisma = new PrismaClient();
    promptLogger = new PromptLogger(prisma);
    jest.clearAllMocks();
  });

  describe('logGeneration', () => {
    it('should successfully log a generation', async () => {
      const projectId = 'test-project-id';
      const generationData: GenerationData = {
        prompt: 'Create a landing page',
        output: '<html>...</html>',
        model: 'gpt-4',
        temperature: 0.7,
        generationType: 'full_page',
        metadata: { version: 1 },
      };

      const mockGeneration = {
        id: 'gen-123',
        projectId,
        ...generationData,
        createdAt: new Date(),
      };

      (prisma.generation.create as jest.Mock).mockResolvedValue(mockGeneration);

      const result = await promptLogger.logGeneration(projectId, generationData);

      expect(prisma.generation.create).toHaveBeenCalledWith({
        data: {
          projectId,
          prompt: generationData.prompt,
          output: generationData.output,
          model: generationData.model,
          temperature: generationData.temperature,
          generationType: 'FULL_PAGE',
          metadata: generationData.metadata,
        },
      });

      expect(result).toEqual(mockGeneration);
    });

    it('should handle errors when logging generation', async () => {
      const projectId = 'test-project-id';
      const generationData: GenerationData = {
        prompt: 'Create a landing page',
        output: '<html>...</html>',
        model: 'gpt-4',
        generationType: 'full_page',
      };

      (prisma.generation.create as jest.Mock).mockRejectedValue(new Error('Database error'));

      await expect(promptLogger.logGeneration(projectId, generationData)).rejects.toThrow('Failed to log generation');
    });
  });

  describe('getProjectGenerations', () => {
    it('should fetch all generations for a project', async () => {
      const projectId = 'test-project-id';
      const mockGenerations = [
        { id: 'gen-1', projectId, prompt: 'Test 1', createdAt: new Date() },
        { id: 'gen-2', projectId, prompt: 'Test 2', createdAt: new Date() },
      ];

      (prisma.generation.findMany as jest.Mock).mockResolvedValue(mockGenerations);

      const result = await promptLogger.getProjectGenerations(projectId);

      expect(prisma.generation.findMany).toHaveBeenCalledWith({
        where: { projectId },
        orderBy: { createdAt: 'desc' },
      });

      expect(result).toEqual(mockGenerations);
    });
  });

  describe('getGenerationsByType', () => {
    it('should fetch generations by type', async () => {
      const projectId = 'test-project-id';
      const type = 'layout';
      const mockGenerations = [
        { id: 'gen-1', projectId, generationType: 'LAYOUT', createdAt: new Date() },
      ];

      (prisma.generation.findMany as jest.Mock).mockResolvedValue(mockGenerations);

      const result = await promptLogger.getGenerationsByType(projectId, type);

      expect(prisma.generation.findMany).toHaveBeenCalledWith({
        where: {
          projectId,
          generationType: 'LAYOUT',
        },
        orderBy: { createdAt: 'desc' },
      });

      expect(result).toEqual(mockGenerations);
    });
  });

  describe('getGenerationStats', () => {
    it('should return generation statistics grouped by type', async () => {
      const projectId = 'test-project-id';
      const mockStats = [
        { generationType: 'LAYOUT', _count: { generationType: 5 } },
        { generationType: 'CONTENT', _count: { generationType: 3 } },
      ];

      (prisma.generation.groupBy as jest.Mock).mockResolvedValue(mockStats);

      const result = await promptLogger.getGenerationStats(projectId);

      expect(prisma.generation.groupBy).toHaveBeenCalledWith({
        by: ['generationType'],
        where: { projectId },
        _count: {
          generationType: true,
        },
      });

      expect(result).toEqual([
        { type: 'LAYOUT', count: 5 },
        { type: 'CONTENT', count: 3 },
      ]);
    });
  });
});