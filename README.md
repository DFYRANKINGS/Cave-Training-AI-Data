# Client AI Data Template

A comprehensive template repository for creating AI-optimized client data systems with automated workflows, structured data generation, and multi-platform content distribution.

## 🚀 Quick Start

1. **Copy this template** to create a new repository for your client
2. **Update client data** in `templates/client-data.xlsx`
3. **Configure GitHub Actions** secrets (see [Configuration](#configuration))
4. **Push changes** to trigger automated workflows

## 📁 Repository Structure

```
├── .github/workflows/          # GitHub Actions workflows
│   ├── auto-refresh.yml       # Automated refresh workflow
│   └── build_ai_files_and_ping_xlsx.yml  # Main processing workflow
├── docs/                      # Documentation
│   ├── comprehensive_readme.md
│   ├── configuration_templates.md
│   ├── deployment_instructions.md
│   ├── documentation_summary.md
│   ├── google_sheets_setup_guide.md
│   ├── testing_guide.md
│   └── troubleshooting_guide.md
├── templates/                 # Template files
│   ├── client-data.xlsx      # Main client data template
│   └── google_sheet_push_xlsx_to_github.js  # Google Sheets integration
├── ai-content/               # Generated AI content
├── schemas/                  # JSON-LD schemas
├── generate_files_xlsx.py    # Enhanced file generation script
├── generate_sitemaps.py      # Sitemap generation script
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## 🔧 Configuration

### Required GitHub Secrets

Set these in your repository settings under **Settings > Secrets and variables > Actions**:

- `GITHUB_TOKEN` - Automatically provided by GitHub
- `GOOGLE_SHEETS_API_KEY` - For Google Sheets integration (optional)
- `SEARCH_CONSOLE_API_KEY` - For search engine notifications (optional)

### Client Data Setup

1. **Excel Method (Recommended)**:
   - Edit `templates/client-data.xlsx`
   - Use multiple sheets for different data types
   - Push changes to trigger workflows

2. **Google Sheets Method**:
   - Follow the guide in `docs/google_sheets_setup_guide.md`
   - Use the provided Google Apps Script

## 🤖 AI Features

- **Structured Data Generation**: Automatic JSON-LD schema creation
- **LLM Training Files**: Optimized content for AI crawlers
- **FAQ Generation**: Automated FAQ schema and content
- **Sitemap Management**: Dynamic sitemap generation and submission
- **Multi-format Output**: JSON, YAML, Markdown, and LLM formats

## 📊 Supported Data Types

- Organization information
- Services and products
- Locations and contact details
- FAQs and testimonials
- Licensing and certifications
- Custom schemas

## 🔄 Automated Workflows

### Main Workflow (`build_ai_files_and_ping_xlsx.yml`)
- Triggers on Excel file changes
- Generates all output formats
- Creates sitemaps
- Notifies search engines

### Auto-refresh Workflow (`auto-refresh.yml`)
- Scheduled updates
- Keeps content fresh
- Maintains search engine visibility

## 📚 Documentation

Comprehensive guides are available in the `docs/` directory:

- **[Deployment Instructions](docs/deployment_instructions.md)** - Step-by-step setup
- **[Google Sheets Setup](docs/google_sheets_setup_guide.md)** - Integration guide
- **[Testing Guide](docs/testing_guide.md)** - Quality assurance
- **[Troubleshooting](docs/troubleshooting_guide.md)** - Common issues
- **[Configuration Templates](docs/configuration_templates.md)** - Advanced setup

## 🛠️ Development

### Local Setup

```bash
# Clone the repository
git clone https://github.com/DFYRANKINGS/client-ai-data-template.git
cd client-ai-data-template

# Install dependencies
pip install -r requirements.txt

# Run file generation
python generate_files_xlsx.py

# Generate sitemaps
python generate_sitemaps.py
```

### Testing

```bash
# Run comprehensive tests
python -m pytest tests/

# Validate generated schemas
python validate_schemas.py
```

## 🔍 SEO & AI Optimization

- **Schema.org compliance** for rich snippets
- **AI crawler optimization** with structured training data
- **Multi-platform compatibility** (Google, Bing, AI assistants)
- **Automated sitemap management** with search engine notifications
- **Performance monitoring** and optimization

## 📈 Analytics & Monitoring

- GitHub Actions workflow monitoring
- Schema validation reports
- Sitemap submission tracking
- Performance metrics

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This template is provided as-is for client projects. Customize as needed for your specific requirements.

## 🆘 Support

- Check the [Troubleshooting Guide](docs/troubleshooting_guide.md)
- Review [Documentation](docs/documentation_summary.md)
- Create an issue for bugs or feature requests

---

**Template Version**: 2.0  
**Last Updated**: September 2024  
**Maintained by**: DFYRANKINGS
