export { PromptLogger } from './PromptLogger';
export { EditTracker } from './EditTracker';
export { FeedbackCollector } from './FeedbackCollector';
export { UsageAnalytics } from './UsageAnalytics';

import { PrismaClient } from '@prisma/client';
import { PromptLogger } from './PromptLogger';
import { EditTracker } from './EditTracker';
import { FeedbackCollector } from './FeedbackCollector';
import { UsageAnalytics } from './UsageAnalytics';

export class TrackingSystem {
  private prisma: PrismaClient;
  public promptLogger: PromptLogger;
  public editTracker: EditTracker;
  public feedbackCollector: FeedbackCollector;
  public usageAnalytics: UsageAnalytics;

  constructor(prisma: PrismaClient) {
    this.prisma = prisma;
    this.promptLogger = new PromptLogger(prisma);
    this.editTracker = new EditTracker(prisma);
    this.feedbackCollector = new FeedbackCollector(prisma);
    this.usageAnalytics = new UsageAnalytics(prisma);
  }

  async createProject(name: string, clientName?: string, description?: string) {
    try {
      const project = await this.prisma.project.create({
        data: {
          name,
          clientName,
          description,
        },
      });
      return project;
    } catch (error) {
      console.error('Error in createProject:', error);
      throw error;
    }
  }

  async getProject(id: string) {
    try {
      const project = await this.prisma.project.findUnique({
        where: { id },
        include: {
          generations: {
            orderBy: { createdAt: 'desc' },
            take: 10,
          },
          edits: {
            orderBy: { createdAt: 'desc' },
            take: 10,
          },
          feedback: {
            orderBy: { createdAt: 'desc' },
            take: 10,
          },
        },
      });
      return project;
    } catch (error) {
      console.error('Error in getProject:', error);
      throw error;
    }
  }

  async getProjects(status?: 'ACTIVE' | 'COMPLETED' | 'ARCHIVED') {
    try {
      const projects = await this.prisma.project.findMany({
        where: status ? { status } : undefined,
        orderBy: { updatedAt: 'desc' },
      });
      return projects;
    } catch (error) {
      console.error('Error in getProjects:', error);
      throw error;
    }
  }
}