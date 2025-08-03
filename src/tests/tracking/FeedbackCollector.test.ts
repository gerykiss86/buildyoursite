import { PrismaClient } from '@prisma/client';
import { FeedbackCollector } from '@/lib/tracking/FeedbackCollector';
import { FeedbackData } from '@/types';

// Mock PrismaClient
jest.mock('@prisma/client', () => {
  const mockPrismaClient = {
    feedback: {
      create: jest.fn(),
      findMany: jest.fn(),
      groupBy: jest.fn(),
      aggregate: jest.fn(),
    },
  };
  return {
    PrismaClient: jest.fn(() => mockPrismaClient),
  };
});

describe('FeedbackCollector', () => {
  let prisma: PrismaClient;
  let feedbackCollector: FeedbackCollector;

  beforeEach(() => {
    prisma = new PrismaClient();
    feedbackCollector = new FeedbackCollector(prisma);
    jest.clearAllMocks();
  });

  describe('collectFeedback', () => {
    it('should successfully collect feedback', async () => {
      const projectId = 'test-project-id';
      const feedbackData: FeedbackData = {
        type: 'design',
        content: 'The layout looks great!',
        rating: 5,
        clientName: 'John Doe',
      };

      const mockFeedback = {
        id: 'feedback-123',
        projectId,
        ...feedbackData,
        type: 'DESIGN',
        createdAt: new Date(),
      };

      (prisma.feedback.create as jest.Mock).mockResolvedValue(mockFeedback);

      const result = await feedbackCollector.collectFeedback(projectId, feedbackData);

      expect(prisma.feedback.create).toHaveBeenCalledWith({
        data: {
          projectId,
          type: 'DESIGN',
          content: feedbackData.content,
          rating: feedbackData.rating,
          clientName: feedbackData.clientName,
        },
      });

      expect(result).toEqual(mockFeedback);
    });
  });

  describe('getAverageRating', () => {
    it('should calculate average rating correctly', async () => {
      const projectId = 'test-project-id';

      (prisma.feedback.aggregate as jest.Mock).mockResolvedValue({
        _avg: { rating: 4.5 },
      });

      const result = await feedbackCollector.getAverageRating(projectId);

      expect(prisma.feedback.aggregate).toHaveBeenCalledWith({
        where: {
          projectId,
          rating: { not: null },
        },
        _avg: {
          rating: true,
        },
      });

      expect(result).toBe(4.5);
    });

    it('should return 0 when no ratings exist', async () => {
      const projectId = 'test-project-id';

      (prisma.feedback.aggregate as jest.Mock).mockResolvedValue({
        _avg: { rating: null },
      });

      const result = await feedbackCollector.getAverageRating(projectId);

      expect(result).toBe(0);
    });
  });

  describe('getFeedbackStats', () => {
    it('should return feedback statistics by type and rating', async () => {
      const projectId = 'test-project-id';

      const mockTypeStats = [
        { type: 'DESIGN', _count: { type: 5 } },
        { type: 'FUNCTIONALITY', _count: { type: 3 } },
      ];

      const mockRatingStats = [
        { rating: 5, _count: { rating: 4 } },
        { rating: 4, _count: { rating: 2 } },
        { rating: 3, _count: { rating: 1 } },
      ];

      (prisma.feedback.groupBy as jest.Mock)
        .mockResolvedValueOnce(mockTypeStats)
        .mockResolvedValueOnce(mockRatingStats);

      const result = await feedbackCollector.getFeedbackStats(projectId);

      expect(result).toEqual({
        byType: [
          { type: 'DESIGN', count: 5 },
          { type: 'FUNCTIONALITY', count: 3 },
        ],
        byRating: [
          { rating: 5, count: 4 },
          { rating: 4, count: 2 },
          { rating: 3, count: 1 },
        ],
      });
    });
  });

  describe('getRecurringPatterns', () => {
    it('should identify recurring patterns in feedback', async () => {
      const mockFeedback = [
        { content: 'The site is too slow', type: 'PERFORMANCE' },
        { content: 'Loading is slow', type: 'PERFORMANCE' },
        { content: 'Beautiful design', type: 'DESIGN' },
        { content: 'Very beautiful layout', type: 'DESIGN' },
        { content: 'Site works perfectly', type: 'FUNCTIONALITY' },
      ];

      (prisma.feedback.findMany as jest.Mock).mockResolvedValue(mockFeedback);

      const result = await feedbackCollector.getRecurringPatterns();

      // Should find patterns like 'PERFORMANCE-slow' appearing twice
      expect(result).toContainEqual({ pattern: 'PERFORMANCE-slow', count: 2 });
      expect(result).toContainEqual({ pattern: 'DESIGN-beautiful', count: 2 });
      expect(result).toContainEqual({ pattern: 'FUNCTIONALITY-works', count: 1 });
    });
  });
});