# Deployment Instructions

## Overview

This guide covers deploying the GitHub workflow system to client repositories. The system consists of Python scripts, GitHub Actions workflows, and configuration files that work together to generate structured data files and sitemaps from Excel data.

## System Architecture Overview

```
Google Sheets → Google Apps Script → GitHub Repository
                                           ↓
                                   GitHub Actions Workflows
                                           ↓
                               Python File Generation Scripts
                                           ↓
                              Generated Files + Sitemaps + Search Engine Pings
```

## Prerequisites

- GitHub repository with Actions enabled
- Admin access to the target repository
- Python 3.11+ environment for local testing (optional)
- Understanding of GitHub Actions and repository structure

## Step 1: Repository Structure Setup

### 1.1 Create Required Directory Structure

Set up the following directory structure in your client repository:

```
your-repo/
├── .github/
│   └── workflows/
│       ├── auto-refresh.yml
│       ├── build_ai_files_and_ping_xlsx.yml
│       └── sitemap.yml
├── ai-generators/
│   ├── generate_files_xlsx.py
│   └── requirements.txt
├── data/
│   └── client-data.xlsx
├── schema-files/
│   └── (generated files will go here)
├── sitemaps/
│   └── (generated sitemaps will go here)
├── locations/
│   └── (optional: manual JSON/YAML files)
├── products/
│   └── (optional: manual JSON/YAML files)
├── team/
│   └── (optional: manual JSON/YAML files)
├── generate_sitemaps.py
└── README.md
```

### 1.2 Create Directories

Run these commands in your repository root:

```bash
# Create required directories
mkdir -p .github/workflows
mkdir -p ai-generators
mkdir -p data
mkdir -p schema-files
mkdir -p sitemaps
mkdir -p locations
mkdir -p products
mkdir -p team

# Verify structure
tree -d . || ls -la
```

## Step 2: Deploy Files to Repository

### 2.1 Copy Workflow Files

Copy the GitHub Actions workflow files to `.github/workflows/`:

**File: `.github/workflows/auto-refresh.yml`**
```yaml
name: Auto Refresh AI Files

on:
  schedule:
    - cron: "0 4 * * 0"   # Every Sunday at 04:00 UTC
  workflow_dispatch:    # Allow manual run from the Actions tab

permissions:
  contents: write

jobs:
  refresh:
    runs-on: ubuntu-latest
    steps:
    - name: Checkout
      uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: "3.11"

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r ai-generators/requirements.txt

    - name: Re-generate files
      env:
        SITE_BASE_URL: "${{ vars.SITE_BASE_URL }}"
      run: |
        python ai-generators/generate_files_xlsx.py

    - name: Commit refreshed files
      run: |
        git config user.name "github-actions[bot]"
        git config user.email "github-actions[bot]@users.noreply.github.com"
        git add -A
        git commit -m "Automated refresh of generated AI files" || echo "No changes"
        git push

    - name: Ping search engines
      if: github.ref == 'refs/heads/main'
      run: |
        curl "http://www.google.com/ping?sitemap=${{ vars.SITE_BASE_URL }}/ai-sitemap.xml" || echo "Google ping failed"
        curl "https://www.bing.com/ping?sitemap=${{ vars.SITE_BASE_URL }}/ai-sitemap.xml" || echo "Bing ping failed"
```

**File: `.github/workflows/build_ai_files_and_ping_xlsx.yml`**
```yaml
name: Build AI files from XLSX and ping sitemap

on:
  push:
    branches: [ main ]
    paths: [ 'data/client-data.xlsx' ]
  workflow_dispatch:
  schedule:
    - cron: '0 3 * * 0'   # Every Sunday at 03:00 UTC

permissions:
  contents: write

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.11'

    - name: Install dependencies
      run: pip install -r ai-generators/requirements.txt

    - name: Generate files and sitemap
      env:
        SITE_BASE_URL: "${{ vars.SITE_BASE_URL }}"
      run: |
        python ai-generators/generate_files_xlsx.py

    - name: Commit changes
      run: |
        git config --global user.name 'github-actions[bot]'
        git config --global user.email 'github-actions[bot]@users.noreply.github.com'
        git add .
        git commit -m "Update generated AI files from XLSX data" || echo "No changes"
        git push
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

    - name: Ping search engines
      if: github.ref == 'refs/heads/main'
      run: |
        curl "http://www.google.com/ping?sitemap=${{ vars.SITE_BASE_URL }}/ai-sitemap.xml" || echo "Google ping failed"
        curl "https://www.bing.com/ping?sitemap=${{ vars.SITE_BASE_URL }}/ai-sitemap.xml" || echo "Bing ping failed"
```

