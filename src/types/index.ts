export interface TrackingEvent {
  id: string;
  timestamp: Date;
  type: 'generation' | 'edit' | 'feedback';
  projectId: string;
  data: GenerationData | EditData | FeedbackData;
}

export interface GenerationData {
  prompt: string;
  output: string;
  model: string;
  temperature?: number;
  generationType: 'layout' | 'content' | 'component' | 'style' | 'full_page' | 'other';
  metadata?: Record<string, any>;
}

export interface EditData {
  generationId?: string;
  originalContent: string;
  editedContent: string;
  editType: 'content_change' | 'layout_adjustment' | 'style_modification' | 'bug_fix' | 'feature_addition' | 'optimization' | 'other';
  reason?: string;
}

export interface FeedbackData {
  type: 'general' | 'design' | 'content' | 'functionality' | 'performance' | 'suggestion';
  content: string;
  rating?: number;
  clientName?: string;
}

export interface ProjectData {
  id: string;
  name: string;
  clientName?: string;
  description?: string;
  status: 'active' | 'completed' | 'archived';
  createdAt: Date;
  updatedAt: Date;
}

export interface UsageMetrics {
  date: Date;
  totalProjects: number;
  aiGeneratedRatio: number;
  manualEditRatio: number;
  generationCount: number;
  editCount: number;
  feedbackCount: number;
  averageRating?: number;
}