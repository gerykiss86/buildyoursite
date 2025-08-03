import { PrismaClient } from '@prisma/client';
import { FeedbackData } from '@/types';

export class FeedbackCollector {
  private prisma: PrismaClient;

  constructor(prisma: PrismaClient) {
    this.prisma = prisma;
  }

  async collectFeedback(
    projectId: string,
    data: FeedbackData
  ) {
    try {
      const feedback = await this.prisma.feedback.create({
        data: {
          projectId,
          type: data.type.toUpperCase() as any,
          content: data.content,
          rating: data.rating,
          clientName: data.clientName,
        },
      });

      return feedback;
    } catch (error) {
      console.error('Failed to collect feedback:', error);
      throw new Error('Failed to collect feedback');
    }
  }

  async getProjectFeedback(projectId: string) {
    try {
      const feedback = await this.prisma.feedback.findMany({
        where: { projectId },
        orderBy: { createdAt: 'desc' },
      });

      return feedback;
    } catch (error) {
      console.error('Failed to fetch feedback:', error);
      throw new Error('Failed to fetch feedback');
    }
  }

  async getFeedbackByType(projectId: string, type: string) {
    try {
      const feedback = await this.prisma.feedback.findMany({
        where: {
          projectId,
          type: type.toUpperCase() as any,
        },
        orderBy: { createdAt: 'desc' },
      });

      return feedback;
    } catch (error) {
      console.error('Failed to fetch feedback by type:', error);
      throw new Error('Failed to fetch feedback by type');
    }
  }

  async getAverageRating(projectId: string) {
    try {
      const result = await this.prisma.feedback.aggregate({
        where: {
          projectId,
          rating: { not: null },
        },
        _avg: {
          rating: true,
        },
      });

      return result._avg.rating || 0;
    } catch (error) {
      console.error('Failed to calculate average rating:', error);
      throw new Error('Failed to calculate average rating');
    }
  }

  async getFeedbackStats(projectId: string) {
    try {
      const [typeStats, ratingStats] = await Promise.all([
        this.prisma.feedback.groupBy({
          by: ['type'],
          where: { projectId },
          _count: {
            type: true,
          },
        }),
        this.prisma.feedback.groupBy({
          by: ['rating'],
          where: {
            projectId,
            rating: { not: null },
          },
          _count: {
            rating: true,
          },
        }),
      ]);

      return {
        byType: typeStats.map((stat: any) => ({
          type: stat.type,
          count: stat._count.type,
        })),
        byRating: ratingStats.map((stat: any) => ({
          rating: stat.rating,
          count: stat._count.rating,
        })),
      };
    } catch (error) {
      console.error('Failed to fetch feedback stats:', error);
      throw new Error('Failed to fetch feedback stats');
    }
  }

  async getRecurringPatterns(projectId?: string) {
    try {
      const whereClause = projectId ? { projectId } : {};
      
      const feedback = await this.prisma.feedback.findMany({
        where: whereClause,
        select: {
          content: true,
          type: true,
        },
      });

      // Simple pattern detection - in production, use NLP
      const patterns = new Map<string, number>();
      const keywords = ['slow', 'fast', 'beautiful', 'ugly', 'confusing', 'clear', 'broken', 'works'];
      
      feedback.forEach((item: any) => {
        const lowerContent = item.content.toLowerCase();
        keywords.forEach(keyword => {
          if (lowerContent.includes(keyword)) {
            const key = `${item.type}-${keyword}`;
            patterns.set(key, (patterns.get(key) || 0) + 1);
          }
        });
      });

      return Array.from(patterns.entries())
        .map(([pattern, count]) => ({ pattern, count }))
        .sort((a, b) => b.count - a.count)
        .slice(0, 10);
    } catch (error) {
      console.error('Failed to find recurring patterns:', error);
      throw new Error('Failed to find recurring patterns');
    }
  }
}