**File: `.github/workflows/sitemap.yml`**
```yaml
name: Generate Sitemaps

on:
  push:
    branches: [ "main" ]
  workflow_dispatch:

permissions:
  contents: write

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - name: Checkout repo
      uses: actions/checkout@v4
      with:
        fetch-depth: 0

    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.x'

    - name: Install dependencies
      run: pip install pandas openpyxl

    - name: Generate sitemaps
      run: |
        python generate_sitemaps.py || true

    - name: Show report
      run: |
        echo "---- SITEMAP GENERATION REPORT ----"
        if [ -f sitemaps/_report.txt ]; then
          cat sitemaps/_report.txt
        else
          echo "No report file found."
        fi

    - name: Commit and push sitemap changes
      run: |
        git config --global user.name "github-actions"
        git config --global user.email "actions@github.com"
        git pull --rebase
        git add sitemaps/*.xml sitemaps/_report.txt || true
        if git diff --cached --quiet; then
          echo "No changes to commit"
        else
          git commit -m "Auto-update sitemaps"
          git push
        fi

    - name: Upload artifact
      if: always()
      uses: actions/upload-artifact@v4
      with:
        name: sitemaps-output
        path: |
          sitemaps/*.xml
          sitemaps/_report.txt
        if-no-files-found: warn
```

### 2.2 Copy Python Scripts

**File: `ai-generators/generate_files_xlsx.py`**

Copy the entire content of the `generate_files_xlsx.py` file to this location, but modify the configuration section at the top:

```python
# ==== CONFIG ====
DATA_FILE = "../data/client-data.xlsx"  # Note: relative to ai-generators/ directory
OUTPUT_DIR = "../schema-files"
SITE_BASE = os.environ.get("SITE_BASE_URL", "https://yourdomain.com")  # Use environment variable
SITEMAP_FILE = "../ai-sitemap.xml"
# ====
```

**File: `ai-generators/requirements.txt`**
```txt
# requirements.txt

# This file lists the Python dependencies needed to run the AI Visibility
# generator for multi‑sheet Excel workbooks.  It is read by the GitHub
# Actions workflow before running the generator script.

# Pandas is used to read and manipulate dataframes from the Excel workbook.
pandas>=2.0

# PyYAML is required to write YAML files.
PyYAML>=6.0

# openpyxl is required by pandas to read .xlsx files.
openpyxl>=3.1

# Additional dependencies for XML handling
lxml>=4.9
```

**File: `generate_sitemaps.py`**

Copy the entire content of the `generate_sitemaps.py` file to the repository root.

### 2.3 Add Sample Data File

**File: `data/client-data.xlsx`**

Place your initial Excel file here. If you don't have one yet, create a simple Excel file with these columns:

| client_name | website | category | tagline | description | business_hours | year_founded | number_of_employees | address | phone | email |
|-------------|---------|----------|---------|-------------|----------------|--------------|-------------------|---------|-------|-------|
| Sample Client | https://example.com | Technology | Innovation at Scale | Leading tech company | 9AM-5PM | 2010 | 50 | 123 Main St | 555-0123 | contact@sample.com |

## Step 3: Configure Repository Settings

### 3.1 Set Repository Variables

Repository variables are used for configuration that can be public.

1. **Navigate to Repository Settings**:
   - Go to your GitHub repository
   - Click "Settings" tab
   - Click "Secrets and variables" → "Actions"
   - Click "Variables" tab

2. **Add Required Variables**:

   **Variable: `SITE_BASE_URL`**
   ```
   Name: SITE_BASE_URL
   Value: https://yourdomain.com
   ```
   
   Replace with your actual domain where the files will be hosted.

   **Example Values**:
   ```
   For GitHub Pages: https://username.github.io/repository-name
   For custom domain: https://www.yourclientdomain.com
   For subdomain: https://client.youragency.com
   ```

### 3.2 Set Repository Secrets (if needed)

Currently, no additional secrets are required beyond the default `GITHUB_TOKEN` that GitHub provides automatically. However, if you need additional API access:

1. **Navigate to Secrets**:
   - Go to "Secrets and variables" → "Actions"
   - Click "Secrets" tab

2. **Add secrets as needed**:
   ```
   CUSTOM_API_KEY: (if integrating with external APIs)
   WEBHOOK_URL: (if sending notifications)
   ```

### 3.3 Configure Repository Permissions

1. **Enable GitHub Actions**:
   - Go to Settings → Actions → General
   - Ensure "Allow all actions and reusable workflows" is selected

