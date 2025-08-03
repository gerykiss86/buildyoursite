# BuildYourSite - Startup Guide

## Prerequisites

1. **Docker Desktop** must be installed and running
2. **Node.js 18+** and npm installed
3. **Git** for version control

## Quick Start

### 1. Start PostgreSQL Database

First, ensure Docker Desktop is running, then:

```bash
# Start PostgreSQL container
docker compose up -d

# Verify it's running
docker ps
```

You should see a container named `buildyoursite-db` running.

### 2. Install Dependencies

```bash
npm install
```

### 3. Set Up Database

```bash
# Generate Prisma client
npm run db:generate

# Run database migrations
npm run db:migrate
```

If you get a connection error, wait a few seconds for PostgreSQL to fully start, then try again.

### 4. Start Development Server

```bash
npm run dev
```

The application will be available at http://localhost:3000

## Using the Application

### Creating Your First Project

1. Navigate to http://localhost:3000
2. Fill in the project details:
   - **Project Name**: e.g., "Coffee Shop Website"
   - **Client Name**: e.g., "John's Coffee"
   - **Description**: Describe what kind of website you want
3. Click "Create Project & Start Building"

### Generating a Website

1. In the builder interface, describe your website in detail:
   ```
   Create a modern, responsive website for a coffee shop called "John's Coffee". 
   Include:
   - A hero section with a background image and welcome message
   - A menu section showcasing coffee and pastries
   - An about us section with the shop's story
   - A contact section with hours and location
   - Modern, warm color scheme with browns and creams
   ```

2. Click "Generate Website"
3. The AI will create a complete HTML website with inline CSS
4. Preview appears on the right side

### Tracking Features

All interactions are automatically tracked:
- **Generations**: Every AI-generated website is logged
- **Edits**: Manual changes are tracked (coming in Phase 2)
- **Feedback**: Rate and comment on generated content
- **Analytics**: View usage statistics in the dashboard

## Troubleshooting

### Docker Issues

If Docker isn't running:
1. Open Docker Desktop
2. Wait for it to fully start
3. Run `docker compose up -d` again

### Database Connection Issues

If you can't connect to the database:
1. Check Docker container is running: `docker ps`
2. Verify `.env` file exists with correct `DATABASE_URL`
3. Try restarting the container: 
   ```bash
   docker compose down
   docker compose up -d
   ```

### API Key Issues

If website generation fails:
1. Check the `.env` file contains `OPENAI_API_KEY`
2. Verify the API key is valid
3. Check the browser console for error messages

## Environment Variables

The `.env` file should contain:
```
DATABASE_URL="postgresql://postgres:postgres@localhost:5432/buildyoursite?schema=public"
OPENAI_API_KEY="your-api-key-here"
NODE_ENV="development"
NEXT_PUBLIC_API_URL="http://localhost:3000/api"
NEXT_PUBLIC_APP_NAME="BuildYourSite"
```

## Next Steps

1. Generate a few test websites
2. Provide feedback and ratings
3. Check the database for tracked data:
   ```bash
   npm run db:studio
   ```
4. View analytics and usage patterns
5. Prepare for Phase 2: Internal Feedback Loops

## Development Commands

- `npm run dev` - Start development server
- `npm test` - Run tests
- `npm run lint` - Check code quality
- `npm run typecheck` - Check TypeScript types
- `npm run db:studio` - Open Prisma Studio to view data
- `docker compose logs -f` - View PostgreSQL logs