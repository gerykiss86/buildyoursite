import { PrismaClient } from '@prisma/client';
import { UsageAnalytics } from '@/lib/tracking/UsageAnalytics';
import { startOfDay } from 'date-fns';

// Mock PrismaClient
jest.mock('@prisma/client', () => {
  const mockPrismaClient = {
    project: {
      findMany: jest.fn(),
    },
    generation: {
      count: jest.fn(),
    },
    edit: {
      count: jest.fn(),
    },
    feedback: {
      aggregate: jest.fn(),
    },
    usageMetric: {
      upsert: jest.fn(),
      findMany: jest.fn(),
    },
    $queryRaw: jest.fn(),
  };
  return {
    PrismaClient: jest.fn(() => mockPrismaClient),
  };
});

describe('UsageAnalytics', () => {
  let prisma: PrismaClient;
  let usageAnalytics: UsageAnalytics;

  beforeEach(() => {
    prisma = new PrismaClient();
    usageAnalytics = new UsageAnalytics(prisma);
    jest.clearAllMocks();
  });

  describe('calculateDailyMetrics', () => {
    it('should calculate and store daily metrics', async () => {
      const testDate = new Date('2024-01-15');
      const dayStart = startOfDay(testDate);

      const mockProjects = [
        {
          id: 'project-1',
          generations: [{ id: 'gen-1' }, { id: 'gen-2' }],
          edits: [{ id: 'edit-1' }],
          feedback: [{ rating: 5 }, { rating: 4 }],
        },
        {
          id: 'project-2',
          generations: [{ id: 'gen-3' }],
          edits: [{ id: 'edit-2' }, { id: 'edit-3' }],
          feedback: [{ rating: 3 }],
        },
      ];

      (prisma.project.findMany as jest.Mock).mockResolvedValue(mockProjects);

      const expectedMetrics = {
        date: dayStart,
        totalProjects: 2,
        aiGeneratedRatio: 0.5, // 3 generations / (3 generations + 3 edits)
        manualEditRatio: 0.5,
        generationCount: 3,
        editCount: 3,
        feedbackCount: 3,
        averageRating: 4, // (5 + 4 + 3) / 3
      };

      (prisma.usageMetric.upsert as jest.Mock).mockResolvedValue(expectedMetrics);

      const result = await usageAnalytics.calculateDailyMetrics(testDate);

      expect(prisma.usageMetric.upsert).toHaveBeenCalledWith({
        where: { date: dayStart },
        update: expect.objectContaining({
          totalProjects: 2,
          aiGeneratedRatio: 0.5,
          manualEditRatio: 0.5,
          generationCount: 3,
          editCount: 3,
          feedbackCount: 3,
          averageRating: 4,
        }),
        create: expect.objectContaining({
          date: dayStart,
          totalProjects: 2,
          aiGeneratedRatio: 0.5,
          manualEditRatio: 0.5,
          generationCount: 3,
          editCount: 3,
          feedbackCount: 3,
          averageRating: 4,
        }),
      });

      expect(result).toEqual(expectedMetrics);
    });
  });

  describe('getProjectUsageStats', () => {
    it('should calculate project usage statistics', async () => {
      const projectId = 'test-project-id';

      (prisma.generation.count as jest.Mock).mockResolvedValue(8);
      (prisma.edit.count as jest.Mock).mockResolvedValue(2);
      (prisma.feedback.aggregate as jest.Mock).mockResolvedValue({
        _avg: { rating: 4.5 },
        _count: { rating: 4 },
      });

      const result = await usageAnalytics.getProjectUsageStats(projectId);

      expect(result).toEqual({
        generationCount: 8,
        editCount: 2,
        aiGeneratedPercentage: 80, // 8 / (8 + 2) * 100
        manualEditPercentage: 20,
        averageRating: 4.5,
        ratingCount: 4,
      });
    });

    it('should handle projects with no operations', async () => {
      const projectId = 'test-project-id';

      (prisma.generation.count as jest.Mock).mockResolvedValue(0);
      (prisma.edit.count as jest.Mock).mockResolvedValue(0);
      (prisma.feedback.aggregate as jest.Mock).mockResolvedValue({
        _avg: { rating: null },
        _count: { rating: 0 },
      });

      const result = await usageAnalytics.getProjectUsageStats(projectId);

      expect(result).toEqual({
        generationCount: 0,
        editCount: 0,
        aiGeneratedPercentage: 0,
        manualEditPercentage: 100,
        averageRating: 0,
        ratingCount: 0,
      });
    });
  });

  describe('getHistoricalMetrics', () => {
    it('should fetch historical metrics for specified days', async () => {
      const mockMetrics = [
        { date: new Date('2024-01-10'), totalProjects: 5 },
        { date: new Date('2024-01-11'), totalProjects: 6 },
        { date: new Date('2024-01-12'), totalProjects: 7 },
      ];

      (prisma.usageMetric.findMany as jest.Mock).mockResolvedValue(mockMetrics);

      const result = await usageAnalytics.getHistoricalMetrics(30);

      expect(prisma.usageMetric.findMany).toHaveBeenCalledWith({
        where: {
          date: {
            gte: expect.any(Date),
            lte: expect.any(Date),
          },
        },
        orderBy: { date: 'asc' },
      });

      expect(result).toEqual(mockMetrics);
    });
  });

  describe('getMostEditedGenerationTypes', () => {
    it('should return the most edited generation types', async () => {
      const mockResult = [
        { generationType: 'CONTENT', edit_count: BigInt(15) },
        { generationType: 'LAYOUT', edit_count: BigInt(10) },
        { generationType: 'STYLE', edit_count: BigInt(5) },
      ];

      (prisma.$queryRaw as jest.Mock).mockResolvedValue(mockResult);

      const result = await usageAnalytics.getMostEditedGenerationTypes();

      expect(result).toEqual(mockResult);
    });
  });
});