2. **Set Workflow Permissions**:
   - Scroll to "Workflow permissions"
   - Select "Read and write permissions"
   - Check "Allow GitHub Actions to create and approve pull requests"

3. **Configure GitHub Pages** (if using):
   - Go to Settings → Pages
   - Set Source to "GitHub Actions"
   - Configure custom domain if needed

## Step 4: Initial Configuration

### 4.1 Customize the Generator Script

Edit `ai-generators/generate_files_xlsx.py` to match your needs:

1. **Update the configuration section**:
```python
# ==== CONFIG ====
DATA_FILE = "../data/client-data.xlsx"
OUTPUT_DIR = "../schema-files"
SITE_BASE = os.environ.get("SITE_BASE_URL", "https://your-actual-domain.com")
SITEMAP_FILE = "../ai-sitemap.xml"
# ====
```

2. **Customize file generation logic** (if needed):
   - Modify the `generate_files_from_row()` function
   - Add additional file formats
   - Change naming conventions
   - Add data validation

### 4.2 Update Sitemap Configuration

Edit `generate_sitemaps.py` if you need to customize:

1. **Domain validation**:
```python
# Add your domains to the placeholder detection
def is_placeholder_domain(domain: str) -> bool:
    low = domain.lower()
    return any(p in low for p in [
        "example.com", 
        "yourdomain.com", 
        "your-domain.com",
        "test.com",  # Add your test domains
        "staging.com"
    ])
```

2. **File scanning configuration**:
```python
# Customize which folders to scan
DEFAULT_FOLDERS = ["locations", "products", "team", "services"]  # Add more as needed
VALID_EXTS = {".json", ".yaml", ".yml", ".xml"}  # Add more extensions if needed
```

### 4.3 Test Configuration Files

Create a simple test to verify your configuration:

**File: `test_config.py`** (temporary, for testing)
```python
#!/usr/bin/env python3
import os
import sys
sys.path.append('ai-generators')

def test_imports():
    try:
        import pandas as pd
        import yaml
        import xml.etree.ElementTree as ET
        print("✓ All required imports successful")
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False

def test_file_paths():
    required_files = [
        "data/client-data.xlsx",
        "ai-generators/generate_files_xlsx.py", 
        "ai-generators/requirements.txt",
        "generate_sitemaps.py"
    ]
    
    missing = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing.append(file_path)
    
    if missing:
        print("✗ Missing required files:")
        for f in missing:
            print(f"  - {f}")
        return False
    else:
        print("✓ All required files present")
        return True

def test_directories():
    required_dirs = [
        ".github/workflows",
        "ai-generators", 
        "data",
        "schema-files",
        "sitemaps"
    ]
    
    missing = []
    for dir_path in required_dirs:
        if not os.path.exists(dir_path):
            missing.append(dir_path)
    
    if missing:
        print("✗ Missing required directories:")
        for d in missing:
            print(f"  - {d}")
        return False
    else:
        print("✓ All required directories present")
        return True

if __name__ == "__main__":
    print("Testing repository configuration...")
    tests = [test_imports, test_file_paths, test_directories]
    results = [test() for test in tests]
    
    if all(results):
        print("\n🎉 Configuration test passed! Repository is ready.")
    else:
        print("\n❌ Configuration test failed. Please fix the issues above.")
        sys.exit(1)
```

Run the test:
```bash
python test_config.py
```

## Step 5: Deploy and Commit Changes

### 5.1 Commit All Files

```bash
# Add all files
git add .

# Commit with descriptive message
git commit -m "Add GitHub workflow system for AI file generation

- Add GitHub Actions workflows for automated file generation
- Add Python scripts for Excel to structured data conversion  
- Add sitemap generation functionality
- Set up directory structure for generated files
- Configure environment variables and repository settings"

# Push to main branch
git push origin main
```

### 5.2 Verify Deployment

1. **Check Actions tab**:
   - Go to your repository → Actions tab
   - You should see the workflows listed
   - No errors should be displayed

2. **Verify file structure**:
```bash
# Check that all files are in place
ls -la .github/workflows/
ls -la ai-generators/
ls -la data/
```

## Step 6: Environment-Specific Configuration

### 6.1 Production Environment

For production deployments:

1. **Use production domain** in `SITE_BASE_URL`:
```
SITE_BASE_URL: https://www.clientdomain.com
```

2. **Configure production schedule**:
   - Adjust cron schedules in workflow files
   - Consider time zones for your client
   - Balance frequency vs. resource usage

