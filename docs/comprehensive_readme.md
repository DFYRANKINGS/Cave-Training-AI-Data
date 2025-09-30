# GitHub Workflow System for AI Visibility and SEO

A comprehensive automation system that transforms Google Sheets data into structured files and sitemaps for enhanced AI discoverability and SEO optimization.

## 🚀 Quick Start

1. **[Google Sheets Integration](google_sheets_setup_guide.md)** - Connect your Google Sheets to GitHub
2. **[Deploy to Repository](deployment_instructions.md)** - Set up the workflow system
3. **[Test Everything](testing_guide.md)** - Validate your setup
4. **[Configure Advanced Options](configuration_templates.md)** - Customize for your needs

**Need help?** Check the **[Troubleshooting Guide](troubleshooting_guide.md)** for common issues and solutions.

---

## 📖 Table of Contents

- [System Overview](#system-overview)
- [Features](#features)
- [Architecture](#architecture)
- [Setup Guides](#setup-guides)
- [Configuration](#configuration)
- [Usage](#usage)
- [Maintenance](#maintenance)
- [Support](#support)

---

## System Overview

This system automates the process of generating structured data files from Google Sheets, making your business data discoverable by AI systems and search engines. It's designed for agencies, consultancies, and businesses who want to maximize their online visibility and AI discoverability.

### What It Does

```
Google Sheets Data → Excel Export → GitHub Repository → Generated Files → Search Engine Sitemaps
```

1. **Data Collection**: Maintain client/business data in Google Sheets
2. **Automated Export**: Google Apps Script exports data to GitHub as Excel files
3. **File Generation**: Python scripts convert Excel data into JSON, YAML, Markdown, and LLM-friendly formats
4. **Sitemap Creation**: XML sitemaps are generated for search engine optimization
5. **Search Engine Notification**: Automatic pings to Google and Bing when content updates

### Key Benefits

- ✅ **AI Discoverability**: Structured data formats optimized for AI systems
- ✅ **SEO Enhancement**: XML sitemaps and search engine notifications
- ✅ **Automation**: Hands-off workflow after initial setup
- ✅ **Scalability**: Handle multiple clients with single system
- ✅ **Flexibility**: Customizable file formats and processing rules
- ✅ **Integration**: Seamless Google Sheets to GitHub workflow

---

## Features

### 🔄 Automation Features
- **Scheduled Updates**: Weekly automatic refresh of generated files
- **Trigger-Based Processing**: Updates when Excel data changes
- **Search Engine Notifications**: Automatic sitemap pings to Google and Bing
- **Error Handling**: Robust error handling with detailed logging

### 📊 Data Processing
- **Multi-Format Output**: JSON, YAML, Markdown, and LLM text formats
- **Data Validation**: Filters empty fields and validates data integrity
- **Unicode Support**: Full international character support
- **Flexible Schema**: Adapts to your data structure

### 🗺️ SEO & Discovery
- **XML Sitemaps**: Standards-compliant sitemaps for each domain
- **Sitemap Indexing**: Master sitemap index for multiple clients
- **Domain Validation**: Filters placeholder domains automatically
- **File Linking**: Direct URLs to all generated content

### 🔧 Customization
- **Environment Configs**: Development, staging, and production environments
- **Feature Flags**: Enable/disable specific functionality
- **Custom Templates**: Modify file generation templates
- **Performance Tuning**: Configurable processing limits and optimizations

---

## Architecture

### System Components

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Google        │    │     GitHub       │    │   Generated     │
│   Sheets        │───▶│   Repository     │───▶│   Content       │
│                 │    │                  │    │                 │
│ • Client Data   │    │ • Excel Files    │    │ • JSON Files    │
│ • Manual Updates│    │ • Python Scripts │    │ • YAML Files    │
│ • Collaboration │    │ • Workflows      │    │ • Markdown      │
└─────────────────┘    └──────────────────┘    │ • LLM Text      │
                                               │ • XML Sitemaps  │
                                               └─────────────────┘
```

### Workflow Process

1. **Data Entry**: Users update data in Google Sheets
2. **Export Trigger**: Google Apps Script exports data to GitHub
3. **Workflow Activation**: GitHub Actions detects file changes
4. **File Generation**: Python scripts process Excel data
5. **Content Creation**: Multiple file formats generated
6. **Sitemap Building**: XML sitemaps created for each domain
7. **Search Notification**: Search engines notified of updates

### File Structure

```
your-repository/
├── .github/
│   └── workflows/           # GitHub Actions workflows
│       ├── auto-refresh.yml
│       ├── build_ai_files_and_ping_xlsx.yml
│       └── sitemap.yml
├── ai-generators/          # Python processing scripts
│   ├── generate_files_xlsx.py
│   └── requirements.txt
├── data/                   # Source data files
│   └── client-data.xlsx
├── schema-files/           # Generated structured files
│   ├── client1/
│   │   ├── client1.json
│   │   ├── client1.yaml
│   │   ├── client1.md
│   │   └── client1.llm
│   └── client2/...
├── sitemaps/              # Generated XML sitemaps
│   ├── client1_sitemap.xml
│   ├── client2_sitemap.xml
│   └── _report.txt
├── generate_sitemaps.py   # Sitemap generation script
└── ai-sitemap.xml        # Master sitemap
```

---

## Setup Guides

### 📋 Complete Setup Checklist

Follow these guides in order for a complete setup:

#### 1. Google Sheets Integration Setup
**📚 [Detailed Guide](google_sheets_setup_guide.md)**

- [ ] Create Google Cloud Project
- [ ] Enable required APIs
- [ ] Set up OAuth consent screen
- [ ] Create GitHub personal access token
- [ ] Configure Google Apps Script
- [ ] Test the integration

**Time Required**: 30-45 minutes

#### 2. Repository Deployment
**📚 [Detailed Guide](deployment_instructions.md)**

- [ ] Create repository directory structure
- [ ] Deploy workflow files
- [ ] Copy Python scripts
- [ ] Configure repository settings
- [ ] Set environment variables
- [ ] Test deployment

**Time Required**: 20-30 minutes

#### 3. System Testing
**📚 [Detailed Guide](testing_guide.md)**

- [ ] Test local file generation
- [ ] Validate sitemap creation
- [ ] Test GitHub Actions workflows
- [ ] Verify end-to-end integration
- [ ] Performance validation

**Time Required**: 45-60 minutes

#### 4. Advanced Configuration
**📚 [Configuration Templates](configuration_templates.md)**

- [ ] Environment-specific settings
- [ ] Custom file generation rules
- [ ] Performance optimization
- [ ] Security configuration

**Time Required**: 15-30 minutes (optional)

### 🎯 Environment-Specific Setup

#### Production Environment
```bash
# Repository Variables
SITE_BASE_URL=https://www.client-domain.com
ENVIRONMENT=production

# Features
- Weekly automated updates
- Search engine notifications enabled
- Error logging only
- Full validation enabled
```

#### Staging Environment
```bash
# Repository Variables  
SITE_BASE_URL=https://staging.client-domain.com
ENVIRONMENT=staging

# Features
- Manual trigger testing
- Search engine notifications disabled
- Debug logging enabled
- Validation with warnings
```

#### Development Environment
```bash
# Local Environment Variables
SITE_BASE_URL=http://localhost:8080
ENVIRONMENT=development

# Features
- Frequent updates for testing
- All debug information
- Validation disabled
- Local file serving
```

---

## Configuration

### Repository Variables

Navigate to: **Repository Settings → Secrets and variables → Actions → Variables**

| Variable | Description | Example |
|----------|-------------|---------|
| `SITE_BASE_URL` | Base domain for generated URLs | `https://www.client-domain.com` |
| `ENVIRONMENT` | Deployment environment | `production`, `staging`, `development` |

### Environment Files

For local development, create environment files:

**`.env.production`**
```bash
SITE_BASE_URL=https://www.client-domain.com
ENVIRONMENT=production
LOG_LEVEL=ERROR
ENABLE_SEARCH_PING=true
```

**`.env.development`**
```bash
SITE_BASE_URL=http://localhost:8080
ENVIRONMENT=development
LOG_LEVEL=DEBUG
ENABLE_SEARCH_PING=false
```

### Data Schema

Your Excel file should include these columns (minimum):

| Column | Required | Description | Example |
|--------|----------|-------------|---------|
| `client_name` | ✅ Yes | Client or business name | "Acme Corporation" |
| `website` | ✅ Yes | Primary website URL | "https://acme-corp.com" |
| `category` | No | Business category | "Technology" |
| `description` | No | Business description | "Leading tech solutions" |

**Additional columns**: Any additional columns will be included in generated files.

---

## Usage

### Daily Operations

Once set up, the system operates automatically:

1. **Update Data**: Edit your Google Sheets as needed
2. **Sync to GitHub**: Use "GitHub → Commit XLSX to GitHub" in Google Sheets
3. **Automatic Processing**: GitHub Actions processes changes automatically
4. **Monitoring**: Check Actions tab for workflow status

### Manual Operations

#### Trigger Manual Update
- Go to repository **Actions** tab
- Select "Build AI files from XLSX and ping sitemap"
- Click "Run workflow"

#### Test Local Changes
```bash
# Set up local environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r ai-generators/requirements.txt

# Set environment variables
export SITE_BASE_URL="http://localhost:8080"

# Run file generation
cd ai-generators
python generate_files_xlsx.py
cd ..

# Run sitemap generation
python generate_sitemaps.py
```

#### View Generated Files
- **In Repository**: Navigate to `schema-files/` directory
- **Live URLs**: Visit `https://your-domain.com/schema-files/client-name/client-name.json`
- **Sitemaps**: Check `sitemaps/` directory for XML files

### Integration with Other Systems

#### Use Generated Data in Applications
```javascript
// Fetch client data in your application
const clientData = await fetch('https://your-domain.com/schema-files/acme-corp/acme-corp.json');
const data = await clientData.json();
console.log(data);
```

#### Monitor with External Tools
```bash
# Check sitemap status
curl -I "https://your-domain.com/ai-sitemap.xml"

# Validate XML
curl "https://your-domain.com/sitemaps/client_sitemap.xml" | xmllint --format -
```

---

## Maintenance

### Regular Tasks

#### Weekly (Automated)
- ✅ File generation refresh
- ✅ Sitemap updates  
- ✅ Search engine notifications

#### Monthly (Manual)
- [ ] Review workflow performance
- [ ] Check error logs
- [ ] Validate generated file quality
- [ ] Update documentation

#### Quarterly (Manual) 
- [ ] Review and rotate GitHub tokens
- [ ] Performance optimization review
- [ ] Backup configuration
- [ ] Team training updates

### Monitoring

#### GitHub Actions Dashboard
Monitor workflow health at: `https://github.com/your-username/your-repo/actions`

#### Key Metrics to Watch
- **Workflow Success Rate**: Should be >95%
- **Processing Time**: Should be <5 minutes for normal datasets
- **File Generation**: Should match number of data rows
- **Search Engine Pings**: Check logs for successful notifications

#### Alerts Setup
Configure email notifications:
1. Go to repository **Settings**
2. Select **Notifications**
3. Enable **Actions** notifications
4. Add team email addresses

### Performance Optimization

#### Large Dataset Handling
For 100+ clients:
- Enable batch processing in configuration
- Consider splitting data across multiple repositories
- Implement CDN for generated files
- Monitor GitHub Actions usage limits

#### File Size Management
```python
# Add to configuration for large files
MAX_FILE_SIZE_MB = 5
COMPRESS_OUTPUT = true
ENABLE_GZIP = true
```

---

## Support

### Self-Service Resources

1. **📚 [Troubleshooting Guide](troubleshooting_guide.md)** - Common issues and solutions
2. **🧪 [Testing Guide](testing_guide.md)** - Comprehensive testing procedures
3. **⚙️ [Configuration Templates](configuration_templates.md)** - Advanced configuration options
4. **🔧 GitHub Actions Logs** - Real-time workflow debugging

### Getting Help

#### Before Requesting Support

1. **Check the troubleshooting guide** for known issues
2. **Review GitHub Actions logs** for specific error messages
3. **Test locally** to isolate the problem
4. **Gather system information** using diagnostic commands

#### Information to Include

When seeking support, provide:

```bash
# Run these diagnostic commands and include output
echo "=== SYSTEM INFO ==="
python --version
git --version
git remote -v

echo "=== REPOSITORY STATUS ==="  
git status --porcelain
ls -la .github/workflows/

echo "=== ENVIRONMENT ==="
env | grep -E "(SITE_BASE|GITHUB)" || echo "No relevant env vars"

echo "=== RECENT ERRORS ==="
# Include any error messages, stack traces, or workflow logs
```

#### Escalation Path

1. **Level 1**: Self-service using documentation
2. **Level 2**: Repository issues for bugs or feature requests  
3. **Level 3**: Direct support contact for critical issues

### Contributing

#### Reporting Issues
- Use GitHub Issues for bug reports
- Include reproduction steps and system information
- Label issues appropriately (bug, enhancement, documentation)

#### Submitting Improvements
- Fork the repository
- Create feature branch
- Submit pull request with clear description
- Include tests for new functionality

---

## Security

### Data Protection
- **No sensitive data** in repository (use environment variables)
- **Token rotation** every 6-12 months
- **Repository access control** via GitHub permissions
- **Audit logs** via GitHub Actions logs

### Best Practices
- Use minimal required GitHub token permissions
- Review generated files for sensitive information
- Monitor repository access and changes
- Keep dependencies updated

---

## FAQ

### General Questions

**Q: How often are files updated?**
A: Automatically every Sunday at 4 AM UTC, plus whenever the Excel file changes.

**Q: Can I customize the generated file formats?**
A: Yes, modify the Python scripts in `ai-generators/` to change output formats.

**Q: What happens if my Google Sheets has errors?**
A: The system filters out empty data and logs errors. Check GitHub Actions logs for details.

**Q: Can I use this with multiple clients?**
A: Yes, each row in your Excel file represents a different client/business.

### Technical Questions

**Q: Why are some domains filtered out of sitemaps?**
A: Placeholder domains (example.com, yourdomain.com) are automatically filtered. Update with real domains.

**Q: How do I add custom data fields?**
A: Simply add columns to your Excel file. They'll automatically be included in generated files.

**Q: Can I run this system locally?**
A: Yes, set up the Python environment and run the scripts locally for testing.

**Q: What's the maximum data size supported?**
A: GitHub has file size limits (~100MB), but normal business data stays well under this.

### Troubleshooting Questions

**Q: Workflow fails with "Permission denied"?**
A: Check repository settings → Actions permissions → Enable "Read and write permissions"

**Q: Files not generating properly?**
A: Run the testing script locally: `python test-configuration.py`

**Q: Search engine pings failing?**
A: This is normal - search engines often ignore pings. Check your sitemap URL directly.

---

## Changelog

### Version 2.0.0 (Current)
- ✅ Multi-environment support
- ✅ Enhanced error handling
- ✅ Comprehensive testing suite
- ✅ Advanced configuration options
- ✅ Performance optimizations

### Version 1.0.0
- ✅ Basic file generation
- ✅ Google Sheets integration  
- ✅ Simple sitemap creation
- ✅ GitHub Actions workflows

---

## License

This system is provided as-is for educational and business use. Modify and adapt as needed for your specific requirements.

---

## Quick Reference

### 🚀 Essential Commands

```bash
# Setup
./setup-system.sh

# Test configuration
python test-configuration.py

# Local development
cd ai-generators && python generate_files_xlsx.py && cd .. && python generate_sitemaps.py

# View results
ls -la schema-files/
cat sitemaps/_report.txt
```

### 🔗 Important Links

- **📚 [Google Sheets Setup](google_sheets_setup_guide.md)** - Complete integration guide
- **🚀 [Deployment Instructions](deployment_instructions.md)** - Repository setup
- **🧪 [Testing Guide](testing_guide.md)** - Validation procedures  
- **🔧 [Troubleshooting](troubleshooting_guide.md)** - Problem solving
- **⚙️ [Configuration](configuration_templates.md)** - Advanced options

### 📞 Support Contacts

- **Documentation Issues**: Check GitHub repository issues
- **Technical Support**: Review troubleshooting guide first
- **Feature Requests**: Submit GitHub issue with enhancement label

---

**Made with ❤️ for better AI discoverability and SEO optimization**

*Last updated: September 27, 2025*
