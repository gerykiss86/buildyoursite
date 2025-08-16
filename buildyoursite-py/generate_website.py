#!/usr/bin/env python3
"""
Website Generator using Claude API
Generates complete, ready-to-use websites as single JSX files with HTML wrapper
"""

import os
import sys
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional
import anthropic
from dotenv import load_dotenv

# Fix Unicode output on Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Load environment variables
load_dotenv()

class WebsiteGenerator:
    def __init__(self):
        """Initialize the generator with Claude API."""
        self.api_key = os.getenv('CLAUDE_API_KEY')
        if not self.api_key:
            raise ValueError("CLAUDE_API_KEY not found in .env file")
        
        self.client = anthropic.Anthropic(api_key=self.api_key)
        self.output_dir = Path("output")
        
    def extract_details(self, prompt: str) -> Dict[str, str]:
        """Extract company details from the prompt."""
        details = {
            "company_name": None,
            "email": None,
            "phone": None,
            "address": None,
            "tagline": None,
            "type": None
        }
        
        # Extract company name (various patterns)
        name_patterns = [
            r"company (?:name |called |named |is )?['\"]?([^'\",.]+)['\"]?",
            r"business (?:name |called |named |is )?['\"]?([^'\",.]+)['\"]?",
            r"(?:for |called |named )['\"]?([A-Z][^'\",.]+)['\"]?",
            r"['\"]([A-Z][^'\"]+)['\"]"
        ]
        
        for pattern in name_patterns:
            match = re.search(pattern, prompt, re.IGNORECASE)
            if match:
                details["company_name"] = match.group(1).strip()
                break
        
        # Extract email
        email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', prompt)
        if email_match:
            details["email"] = email_match.group(0)
        
        # Extract phone
        phone_patterns = [
            r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',
            r'\+\d{1,3}[-.\s]?\d{3,14}',
            r'\d{3}[-.\s]\d{3}[-.\s]\d{4}'
        ]
        for pattern in phone_patterns:
            match = re.search(pattern, prompt)
            if match:
                details["phone"] = match.group(0)
                break
        
        # Extract address
        address_patterns = [
            r"address:?\s*([^,.]+(?:,\s*[^,.]+){1,3})",
            r"located (?:at |in )?([^,.]+(?:,\s*[^,.]+){1,3})"
        ]
        for pattern in address_patterns:
            match = re.search(pattern, prompt, re.IGNORECASE)
            if match:
                details["address"] = match.group(1).strip()
                break
        
        # Extract tagline
        tagline_patterns = [
            r"tagline:?\s*['\"]([^'\"]+)['\"]",
            r"slogan:?\s*['\"]([^'\"]+)['\"]"
        ]
        for pattern in tagline_patterns:
            match = re.search(pattern, prompt, re.IGNORECASE)
            if match:
                details["tagline"] = match.group(1)
                break
                
        # Determine website type
        type_keywords = {
            "agency": ["agency", "creative", "marketing", "advertising", "consulting"],
            "portfolio": ["portfolio", "photography", "photographer", "designer", "artist", "creative"],
            "restaurant": ["restaurant", "cafe", "coffee", "bistro", "food", "dining", "bakery"],
            "ecommerce": ["shop", "store", "ecommerce", "retail", "boutique", "products"],
            "saas": ["saas", "software", "app", "platform", "tool", "service"],
            "corporate": ["corporate", "business", "company", "enterprise", "firm"],
            "medical": ["medical", "health", "clinic", "doctor", "dental", "healthcare"],
            "fitness": ["gym", "fitness", "wellness", "yoga", "sports", "training"],
            "education": ["school", "academy", "education", "learning", "course", "university"],
            "real_estate": ["real estate", "property", "realty", "homes", "housing"]
        }
        
        prompt_lower = prompt.lower()
        for site_type, keywords in type_keywords.items():
            if any(keyword in prompt_lower for keyword in keywords):
                details["type"] = site_type
                break
        
        if not details["type"]:
            details["type"] = "general"
            
        return details
    
    def create_enhanced_prompt(self, user_prompt: str, details: Dict[str, str]) -> str:
        """Create an enhanced prompt with extracted details."""
        base_prompt = f"""Create a complete, production-ready website as a single JSX React component based on this request: {user_prompt}

IMPORTANT REQUIREMENTS:
1. Create ONLY a single self-contained React component that can be rendered
2. Use inline styles or Tailwind CSS classes (assume Tailwind is available)
3. Include ALL content - no placeholders, lorem ipsum, or "coming soon" sections
4. Use real, free stock photo URLs from Unsplash (use format: https://images.unsplash.com/photo-[ID]?w=800&q=80)
5. Make it fully responsive with mobile menu
6. Include smooth scrolling navigation
7. Add hover effects and transitions
8. Create at least 5-7 main sections appropriate for the website type
9. Include a contact form and footer with all details
10. Use modern, professional design patterns

"""
        
        if details["company_name"]:
            base_prompt += f"\nCompany Name: {details['company_name']}"
        if details["email"]:
            base_prompt += f"\nEmail: {details['email']}"
        if details["phone"]:
            base_prompt += f"\nPhone: {details['phone']}"
        if details["address"]:
            base_prompt += f"\nAddress: {details['address']}"
        if details["tagline"]:
            base_prompt += f"\nTagline: {details['tagline']}"
            
        base_prompt += f"""

The component should:
- Be named {(details.get('company_name') or 'Website').replace(' ', '')}Website
- Include useState and useEffect hooks as needed
- Have a fixed navigation that changes on scroll
- Include relevant sections for a {details.get('type', 'modern')} website
- Use professional copy and realistic content
- Include testimonials with names and photos
- Have a working contact form structure
- Include social media links
- Be completely self-contained with no external dependencies except React

Return ONLY the JSX code starting with 'const' and ending with the export statement. Do not include import statements or explanations."""

        return base_prompt
    
    def generate_website_jsx(self, prompt: str) -> str:
        """Generate the website JSX using Claude API."""
        details = self.extract_details(prompt)
        enhanced_prompt = self.create_enhanced_prompt(prompt, details)
        
        print(f"🎨 Generating {details.get('type', 'modern')} website...")
        if details.get('company_name'):
            print(f"   Company: {details['company_name']}")
        
        try:
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=8000,
                temperature=0.7,
                messages=[
                    {
                        "role": "user",
                        "content": enhanced_prompt
                    }
                ]
            )
            
            jsx_content = response.content[0].text
            
            # Clean up the response - remove any markdown or explanations
            jsx_content = re.sub(r'^```jsx?\n?', '', jsx_content, flags=re.MULTILINE)
            jsx_content = re.sub(r'\n?```$', '', jsx_content, flags=re.MULTILINE)
            
            # Ensure it starts with const and has proper structure
            if not jsx_content.strip().startswith('const'):
                # Try to extract just the component code
                match = re.search(r'(const\s+\w+\s*=.*?export\s+default\s+\w+;?)', jsx_content, re.DOTALL)
                if match:
                    jsx_content = match.group(1)
            
            return jsx_content
            
        except Exception as e:
            print(f"❌ Error generating website: {e}")
            raise
    
    def create_html_wrapper(self, jsx_content: str, company_name: str = "Website") -> str:
        """Create an HTML file that loads and renders the JSX."""
        # Extract component name from the JSX
        component_match = re.search(r'const\s+(\w+)\s*=', jsx_content)
        component_name = component_match.group(1) if component_match else 'Website'
        
        # Add necessary imports to JSX for browser use
        browser_jsx = f"const {{ useState, useEffect }} = React;\n\n{jsx_content}"
        
        # Ensure export is handled for browser
        if 'export default' in browser_jsx:
            browser_jsx = browser_jsx.replace(f'export default {component_name}', '')
            browser_jsx += f"\n\n// Render the component\nconst root = ReactDOM.createRoot(document.getElementById('root'));\nroot.render(<{component_name} />);"
        else:
            browser_jsx += f"\n\n// Render the component\nconst root = ReactDOM.createRoot(document.getElementById('root'));\nroot.render(<{component_name} />);"
        
        html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{company_name}</title>
    
    <!-- React and Babel for JSX transformation -->
    <script crossorigin src="https://unpkg.com/react@18/umd/react.development.js"></script>
    <script crossorigin src="https://unpkg.com/react-dom@18/umd/react-dom.development.js"></script>
    <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
    
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    
    <style>
        /* Smooth scrolling */
        html {{
            scroll-behavior: smooth;
        }}
        
        /* Custom animations */
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        .fade-in {{
            animation: fadeIn 0.8s ease-out;
        }}
        
        /* Additional styles for better rendering */
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
        }}
    </style>