3. **Set up monitoring**:
   - Enable GitHub Actions notifications
   - Set up external monitoring for the generated files
   - Configure alerts for failed workflows

### 6.2 Staging Environment

For staging/testing:

1. **Use staging domain**:
```
SITE_BASE_URL: https://staging.clientdomain.com
```

2. **More frequent updates** for testing:
```yaml
schedule:
  - cron: "*/30 * * * *"  # Every 30 minutes for testing
```

3. **Additional debugging**:
   - Add more verbose logging
   - Keep generated artifacts longer
   - Enable manual workflow triggers

### 6.3 Development Environment

For local development:

1. **Install dependencies locally**:
```bash
pip install -r ai-generators/requirements.txt
```

2. **Set environment variables**:
```bash
export SITE_BASE_URL="http://localhost:3000"
```

3. **Run scripts locally**:
```bash
cd ai-generators
python generate_files_xlsx.py

cd ..
python generate_sitemaps.py
```

## Step 7: Verify Deployment

### 7.1 Manual Workflow Trigger

1. **Go to Actions tab** in your repository
2. **Select "Build AI files from XLSX and ping sitemap"**
3. **Click "Run workflow"**
4. **Monitor execution** and check for errors

### 7.2 Check Generated Output

After successful execution:

1. **Verify generated files**:
```bash
ls -la schema-files/
ls -la sitemaps/
```

2. **Check sitemap content**:
```bash
cat ai-sitemap.xml
cat sitemaps/_report.txt
```

3. **Validate XML** (optional):
```bash
xmllint --noout ai-sitemap.xml && echo "✓ Valid XML"
```

### 7.3 Test Search Engine Pings

Check the Actions logs to see if search engines were successfully pinged:

```bash
# Look for these in the workflow logs:
# "Google ping successful" or "Google ping failed"  
# "Bing ping successful" or "Bing ping failed"
```

## Common Deployment Issues

### Issue: Workflow Permission Errors

**Symptom**: "Resource not accessible by integration" errors

**Solution**:
1. Check repository settings → Actions → General → Workflow permissions
2. Ensure "Read and write permissions" is selected
3. Enable "Allow GitHub Actions to create and approve pull requests"

### Issue: Python Import Errors

**Symptom**: "ModuleNotFoundError" in workflow logs

**Solution**:
1. Verify `requirements.txt` is in the correct location (`ai-generators/requirements.txt`)
2. Check that all required packages are listed with correct versions
3. Ensure the workflow installs dependencies with correct path

### Issue: File Path Errors

**Symptom**: "FileNotFoundError" for data files

**Solution**:
1. Verify file paths in the Python scripts are correct relative to execution directory
2. Check that `data/client-data.xlsx` exists and is committed to repository
3. Ensure directory structure matches expectations

### Issue: Environment Variable Not Set

**Symptom**: Using default "https://yourdomain.com" in generated files

**Solution**:
1. Go to repository Settings → Secrets and variables → Actions → Variables
2. Add `SITE_BASE_URL` variable with your actual domain
3. Re-run the workflow

## Next Steps

After successful deployment:

1. **Set up Google Sheets integration** (if not done already)
2. **Configure monitoring and alerting**
3. **Train your team** on the workflow
4. **Set up testing procedures** for ongoing maintenance
5. **Document client-specific customizations**

---

**📋 Deployment Checklist**

Use this checklist to ensure complete deployment:

- [ ] Repository directory structure created
- [ ] All workflow files copied to `.github/workflows/`
- [ ] Python scripts placed in `ai-generators/`
- [ ] `requirements.txt` configured with correct dependencies
- [ ] `generate_sitemaps.py` placed in repository root
- [ ] Sample `client-data.xlsx` added to `data/` directory
- [ ] Repository variables configured (`SITE_BASE_URL`)
- [ ] Repository permissions set for GitHub Actions
- [ ] All files committed and pushed to main branch
- [ ] Manual workflow test completed successfully
- [ ] Generated files verified in repository
- [ ] Search engine pings tested (check logs)
- [ ] Documentation updated with client-specific details

**🔧 Repository Settings Summary**

For quick reference:

```
Repository Variables:
└── SITE_BASE_URL: https://your-actual-domain.com

Repository Permissions:
├── Actions: Enabled
├── Workflow permissions: Read and write permissions  
└── Allow GitHub Actions to create PRs: Enabled

Required Files:
├── .github/workflows/*.yml (3 files)
├── ai-generators/generate_files_xlsx.py
├── ai-generators/requirements.txt
├── data/client-data.xlsx
└── generate_sitemaps.py
```
