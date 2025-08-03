import { PrismaClient } from '@prisma/client';
import { GenerationData } from '@/types';

export class PromptLogger {
  private prisma: PrismaClient;

  constructor(prisma: PrismaClient) {
    this.prisma = prisma;
  }

  async logGeneration(
    projectId: string,
    data: GenerationData
  ) {
    try {
      const generation = await this.prisma.generation.create({
        data: {
          projectId,
          prompt: data.prompt,
          output: data.output,
          model: data.model,
          temperature: data.temperature,
          generationType: data.generationType.toUpperCase() as any,
          metadata: data.metadata || {},
        },
      });

      return generation;
    } catch (error) {
      console.error('Failed to log generation:', error);
      throw new Error('Failed to log generation');
    }
  }

  async getProjectGenerations(projectId: string) {
    try {
      const generations = await this.prisma.generation.findMany({
        where: { projectId },
        orderBy: { createdAt: 'desc' },
      });

      return generations;
    } catch (error) {
      console.error('Failed to fetch generations:', error);
      throw new Error('Failed to fetch generations');
    }
  }

  async getGenerationsByType(projectId: string, type: string) {
    try {
      const generations = await this.prisma.generation.findMany({
        where: {
          projectId,
          generationType: type.toUpperCase() as any,
        },
        orderBy: { createdAt: 'desc' },
      });

      return generations;
    } catch (error) {
      console.error('Failed to fetch generations by type:', error);
      throw new Error('Failed to fetch generations by type');
    }
  }

  async getGenerationStats(projectId: string) {
    try {
      const stats = await this.prisma.generation.groupBy({
        by: ['generationType'],
        where: { projectId },
        _count: {
          generationType: true,
        },
      });

      return stats.map((stat: any) => ({
        type: stat.generationType,
        count: stat._count.generationType,
      }));
    } catch (error) {
      console.error('Failed to fetch generation stats:', error);
      throw new Error('Failed to fetch generation stats');
    }
  }
}