</head>
<body>
    <div id="root"></div>

    <script type="text/babel">
        {browser_jsx}
    </script>
</body>
</html>"""
        
        return html_template
    
    def save_output(self, jsx_content: str, html_content: str, project_name: str):
        """Save the generated files to the output directory."""
        # Create output directory with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        project_dir = self.output_dir / f"{project_name}_{timestamp}"
        project_dir.mkdir(parents=True, exist_ok=True)
        
        # Save JSX file
        jsx_path = project_dir / "component.jsx"
        with open(jsx_path, 'w', encoding='utf-8') as f:
            f.write(jsx_content)
        
        # Save HTML file
        html_path = project_dir / "index.html"
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        # Create a README
        readme_content = f"""# Generated Website

## Files
- `index.html` - Open this file in a browser to view the website
- `component.jsx` - The React component source code

## Usage
Simply open `index.html` in any modern web browser. No build process required!

## Generated
- Date: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
- Project: {project_name}

## Features
- Fully responsive design
- Modern UI with Tailwind CSS
- Interactive components with React
- Smooth scrolling navigation
- Contact form ready for backend integration
"""
        
        readme_path = project_dir / "README.md"
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        return project_dir
    
    def generate(self, prompt: str):
        """Main generation function."""
        print("🚀 Starting website generation...")
        print(f"📝 Prompt: {prompt}\n")
        
        # Extract details for project naming
        details = self.extract_details(prompt)
        project_name = (details.get('company_name') or details.get('type') or 'website').replace(' ', '_')
        
        # Generate JSX
        jsx_content = self.generate_website_jsx(prompt)
        
        # Create HTML wrapper
        company_name = details.get('company_name', 'Generated Website')
        html_content = self.create_html_wrapper(jsx_content, company_name)
        
        # Save files
        output_path = self.save_output(jsx_content, html_content, project_name)
        
        print(f"\n✅ Website generated successfully!")
        print(f"📁 Output saved to: {output_path}")
        print(f"🌐 Open {output_path / 'index.html'} in your browser to view the website")
        
        return output_path


def main():
    """Main entry point."""
    print("=" * 60)
    print("Website Generator - Powered by Claude AI")
    print("=" * 60)
    
    # Get user input
    if len(sys.argv) > 1:
        # Use command line argument
        prompt = ' '.join(sys.argv[1:])
    else:
        # Interactive mode
        print("\nEnter your website requirements:")
        print("Example: 'Create a modern photography agency website'")
        print("You can include: company name, email, phone, address, etc.")
        print("-" * 60)
        prompt = input("Your prompt: ").strip()
    
    if not prompt:
        print("❌ No prompt provided. Exiting.")
        return
    
    # Initialize generator and create website
    try:
        generator = WebsiteGenerator()
        generator.generate(prompt)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()