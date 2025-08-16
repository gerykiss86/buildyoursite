# Website Generator - Claude AI Powered

Generate complete, production-ready websites using Claude AI with a single command.

## Features

- 🚀 **One-command website generation**
- 🎨 **Complete JSX components** with React
- 📱 **Fully responsive** designs with Tailwind CSS
- 🖼️ **Real stock photos** from Unsplash
- 📝 **Smart prompt parsing** - extracts company details automatically
- 🌐 **Ready-to-view HTML** - no build process needed
- 📁 **Organized output** with timestamped folders

## Installation

1. Clone or download this repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file with your Claude API key:
```
CLAUDE_API_KEY=your_api_key_here
```

Get your API key from [Anthropic Console](https://console.anthropic.com/)

## Usage

### Interactive Mode
```bash
python generate_website.py
```
Then enter your prompt when asked.

### Command Line Mode
```bash
python generate_website.py "create a modern photography agency website"
```

### With Company Details
Include specific details in your prompt:
```bash
python generate_website.py "create a restaurant website for 'Bella Vista Italian Bistro' with email: info@bellavista.com, phone: (555) 123-4567, address: 123 Main St, New York, NY 10001"
```

## Supported Website Types

The generator automatically detects and optimizes for:
- 📸 **Portfolio/Photography** sites
- 🍔 **Restaurant/Cafe** websites
- 🏢 **Corporate/Business** sites
- 🛍️ **E-commerce** stores
- 💻 **SaaS** platforms
- 🏥 **Medical/Healthcare** sites
- 💪 **Fitness/Gym** websites
- 🎓 **Education** platforms
- 🏠 **Real Estate** sites
- And more...

## Output Structure

Each generated website includes:
```
output/
└── CompanyName_20240101_120000/
    ├── index.html      # Open this in browser
    ├── component.jsx   # React component source
    └── README.md       # Project information
```

## Examples

### Basic Usage
```bash
python generate_website.py "create a modern tech startup website"
```

### With Company Name
```bash
python generate_website.py "create a portfolio site for 'Creative Studios'"
```

### Full Details
```bash
python generate_website.py "create a fitness gym website called 'PowerFit Gym' with email: info@powerfit.com, phone: (555) 987-6543, tagline: 'Transform Your Body, Transform Your Life'"
```

## Features Generated

Every website includes:
- ✅ Responsive navigation with mobile menu
- ✅ Hero section with call-to-action
- ✅ Services/Products section
- ✅ About/Team section
- ✅ Portfolio/Gallery (when relevant)
- ✅ Testimonials
- ✅ Contact form
- ✅ Footer with social links
- ✅ Smooth scrolling
- ✅ Hover effects and animations

## Requirements

- Python 3.7+
- Claude API key (from Anthropic)
- Internet connection for API calls

## Tips

1. **Be specific**: Include company name, industry, and style preferences
2. **Add details**: Email, phone, address will be automatically incorporated
3. **Specify sections**: Mention specific sections you want included
4. **Style preferences**: Mention color schemes or design styles

## Troubleshooting

### API Key Issues
- Ensure your `.env` file contains: `CLAUDE_API_KEY=your_actual_key`
- Check that the key starts with `sk-ant-`

### Generation Errors
- Try a simpler prompt first
- Ensure you have internet connection
- Check API quota limits

## License

MIT License - Feel free to use for any purpose.

## Support

For issues or suggestions, please create an issue on GitHub.