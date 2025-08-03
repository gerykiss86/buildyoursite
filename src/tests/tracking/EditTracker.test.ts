import { PrismaClient } from '@prisma/client';
import { EditTracker } from '@/lib/tracking/EditTracker';
import { EditData } from '@/types';

// Mock PrismaClient
jest.mock('@prisma/client', () => {
  const mockPrismaClient = {
    edit: {
      create: jest.fn(),
      findMany: jest.fn(),
      groupBy: jest.fn(),
      count: jest.fn(),
    },
    generation: {
      count: jest.fn(),
    },
  };
  return {
    PrismaClient: jest.fn(() => mockPrismaClient),
  };
});

describe('EditTracker', () => {
  let prisma: PrismaClient;
  let editTracker: EditTracker;

  beforeEach(() => {
    prisma = new PrismaClient();
    editTracker = new EditTracker(prisma);
    jest.clearAllMocks();
  });

  describe('trackEdit', () => {
    it('should successfully track an edit', async () => {
      const projectId = 'test-project-id';
      const editData: EditData = {
        generationId: 'gen-123',
        originalContent: 'Original content',
        editedContent: 'Edited content',
        editType: 'content_change',
        reason: 'Improved clarity',
      };

      const mockEdit = {
        id: 'edit-123',
        projectId,
        ...editData,
        createdAt: new Date(),
      };

      (prisma.edit.create as jest.Mock).mockResolvedValue(mockEdit);

      const result = await editTracker.trackEdit(projectId, editData);

      expect(prisma.edit.create).toHaveBeenCalledWith({
        data: {
          projectId,
          generationId: editData.generationId,
          originalContent: editData.originalContent,
          editedContent: editData.editedContent,
          editType: 'CONTENT_CHANGE',
          reason: editData.reason,
        },
      });

      expect(result).toEqual(mockEdit);
    });

    it('should handle errors when tracking edit', async () => {
      const projectId = 'test-project-id';
      const editData: EditData = {
        originalContent: 'Original',
        editedContent: 'Edited',
        editType: 'bug_fix',
      };

      (prisma.edit.create as jest.Mock).mockRejectedValue(new Error('Database error'));

      await expect(editTracker.trackEdit(projectId, editData)).rejects.toThrow('Failed to track edit');
    });
  });

  describe('getProjectEdits', () => {
    it('should fetch all edits for a project', async () => {
      const projectId = 'test-project-id';
      const mockEdits = [
        { id: 'edit-1', projectId, editType: 'CONTENT_CHANGE', generation: null },
        { id: 'edit-2', projectId, editType: 'BUG_FIX', generation: { id: 'gen-1' } },
      ];

      (prisma.edit.findMany as jest.Mock).mockResolvedValue(mockEdits);

      const result = await editTracker.getProjectEdits(projectId);

      expect(prisma.edit.findMany).toHaveBeenCalledWith({
        where: { projectId },
        include: {
          generation: true,
        },
        orderBy: { createdAt: 'desc' },
      });

      expect(result).toEqual(mockEdits);
    });
  });

  describe('calculateEditRatio', () => {
    it('should calculate the edit ratio correctly', async () => {
      const projectId = 'test-project-id';

      (prisma.generation.count as jest.Mock).mockResolvedValue(10);
      (prisma.edit.count as jest.Mock).mockResolvedValue(3);

      const result = await editTracker.calculateEditRatio(projectId);

      expect(result).toBe(0.3); // 3 edits / 10 generations
    });

    it('should return 0 when there are no generations', async () => {
      const projectId = 'test-project-id';

      (prisma.generation.count as jest.Mock).mockResolvedValue(0);
      (prisma.edit.count as jest.Mock).mockResolvedValue(5);

      const result = await editTracker.calculateEditRatio(projectId);

      expect(result).toBe(0);
    });
  });

  describe('getEditStats', () => {
    it('should return edit statistics grouped by type', async () => {
      const projectId = 'test-project-id';
      const mockStats = [
        { editType: 'CONTENT_CHANGE', _count: { editType: 8 } },
        { editType: 'BUG_FIX', _count: { editType: 5 } },
        { editType: 'STYLE_MODIFICATION', _count: { editType: 3 } },
      ];

      (prisma.edit.groupBy as jest.Mock).mockResolvedValue(mockStats);

      const result = await editTracker.getEditStats(projectId);

      expect(prisma.edit.groupBy).toHaveBeenCalledWith({
        by: ['editType'],
        where: { projectId },
        _count: {
          editType: true,
        },
      });

      expect(result).toEqual([
        { type: 'CONTENT_CHANGE', count: 8 },
        { type: 'BUG_FIX', count: 5 },
        { type: 'STYLE_MODIFICATION', count: 3 },
      ]);
    });
  });
});