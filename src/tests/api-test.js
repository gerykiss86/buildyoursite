async function testAPIFlow() {
  console.log('Testing API flow...\n');
  
  try {
    // 1. Create a project
    console.log('1. Creating project...');
    const createResponse = await fetch('http://localhost:3000/api/projects-temp', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        name: 'API Test Project',
        clientName: 'Test Client',
        description: 'Testing the API flow'
      })
    });
    
    const project = await createResponse.json();
    console.log('Created project:', project);
    
    if (!project.id) {
      throw new Error('No project ID returned');
    }
    
    // 2. Fetch the project
    console.log('\n2. Fetching project by ID...');
    const getResponse = await fetch(`http://localhost:3000/api/projects-temp/${project.id}`);
    const fetchedProject = await getResponse.json();
    console.log('Fetched project:', fetchedProject);
    
    // 3. Test what the builder page would receive
    console.log('\n3. Testing builder page fetch...');
    const builderUrl = `http://localhost:3000/builder/${project.id}`;
    console.log('Builder would navigate to:', builderUrl);
    console.log('Builder would fetch from:', `http://localhost:3000/api/projects-temp/${project.id}`);
    
    // 4. Test generation endpoint
    console.log('\n4. Testing generation endpoint...');
    const genResponse = await fetch('http://localhost:3000/api/generate-temp', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        projectId: project.id,
        prompt: 'Create a simple test page',
        type: 'full_page'
      })
    });
    
    if (!genResponse.ok) {
      const error = await genResponse.text();
      console.error('Generation failed:', error);
    } else {
      const genData = await genResponse.json();
      console.log('Generation successful:', genData.generation.id);
    }
    
  } catch (error) {
    console.error('Test failed:', error);
  }
}

// Run the test
testAPIFlow();