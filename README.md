# BuildYourSite

AI-powered website builder transitioning from internal tooling to a public SaaS platform.

## 🚀 Project Overview

BuildYourSite is a comprehensive tracking and analytics system for AI-powered website generation. It helps you:
- Track AI prompts and outputs
- Monitor manual edits and improvements
- Collect client feedback
- Analyze usage patterns
- Build towards autonomous website creation

## 📋 Current Phase: Phase 1 - Private Use

We're currently implementing the tracking infrastructure to monitor and analyze how AI tools are used in real client projects.

### Phase 1 Milestones ✅
- [x] Project structure and configuration
- [x] Database schema design (Prisma)
- [x] Core tracking modules:
  - [x] PromptLogger - Records AI generations
  - [x] EditTracker - Monitors manual changes
  - [x] FeedbackCollector - Captures client feedback
  - [x] UsageAnalytics - Analyzes tool usage
- [x] Comprehensive test suite
- [x] API endpoints for data collection
- [ ] Dashboard UI (in progress)
- [ ] Real project testing

## 🛠️ Tech Stack

- **Frontend**: Next.js 14 with TypeScript
- **Database**: PostgreSQL with Prisma ORM
- **Testing**: Jest + React Testing Library
- **Styling**: Tailwind CSS
- **API**: Next.js API Routes

## 📦 Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/buildyoursite.git
cd buildyoursite
```

2. Install dependencies:
```bash
npm install
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your database credentials
```

4. Set up the database:
```bash
npm run db:generate
npm run db:migrate
```

5. Run the development server:
```bash
npm run dev
```

## 🧪 Testing

Run the test suite:
```bash
npm test
```

Run tests with coverage:
```bash
npm run test:coverage
```

## 📊 Usage

### Creating a Project
```typescript
const project = await trackingSystem.createProject(
  "Client Website",
  "John Doe",
  "E-commerce site for local business"
);
```

### Logging AI Generations
```typescript
await trackingSystem.promptLogger.logGeneration(projectId, {
  prompt: "Create a modern landing page header",
  output: "<header>...</header>",
  model: "gpt-4",
  generationType: "component"
});
```

### Tracking Edits
```typescript
await trackingSystem.editTracker.trackEdit(projectId, {
  originalContent: "Original HTML",
  editedContent: "Edited HTML",
  editType: "style_modification",
  reason: "Improved responsive design"
});
```

### Collecting Feedback
```typescript
await trackingSystem.feedbackCollector.collectFeedback(projectId, {
  type: "design",
  content: "Love the modern look!",
  rating: 5,
  clientName: "John Doe"
});
```

## 🚦 Development Workflow

1. Always run tests before committing
2. Use TypeScript strict mode
3. Follow the established project structure
4. Document new features in CLAUDE.md
5. Track progress using the built-in todo system

## 📈 Next Steps

- Complete dashboard UI components
- Add real-time analytics
- Implement data export functionality
- Begin testing with real client projects
- Prepare for Phase 2: Internal Feedback Loops