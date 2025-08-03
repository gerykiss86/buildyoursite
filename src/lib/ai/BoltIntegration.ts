import { GenerationData } from '@/types';
import OpenAI from 'openai';

interface BoltGenerationRequest {
  prompt: string;
  model?: string;
  temperature?: number;
  max_tokens?: number;
  systemPrompt?: string;
}

interface BoltGenerationResponse {
  content: string;
  model: string;
  usage?: {
    prompt_tokens: number;
    completion_tokens: number;
    total_tokens: number;
  };
}

export class BoltIntegration {
  private openai: OpenAI;

  constructor(apiKey?: string) {
    const key = apiKey || process.env.OPENAI_API_KEY || '';
    if (!key) {
      throw new Error('OpenAI API key is required');
    }
    
    this.openai = new OpenAI({
      apiKey: key,
    });
  }

  async generateWebsite(prompt: string, type: 'full_page' | 'component' | 'layout' | 'content' = 'full_page'): Promise<GenerationData> {
    const systemPrompt = this.getSystemPrompt(type);
    
    try {
      const response = await this.callOpenAI({
        prompt,
        systemPrompt,
        model: 'gpt-4',
        temperature: 0.7,
        max_tokens: 4000,
      });

      return {
        prompt,
        output: response.content,
        model: response.model,
        temperature: 0.7,
        generationType: type,
        metadata: {
          usage: response.usage,
          timestamp: new Date().toISOString(),
        },
      };
    } catch (error) {
      console.error('Failed to generate website - Full error:', error);
      if (error instanceof Error) {
        throw new Error(`Generation failed: ${error.message}`);
      }
      throw new Error('Failed to generate website content');
    }
  }

  private async callOpenAI(request: BoltGenerationRequest): Promise<BoltGenerationResponse> {
    try {
      const completion = await this.openai.chat.completions.create({
        model: request.model || 'gpt-4',
        messages: [
          {
            role: 'system',
            content: request.systemPrompt || this.getSystemPrompt('full_page'),
          },
          {
            role: 'user',
            content: request.prompt,
          },
        ],
        temperature: request.temperature || 0.7,
        max_tokens: request.max_tokens || 4000,
      });

      return {
        content: completion.choices[0].message.content || '',
        model: completion.model,
        usage: completion.usage ? {
          prompt_tokens: completion.usage.prompt_tokens,
          completion_tokens: completion.usage.completion_tokens,
          total_tokens: completion.usage.total_tokens,
        } : undefined,
      };
    } catch (error) {
      console.error('OpenAI API error:', error);
      throw new Error('Failed to call OpenAI API');
    }
  }

  private getSystemPrompt(type: string): string {
    const prompts = {
      full_page: `You are an expert web developer. Generate a complete, modern, responsive HTML page with inline CSS and JavaScript. 
The output should be production-ready code that works immediately when saved as an HTML file.
Include modern design patterns, accessibility features, and responsive layouts.
Use semantic HTML5 elements and follow best practices.`,

      component: `You are an expert web developer. Generate a reusable HTML component with inline styles.
The component should be self-contained and easy to integrate into existing pages.
Include any necessary JavaScript for interactivity.`,

      layout: `You are an expert web developer. Generate a responsive layout structure using modern CSS.
Focus on the layout grid, spacing, and responsive behavior.
Use CSS Grid or Flexbox as appropriate.`,

      content: `You are an expert content writer and web developer. Generate well-structured content in HTML format.
Focus on semantic markup, readability, and SEO best practices.
Include appropriate headings, paragraphs, and other content elements.`,
    };

    return prompts[type as keyof typeof prompts] || prompts.full_page;
  }

  async improveContent(originalContent: string, feedback: string): Promise<GenerationData> {
    const prompt = `Improve the following HTML content based on this feedback: "${feedback}"

Original content:
${originalContent}

Generate the improved version maintaining the same structure but addressing the feedback.`;

    return this.generateWebsite(prompt, 'content');
  }

  async regenerateSection(fullContent: string, sectionIdentifier: string, newRequirements: string): Promise<GenerationData> {
    const prompt = `In the following HTML, find and regenerate the section identified as "${sectionIdentifier}" with these new requirements: "${newRequirements}"

Full content:
${fullContent}

Return the complete HTML with only the specified section updated.`;

    return this.generateWebsite(prompt, 'component');
  }
}