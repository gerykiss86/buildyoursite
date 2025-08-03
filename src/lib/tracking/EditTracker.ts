import { PrismaClient } from '@prisma/client';
import { EditData } from '@/types';

export class EditTracker {
  private prisma: PrismaClient;

  constructor(prisma: PrismaClient) {
    this.prisma = prisma;
  }

  async trackEdit(
    projectId: string,
    data: EditData
  ) {
    try {
      const edit = await this.prisma.edit.create({
        data: {
          projectId,
          generationId: data.generationId,
          originalContent: data.originalContent,
          editedContent: data.editedContent,
          editType: data.editType.toUpperCase() as any,
          reason: data.reason,
        },
      });

      return edit;
    } catch (error) {
      console.error('Failed to track edit:', error);
      throw new Error('Failed to track edit');
    }
  }

  async getProjectEdits(projectId: string) {
    try {
      const edits = await this.prisma.edit.findMany({
        where: { projectId },
        include: {
          generation: true,
        },
        orderBy: { createdAt: 'desc' },
      });

      return edits;
    } catch (error) {
      console.error('Failed to fetch edits:', error);
      throw new Error('Failed to fetch edits');
    }
  }

  async getEditsByType(projectId: string, type: string) {
    try {
      const edits = await this.prisma.edit.findMany({
        where: {
          projectId,
          editType: type.toUpperCase() as any,
        },
        orderBy: { createdAt: 'desc' },
      });

      return edits;
    } catch (error) {
      console.error('Failed to fetch edits by type:', error);
      throw new Error('Failed to fetch edits by type');
    }
  }

  async getEditStats(projectId: string) {
    try {
      const stats = await this.prisma.edit.groupBy({
        by: ['editType'],
        where: { projectId },
        _count: {
          editType: true,
        },
      });

      return stats.map((stat: any) => ({
        type: stat.editType,
        count: stat._count.editType,
      }));
    } catch (error) {
      console.error('Failed to fetch edit stats:', error);
      throw new Error('Failed to fetch edit stats');
    }
  }

  async calculateEditRatio(projectId: string) {
    try {
      const [totalGenerations, totalEdits] = await Promise.all([
        this.prisma.generation.count({
          where: { projectId },
        }),
        this.prisma.edit.count({
          where: { projectId },
        }),
      ]);

      if (totalGenerations === 0) {
        return 0;
      }

      return totalEdits / totalGenerations;
    } catch (error) {
      console.error('Failed to calculate edit ratio:', error);
      throw new Error('Failed to calculate edit ratio');
    }
  }
}