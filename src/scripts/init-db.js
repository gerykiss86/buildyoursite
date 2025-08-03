const { PrismaClient } = require('@prisma/client');

const prisma = new PrismaClient();

async function main() {
  console.log('Initializing database...');
  
  try {
    // Test the connection
    await prisma.$connect();
    console.log('Database connected successfully');
    
    // Create a test project to ensure schema is working
    const testProject = await prisma.project.create({
      data: {
        name: 'Test Project',
        clientName: 'Test Client',
        description: 'This is a test project to verify database setup',
      },
    });
    
    console.log('Test project created:', testProject);
    
    // Clean up test project
    await prisma.project.delete({
      where: { id: testProject.id },
    });
    
    console.log('Database initialization complete!');
  } catch (error) {
    console.error('Database initialization failed:', error);
    process.exit(1);
  } finally {
    await prisma.$disconnect();
  }
}

main();