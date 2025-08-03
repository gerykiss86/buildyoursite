const { Builder, By, until } = require('selenium-webdriver');

async function testProjectCreation() {
  let driver;
  
  try {
    console.log('Starting test...');
    
    // Use Chrome directly since it's already installed
    driver = await new Builder().forBrowser('chrome').build();
    
    // Navigate to home page
    console.log('Navigating to http://localhost:3000');
    await driver.get('http://localhost:3000');
    await driver.sleep(2000);
    
    // Fill in the form
    console.log('Filling in project form...');
    await driver.findElement(By.id('projectName')).sendKeys('Test Coffee Shop');
    await driver.findElement(By.id('clientName')).sendKeys('Test Client');
    await driver.findElement(By.id('description')).sendKeys('A test project for debugging');
    
    // Take screenshot before submit
    console.log('Taking screenshot before submit...');
    
    // Submit the form
    console.log('Submitting form...');
    const submitButton = await driver.findElement(By.css('button[type="submit"]'));
    await submitButton.click();
    
    // Wait for navigation or error
    await driver.sleep(3000);
    
    // Check current URL
    const currentUrl = await driver.getCurrentUrl();
    console.log('Current URL after submit:', currentUrl);
    
    // Check for any error messages
    const pageSource = await driver.getPageSource();
    if (pageSource.includes('Project not found')) {
      console.error('ERROR: "Project not found" message detected');
      
      // Let's check what's in the URL
      if (currentUrl.includes('/builder/')) {
        const projectId = currentUrl.split('/builder/')[1];
        console.log('Project ID from URL:', projectId);
        
        // Test if the project exists in our temp API
        const fetch = require('node-fetch');
        try {
          const response = await fetch(`http://localhost:3000/api/projects-temp/${projectId}`);
          const data = await response.json();
          console.log('API response for project:', data);
        } catch (err) {
          console.error('Failed to fetch project from API:', err);
        }
      }
    } else {
      console.log('Successfully navigated to builder page!');
    }
    
  } catch (error) {
    console.error('Test failed:', error);
  } finally {
    if (driver) {
      await driver.quit();
    }
  }
}

// Run the test
testProjectCreation().catch(console.error);