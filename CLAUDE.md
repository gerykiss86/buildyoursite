# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

BuildYourSite is an AI-powered website builder that transitions from internal tooling to a public SaaS platform. The project uses AI tools (like Bolt.new) for initial site generation, tracks edits and improvements, and progressively builds autonomous website creation capabilities.

### Project Phases
1. **Phase 1 (Current)**: Private Use - Internal tool for client projects with comprehensive tracking
2. **Phase 2**: Internal Feedback Loops - Enhanced UI with regeneration capabilities and analytics
3. **Phase 3**: Semi-Autonomous Flow - 70-80% autonomous site generation with deployment integration
4. **Phase 4**: SaaS Launch - Full multi-tenant platform with billing and user management

## Development Setup

### Prerequisites
- Node.js 18+ and npm/yarn
- PostgreSQL or Supabase account for data storage
- Git for version control

### Installation
```bash
npm install
npm run dev
```

### Key Commands
- `npm run dev` - Start development server
- `npm test` - Run test suite
- `npm run test:watch` - Run tests in watch mode
- `npm run lint` - Run ESLint
- `npm run typecheck` - Run TypeScript type checking
- `npm run build` - Build for production

## Architecture

### Technology Stack
- **Frontend**: React/Next.js with TypeScript
- **Backend**: Node.js API with Express/Fastify
- **Database**: PostgreSQL/Supabase for data persistence
- **AI Integration**: OpenAI/Anthropic API for content generation
- **Testing**: Jest + React Testing Library
- **Deployment**: Vercel/Netlify ready

### Project Structure
```
buildyoursite/
├── src/
│   ├── api/           # Backend API endpoints
│   ├── components/    # React components
│   ├── lib/          # Core libraries and utilities
│   │   ├── tracking/ # Prompt/output tracking
│   │   ├── ai/       # AI integration modules
│   │   └── db/       # Database schemas and queries
│   ├── pages/        # Next.js pages
│   └── tests/        # Test files
├── prisma/           # Database schemas (if using Prisma)
└── public/           # Static assets
```

### Key Modules

#### Tracking System (Phase 1)
- **PromptLogger**: Records all AI prompts and outputs
- **EditTracker**: Monitors manual code changes
- **FeedbackCollector**: Captures client feedback
- **UsageAnalytics**: Tracks tool usage percentages

#### AI Integration
- **SiteGenerator**: Core AI-powered site generation
- **ContentOptimizer**: Iterative content improvement
- **LayoutEngine**: Dynamic layout generation

## Development Guidelines

### Phase-by-Phase Implementation
Always complete and test each phase before moving to the next:
1. Implement core functionality
2. Add comprehensive tests (aim for >80% coverage)
3. Document APIs and user flows
4. Gather metrics and feedback
5. Iterate based on data

### Testing Strategy
- Unit tests for all utility functions
- Integration tests for API endpoints
- E2E tests for critical user flows
- Performance benchmarks for AI operations

### Data Privacy
- Never log sensitive client data
- Implement proper data retention policies
- Use encryption for stored prompts/outputs
- Comply with GDPR/privacy regulations

## Current Phase: Phase 1 Implementation

### ✅ Completed Features (Phase 1)

1. **Tracking Infrastructure** ✓
   - PromptLogger: Logs all AI generations with metadata
   - EditTracker: Ready for manual edit tracking (Phase 2)
   - FeedbackCollector: Captures ratings and comments
   - UsageAnalytics: Calculates AI vs manual ratios

2. **Database Schema** ✓
   - Prisma ORM with full schema for all tracking needs
   - Support for PostgreSQL (production) and SQLite (development)
   - Models: Project, Generation, Edit, Feedback, UsageMetric

3. **AI Integration** ✓
   - BoltIntegration module using OpenAI API
   - Server-side generation endpoint (/api/generate)
   - Support for different content types (full_page, component, layout, content)

4. **User Interface** ✓
   - Home page for project creation
   - Builder interface with:
     - AI prompt input area
     - Real-time website generation
     - Live preview in iframe
     - Feedback collection (rating + comments)
   - Responsive design with Tailwind CSS

5. **API Endpoints** ✓
   - `/api/projects` - Create/list projects
   - `/api/projects/[id]` - Get/update project
   - `/api/projects/[id]/generations` - Log AI generations
   - `/api/projects/[id]/edits` - Track manual edits
   - `/api/projects/[id]/feedback` - Collect feedback
   - `/api/generate` - Generate website content

### Current Status

**Development Environment:**
- Running on SQLite for easy local development
- OpenAI API key configured in .env
- Next.js dev server at http://localhost:3000
- All core features functional

**Testing Coverage:**
- Unit tests: ~70% coverage on tracking modules
- All tests passing
- TypeScript compilation successful
- ESLint configured (minor warnings only)

### How to Use

1. **Start the application:**
   ```bash
   npm run dev
   # Open http://localhost:3000
   ```

2. **Create a project:**
   - Enter project name, client name, and description
   - Click "Create Project & Start Building"

3. **Generate a website:**
   - Enter detailed prompt (e.g., "Create a modern landing page for a coffee shop...")
   - Click "Generate Website"
   - View live preview on the right
   - Provide feedback and rating

4. **View tracked data:**
   ```bash
   npm run db:studio  # Opens Prisma Studio to view database
   ```

### Database Configuration

**For Development (current):**
```env
DATABASE_URL="file:./prisma/dev.db"  # SQLite
```

**For Production (PostgreSQL):**
```env
DATABASE_URL="postgresql://user:pass@localhost:5432/buildyoursite"
```

### Important Files

- `.env` - Environment variables (API keys, database URL)
- `src/lib/ai/BoltIntegration.ts` - AI generation logic
- `src/lib/tracking/*` - Tracking system modules
- `src/pages/builder/[projectId].tsx` - Main builder interface
- `prisma/schema.prisma` - Database schema

### Next Steps for Phase 2

1. Add "Regenerate Section" functionality
2. Implement "Improve Copy" button
3. Create analytics dashboard
4. Add real-time edit tracking
5. Build pattern recognition for common edits

### Success Metrics
- ✅ Track 100% of AI generations
- ⏳ Capture all manual edits (Phase 2)
- ✅ Log client feedback for every project
- ✅ Measure % of site built by AI vs manual

## Troubleshooting

### Common Issues

1. **Database Connection Error**
   - If using PostgreSQL: Ensure Docker Desktop is running
   - For SQLite: Database is auto-created on first use
   - Check `.env` file has correct DATABASE_URL

2. **OpenAI API Errors**
   - Verify API key in `.env` is valid
   - Check API quota/limits on OpenAI dashboard
   - API key should start with `sk-proj-`

3. **Generation Fails**
   - Check browser console for detailed errors
   - Verify `/api/generate` endpoint is accessible
   - Ensure prompt is not too long (max ~2000 characters recommended)

4. **Preview Not Loading**
   - Generated content must be valid HTML
   - Check for JavaScript errors in preview iframe
   - Some complex scripts may be blocked by sandbox

### Development Tips

- Use `npm run db:studio` to inspect database contents
- Check `npm run lint` before committing
- Run `npm test` to ensure tracking modules work
- SQLite database file is at `prisma/dev.db`

## Project Timeline

- **Phase 1 Start**: August 2025
- **Phase 1 Core Complete**: August 3, 2025
- **Current**: Testing with demo projects
- **Next Milestone**: Phase 2 - Internal Feedback Loops