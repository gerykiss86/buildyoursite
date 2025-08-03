import { PrismaClient } from '@prisma/client';
import { startOfDay } from 'date-fns';

export class UsageAnalytics {
  private prisma: PrismaClient;

  constructor(prisma: PrismaClient) {
    this.prisma = prisma;
  }

  async calculateDailyMetrics(date: Date = new Date()) {
    try {
      const dayStart = startOfDay(date);
      
      // Get all projects
      const projects = await this.prisma.project.findMany({
        where: {
          createdAt: {
            lte: dayStart,
          },
        },
        include: {
          generations: true,
          edits: true,
          feedback: {
            where: {
              rating: { not: null },
            },
          },
        },
      });

      // Calculate metrics
      const totalProjects = projects.length;
      let totalGenerations = 0;
      let totalEdits = 0;
      let totalFeedback = 0;
      let totalRating = 0;
      let ratingCount = 0;

      projects.forEach((project: any) => {
        totalGenerations += project.generations.length;
        totalEdits += project.edits.length;
        totalFeedback += project.feedback.length;
        
        project.feedback.forEach((fb: any) => {
          if (fb.rating) {
            totalRating += fb.rating;
            ratingCount++;
          }
        });
      });

      const aiGeneratedRatio = totalGenerations > 0 
        ? totalGenerations / (totalGenerations + totalEdits) 
        : 0;
      
      const manualEditRatio = 1 - aiGeneratedRatio;
      const averageRating = ratingCount > 0 ? totalRating / ratingCount : null;

      // Store or update metrics
      const metrics = await this.prisma.usageMetric.upsert({
        where: { date: dayStart },
        update: {
          totalProjects,
          aiGeneratedRatio,
          manualEditRatio,
          generationCount: totalGenerations,
          editCount: totalEdits,
          feedbackCount: totalFeedback,
          averageRating,
        },
        create: {
          date: dayStart,
          totalProjects,
          aiGeneratedRatio,
          manualEditRatio,
          generationCount: totalGenerations,
          editCount: totalEdits,
          feedbackCount: totalFeedback,
          averageRating,
        },
      });

      return metrics;
    } catch (error) {
      console.error('Failed to calculate daily metrics:', error);
      throw new Error('Failed to calculate daily metrics');
    }
  }

  async getProjectUsageStats(projectId: string) {
    try {
      const [generations, edits, feedback] = await Promise.all([
        this.prisma.generation.count({
          where: { projectId },
        }),
        this.prisma.edit.count({
          where: { projectId },
        }),
        this.prisma.feedback.aggregate({
          where: {
            projectId,
            rating: { not: null },
          },
          _avg: {
            rating: true,
          },
          _count: {
            rating: true,
          },
        }),
      ]);

      const totalOperations = generations + edits;
      const aiGeneratedPercentage = totalOperations > 0 
        ? (generations / totalOperations) * 100 
        : 0;

      return {
        generationCount: generations,
        editCount: edits,
        aiGeneratedPercentage: Math.round(aiGeneratedPercentage),
        manualEditPercentage: Math.round(100 - aiGeneratedPercentage),
        averageRating: feedback._avg.rating || 0,
        ratingCount: feedback._count.rating,
      };
    } catch (error) {
      console.error('Failed to get project usage stats:', error);
      throw new Error('Failed to get project usage stats');
    }
  }

  async getHistoricalMetrics(days: number = 30) {
    try {
      const endDate = new Date();
      const startDate = new Date();
      startDate.setDate(startDate.getDate() - days);

      const metrics = await this.prisma.usageMetric.findMany({
        where: {
          date: {
            gte: startDate,
            lte: endDate,
          },
        },
        orderBy: { date: 'asc' },
      });

      return metrics;
    } catch (error) {
      console.error('Failed to fetch historical metrics:', error);
      throw new Error('Failed to fetch historical metrics');
    }
  }

  async getMostEditedGenerationTypes() {
    try {
      const result = await this.prisma.$queryRaw`
        SELECT g."generationType", COUNT(e.id) as edit_count
        FROM "Generation" g
        LEFT JOIN "Edit" e ON g.id = e."generationId"
        WHERE e.id IS NOT NULL
        GROUP BY g."generationType"
        ORDER BY edit_count DESC
        LIMIT 5
      `;

      return result;
    } catch (error) {
      console.error('Failed to get most edited generation types:', error);
      throw new Error('Failed to get most edited generation types');
    }
  }
}