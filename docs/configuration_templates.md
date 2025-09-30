# Configuration Templates and Examples

## Overview

This document provides ready-to-use configuration templates, examples, and reference materials for setting up the GitHub workflow system. Copy and customize these templates for your specific deployment needs.

## Environment Variables Templates

### Repository Variables Configuration

**Location**: GitHub Repository → Settings → Secrets and variables → Actions → Variables

```bash
# Primary configuration
SITE_BASE_URL=https://your-domain.com

# Development/Staging variants
SITE_BASE_URL=https://staging.your-domain.com
SITE_BASE_URL=https://your-username.github.io/repository-name
SITE_BASE_URL=https://subdomain.your-agency.com

# Local development
SITE_BASE_URL=http://localhost:3000
```

### Environment Variables for Different Deployment Types

#### Production Environment
```bash
SITE_BASE_URL=https://www.clientdomain.com
ENVIRONMENT=production
LOG_LEVEL=error
ENABLE_SEARCH_PING=true
```

#### Staging Environment
```bash
SITE_BASE_URL=https://staging.clientdomain.com
ENVIRONMENT=staging
LOG_LEVEL=debug
ENABLE_SEARCH_PING=false
```

#### Development Environment
```bash
SITE_BASE_URL=http://localhost:8080
ENVIRONMENT=development
LOG_LEVEL=debug
ENABLE_SEARCH_PING=false
DEBUG_MODE=true
```

## GitHub Repository Settings Templates

### Required Repository Settings Checklist

**Actions Settings** (`Settings → Actions → General`):
```
✓ Actions permissions: "Allow all actions and reusable workflows"
✓ Workflow permissions: "Read and write permissions" 
✓ Allow GitHub Actions to create and approve pull requests: Enabled
✓ Fork pull request workflows: "Require approval for first-time contributors"
```

### Branch Protection Rules Template

**Branch**: `main`

```yaml
# Protection settings for main branch
Restrict pushes that create files: ❌ Disabled
Require a pull request before merging: ❌ Disabled (for automated commits)
Require status checks to pass before merging: ✅ Enabled
  - Required status checks:
    - "build / build"
Require conversation resolution before merging: ❌ Disabled
Restrict pushes that create files: ❌ Disabled
Allow force pushes: ❌ Disabled
Allow deletions: ❌ Disabled
```

### Repository Secrets Template

**Note**: Most setups only need repository variables, not secrets.

```bash
# Only if integrating with external APIs
EXTERNAL_API_KEY=your_api_key_here
WEBHOOK_URL=https://hooks.slack.com/services/...
NOTIFICATION_EMAIL=alerts@yourdomain.com

# Custom GitHub token (only if default GITHUB_TOKEN insufficient)
CUSTOM_GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

## File Configuration Templates

### 1. Enhanced Python Generator Script Template

**File**: `ai-generators/generate_files_xlsx_enhanced.py`

```python
#!/usr/bin/env python3
"""
Enhanced file generator with configuration options and better error handling.
This version includes more customization options and robust error handling.
"""

import os
import json
import yaml
import pandas as pd
import datetime
import xml.etree.ElementTree as ET
import logging
from pathlib import Path
from typing import Dict, Any, Optional

# ==== CONFIGURATION ====
class Config:
    # File paths
    DATA_FILE = os.environ.get("DATA_FILE", "../data/client-data.xlsx")
    OUTPUT_DIR = os.environ.get("OUTPUT_DIR", "../schema-files")
    SITEMAP_FILE = os.environ.get("SITEMAP_FILE", "../ai-sitemap.xml")
    
    # Site configuration
    SITE_BASE = os.environ.get("SITE_BASE_URL", "https://yourdomain.com")
    ENVIRONMENT = os.environ.get("ENVIRONMENT", "production")
    
    # Feature flags
    GENERATE_JSON = os.environ.get("GENERATE_JSON", "true").lower() == "true"
    GENERATE_YAML = os.environ.get("GENERATE_YAML", "true").lower() == "true"
    GENERATE_MD = os.environ.get("GENERATE_MD", "true").lower() == "true"
    GENERATE_LLM = os.environ.get("GENERATE_LLM", "true").lower() == "true"
    GENERATE_SITEMAP = os.environ.get("GENERATE_SITEMAP", "true").lower() == "true"
    
    # Data processing options
    FILTER_EMPTY_FIELDS = os.environ.get("FILTER_EMPTY_FIELDS", "true").lower() == "true"
    MIN_FIELDS_REQUIRED = int(os.environ.get("MIN_FIELDS_REQUIRED", "2"))
    SLUG_FROM_FIELD = os.environ.get("SLUG_FROM_FIELD", "slug,client_name,name")
    
    # Logging
    LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO").upper()

# ==== LOGGING SETUP ====
logging.basicConfig(
    level=getattr(logging, Config.LOG_LEVEL),
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# ==== UTILITY FUNCTIONS ====
def ensure_output_dir():
    """Create output directory if it doesn't exist."""
    Path(Config.OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
    logger.info(f"Output directory ensured: {Config.OUTPUT_DIR}")

def load_client_data(file_path: str) -> pd.DataFrame:
    """Load client data from Excel file with error handling."""
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Data file not found: {file_path}")
        
        df = pd.read_excel(file_path)
        logger.info(f"Loaded {len(df)} rows from {file_path}")
        return df
    
    except Exception as e:
        logger.error(f"Failed to load data file {file_path}: {e}")
        raise

def get_slug_from_row(row: pd.Series) -> str:
    """Generate slug from row data based on configuration."""
    slug_fields = Config.SLUG_FROM_FIELD.split(",")
    
    for field in slug_fields:
        field = field.strip()
        if field in row and pd.notna(row[field]):
            slug = str(row[field]).lower()
            slug = "".join(c if c.isalnum() else "_" for c in slug)
            slug = "_".join(part for part in slug.split("_") if part)
            return slug
    
    # Fallback to row index
    return f"client_{row.name}"

def filter_row_data(row: pd.Series) -> Dict[str, Any]:
    """Filter and clean row data based on configuration."""
    if not Config.FILTER_EMPTY_FIELDS:
        return row.to_dict()
    
    # Filter out empty/NaN/blank values
    filtered = {}
    for key, value in row.to_dict().items():
        if pd.notna(value):
            str_value = str(value).strip()
            if str_value and str_value.lower() != 'nan':
                filtered[key] = value
    
    return filtered

# ==== FILE GENERATION FUNCTIONS ====
def save_json(data: Dict[str, Any], path: str) -> bool:
    """Save data as JSON file."""
    if not Config.GENERATE_JSON or not data:
        return False
    
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False, default=str)
        logger.debug(f"Saved JSON: {path}")
        return True
    except Exception as e:
        logger.error(f"Failed to save JSON {path}: {e}")
        return False

def save_yaml(data: Dict[str, Any], path: str) -> bool:
    """Save data as YAML file."""
    if not Config.GENERATE_YAML or not data:
        return False
    
    try:
        with open(path, "w", encoding="utf-8") as f:
            yaml.dump(data, f, allow_unicode=True, default_flow_style=False)
        logger.debug(f"Saved YAML: {path}")
        return True
    except Exception as e:
        logger.error(f"Failed to save YAML {path}: {e}")
        return False

def save_md(content: str, path: str) -> bool:
    """Save content as Markdown file."""
    if not Config.GENERATE_MD or not content.strip():
        return False
    
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        logger.debug(f"Saved MD: {path}")
        return True
    except Exception as e:
        logger.error(f"Failed to save MD {path}: {e}")
        return False

def save_llm(content: str, path: str) -> bool:
    """Save content as LLM text file."""
    if not Config.GENERATE_LLM or not content.strip():
        return False
    
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        logger.debug(f"Saved LLM: {path}")
        return True
    except Exception as e:
        logger.error(f"Failed to save LLM {path}: {e}")
        return False

def generate_markdown_content(data: Dict[str, Any], title: str) -> str:
    """Generate markdown content from data."""
    content = f"# {title}\n\n"
    
    # Add metadata
    content += f"*Generated on {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n"
    
    # Add data fields
    for key, value in data.items():
        formatted_key = key.replace("_", " ").title()
        content += f"**{formatted_key}:** {value}\n\n"
    
    return content

def generate_llm_content(data: Dict[str, Any], title: str) -> str:
    """Generate LLM-friendly text content from data."""
    content = f"LLM Data for {title}\n"
    content += "=" * (len(title) + 13) + "\n\n"
    
    for key, value in data.items():
        content += f"{key}: {value}\n"
    
    content += f"\nGenerated: {datetime.datetime.now().isoformat()}\n"
    return content

def generate_files_from_row(row: pd.Series) -> bool:
    """Generate all file formats for a single row."""
    try:
        # Get slug for directory/file naming
        slug = get_slug_from_row(row)
        
        # Filter data
        row_data = filter_row_data(row)
        
        # Check minimum requirements
        if len(row_data) < Config.MIN_FIELDS_REQUIRED:
            logger.warning(f"Skipping {slug}: insufficient data ({len(row_data)} fields)")
            return False
        
        # Create directory
        base_path = Path(Config.OUTPUT_DIR) / slug
        base_path.mkdir(parents=True, exist_ok=True)
        
        # Generate title
        title = row_data.get('client_name') or row_data.get('name') or slug
        
        # Save files
        files_created = 0
        
        if save_json(row_data, base_path / f"{slug}.json"):
            files_created += 1
        
        if save_yaml(row_data, base_path / f"{slug}.yaml"):
            files_created += 1
        
        if save_md(generate_markdown_content(row_data, title), base_path / f"{slug}.md"):
            files_created += 1
        
        if save_llm(generate_llm_content(row_data, title), base_path / f"{slug}.llm"):
            files_created += 1
        
        logger.info(f"Generated {files_created} files for {slug}")
        return files_created > 0
    
    except Exception as e:
        logger.error(f"Failed to generate files for row: {e}")
        return False

def generate_all_files() -> int:
    """Generate files for all rows in the data."""
    ensure_output_dir()
    
    try:
        df = load_client_data(Config.DATA_FILE)
        successful = 0
        
        logger.info(f"Processing {len(df)} rows...")
        
        for i, (_, row) in enumerate(df.iterrows()):
            if generate_files_from_row(row):
                successful += 1
            
            # Progress logging
            if (i + 1) % 10 == 0:
                logger.info(f"Processed {i + 1}/{len(df)} rows ({successful} successful)")
        
        logger.info(f"File generation complete: {successful}/{len(df)} successful")
        return successful
    
    except Exception as e:
        logger.error(f"File generation failed: {e}")
        return 0

def generate_sitemap(root_dir: str = None, output_file: str = None) -> bool:
    """Generate XML sitemap for all generated files."""
    if not Config.GENERATE_SITEMAP:
        logger.info("Sitemap generation disabled")
        return True
    
    root_dir = root_dir or Config.OUTPUT_DIR
    output_file = output_file or Config.SITEMAP_FILE
    
    try:
        urlset = ET.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
        url_count = 0
        
        for file_path in Path(root_dir).rglob("*"):
            if not file_path.is_file():
                continue
            
            if file_path.suffix.lower() not in {".json", ".yaml", ".yml", ".md", ".llm"}:
                continue
            
            if file_path.stat().st_size == 0:
                continue
            
            rel_path = file_path.relative_to(root_dir).as_posix()
            url = f"{Config.SITE_BASE.rstrip('/')}/{rel_path}"
            
            url_el = ET.SubElement(urlset, "url")
            ET.SubElement(url_el, "loc").text = url
            ET.SubElement(url_el, "lastmod").text = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
            
            url_count += 1
        
        tree = ET.ElementTree(urlset)
        ET.indent(tree, space="  ")
        tree.write(output_file, encoding="utf-8", xml_declaration=True)
        
        logger.info(f"Sitemap generated with {url_count} URLs: {output_file}")
        return True
    
    except Exception as e:
        logger.error(f"Sitemap generation failed: {e}")
        return False

def main():
    """Main execution function."""
    logger.info("Starting enhanced file generation")
    logger.info(f"Configuration: {Config.ENVIRONMENT} environment")
    logger.info(f"Site base: {Config.SITE_BASE}")
    
    try:
        # Generate files
        files_generated = generate_all_files()
        
        if files_generated == 0:
            logger.error("No files were generated")
            return 1
        
        # Generate sitemap
        if not generate_sitemap():
            logger.warning("Sitemap generation failed")
        
        logger.info("File generation completed successfully")
        return 0
    
    except Exception as e:
        logger.error(f"Process failed: {e}")
        return 1

if __name__ == "__main__":
    exit(main())
```

### 2. Advanced Sitemap Generator Template

**File**: `generate_sitemaps_advanced.py`

```python
#!/usr/bin/env python3
"""
Advanced sitemap generator with multiple sitemap support and configuration options.
Supports sitemap index files and advanced filtering.
"""

import os
import sys
import json
import traceback
from pathlib import Path
from datetime import datetime, timezone
from typing import List, Dict, Set, Optional
import pandas as pd
import xml.etree.ElementTree as ET

# ==== CONFIGURATION ====
class SitemapConfig:
    # Data source
    EXCEL_FILE = os.environ.get("EXCEL_FILE", "client-data.xlsx")
    
    # Output settings
    SITEMAPS_DIR = os.environ.get("SITEMAPS_DIR", "sitemaps")
    SITEMAP_INDEX_FILE = os.environ.get("SITEMAP_INDEX_FILE", "sitemap-index.xml")
    
    # Domain settings
    DOMAIN_COLUMNS = os.environ.get("DOMAIN_COLUMNS", "domain,site_url,website,base_url,url").split(",")
    CLIENT_COLUMNS = os.environ.get("CLIENT_COLUMNS", "client_name,name,client,brand").split(",")
    
    # File scanning
    DEFAULT_FOLDERS = os.environ.get("DEFAULT_FOLDERS", "locations,products,team,schema-files").split(",")
    VALID_EXTENSIONS = set(os.environ.get("VALID_EXTENSIONS", ".json,.yaml,.yml,.md,.xml").split(","))
    
    # Filtering
    PLACEHOLDER_DOMAINS = os.environ.get("PLACEHOLDER_DOMAINS", "example.com,yourdomain.com,your-domain.com,test.com").split(",")
    MIN_URLS_PER_SITEMAP = int(os.environ.get("MIN_URLS_PER_SITEMAP", "1"))
    MAX_URLS_PER_SITEMAP = int(os.environ.get("MAX_URLS_PER_SITEMAP", "50000"))
    
    # Features
    GENERATE_INDEX = os.environ.get("GENERATE_INDEX", "true").lower() == "true"
    INCLUDE_LASTMOD = os.environ.get("INCLUDE_LASTMOD", "true").lower() == "true"
    VALIDATE_URLS = os.environ.get("VALIDATE_URLS", "true").lower() == "true"

def log(message: str, level: str = "INFO"):
    """Simple logging function."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {level}: {message}")

def ensure_https(url: str) -> str:
    """Ensure URL has https scheme."""
    url = url.strip()
    if not url:
        return url
    if not (url.startswith("http://") or url.startswith("https://")):
        url = "https://" + url
    return url.rstrip("/")

def is_placeholder_domain(domain: str) -> bool:
    """Check if domain is a placeholder that should be filtered out."""
    domain_lower = domain.lower()
    return any(placeholder in domain_lower for placeholder in SitemapConfig.PLACEHOLDER_DOMAINS)

def get_file_lastmod(file_path: Path) -> str:
    """Get file modification time in ISO format."""
    try:
        mtime = file_path.stat().st_mtime
        dt = datetime.fromtimestamp(mtime, tz=timezone.utc)
        return dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    except Exception:
        return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def find_files_for_client(client_data: Dict) -> List[Path]:
    """Find files associated with a client."""
    files = []
    
    # Check for explicit file columns
    file_columns = [col for col in client_data.keys() if 'file' in col.lower() or 'path' in col.lower()]
    
    for col in file_columns:
        if pd.notna(client_data[col]):
            # Handle comma/semicolon separated lists
            paths = str(client_data[col]).replace(';', ',').split(',')
            for path_str in paths:
                path = Path(path_str.strip())
                if path.exists() and path.is_file() and path.suffix.lower() in SitemapConfig.VALID_EXTENSIONS:
                    files.append(path)
    
    # Auto-scan default folders if no explicit files
    if not files:
        client_name = str(client_data.get('client_name', client_data.get('name', 'unknown'))).lower()
        client_slug = "".join(c if c.isalnum() else "_" for c in client_name)
        
        for folder in SitemapConfig.DEFAULT_FOLDERS:
            folder_path = Path(folder)
            if folder_path.exists():
                # Look for client-specific subdirectory
                client_dir = folder_path / client_slug
                if client_dir.exists():
                    for file_path in client_dir.rglob("*"):
                        if (file_path.is_file() and 
                            file_path.suffix.lower() in SitemapConfig.VALID_EXTENSIONS and 
                            file_path.stat().st_size > 0):
                            files.append(file_path)
    
    # Remove duplicates while preserving order
    seen = set()
    unique_files = []
    for file_path in files:
        file_str = str(file_path)
        if file_str not in seen:
            seen.add(file_str)
            unique_files.append(file_path)
    
    return unique_files

def create_sitemap(client_data: Dict, files: List[Path], output_path: Path) -> int:
    """Create sitemap XML file for a client."""
    domain = client_data['domain']
    
    # Create XML structure
    urlset = ET.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
    
    url_count = 0
    for file_path in files:
        if url_count >= SitemapConfig.MAX_URLS_PER_SITEMAP:
            log(f"Warning: Reached maximum URLs per sitemap ({SitemapConfig.MAX_URLS_PER_SITEMAP})")
            break
        
        # Create URL element
        url_elem = ET.SubElement(urlset, "url")
        
        # Add location
        relative_path = file_path.as_posix()
        if relative_path.startswith('./'):
            relative_path = relative_path[2:]
        
        url = f"{domain}/{relative_path}"
        ET.SubElement(url_elem, "loc").text = url
        
        # Add last modified date if enabled
        if SitemapConfig.INCLUDE_LASTMOD:
            lastmod = get_file_lastmod(file_path)
            ET.SubElement(url_elem, "lastmod").text = lastmod
        
        url_count += 1
    
    # Only create sitemap if it meets minimum requirements
    if url_count < SitemapConfig.MIN_URLS_PER_SITEMAP:
        log(f"Skipping sitemap for {domain}: only {url_count} URLs (minimum: {SitemapConfig.MIN_URLS_PER_SITEMAP})")
        return 0
    
    # Write XML file
    tree = ET.ElementTree(urlset)
    ET.indent(tree, space="  ")
    tree.write(output_path, encoding="utf-8", xml_declaration=True)
    
    return url_count

def create_sitemap_index(sitemap_files: List[Path], output_path: Path) -> bool:
    """Create sitemap index file."""
    if not SitemapConfig.GENERATE_INDEX or not sitemap_files:
        return False
    
    # Create XML structure
    sitemapindex = ET.Element("sitemapindex", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
    
    for sitemap_file in sitemap_files:
        sitemap_elem = ET.SubElement(sitemapindex, "sitemap")
        
        # Use the first domain from sitemaps as base (or could be configured)
        sitemap_url = f"https://example.com/sitemaps/{sitemap_file.name}"  # TODO: Make configurable
        ET.SubElement(sitemap_elem, "loc").text = sitemap_url
        
        if SitemapConfig.INCLUDE_LASTMOD:
            lastmod = get_file_lastmod(sitemap_file)
            ET.SubElement(sitemap_elem, "lastmod").text = lastmod
    
    # Write index file
    tree = ET.ElementTree(sitemapindex)
    ET.indent(tree, space="  ")
    tree.write(output_path, encoding="utf-8", xml_declaration=True)
    
    return True

def main():
    """Main execution function."""
    report = []
    
    try:
        # Check for Excel file
        excel_path = Path(SitemapConfig.EXCEL_FILE)
        if not excel_path.exists():
            raise FileNotFoundError(f"Excel file not found: {excel_path}")
        
        # Load data
        try:
            df = pd.read_excel(excel_path)
            log(f"Loaded {len(df)} rows from {excel_path}")
        except Exception as e:
            raise RuntimeError(f"Failed to read Excel file: {e}")
        
        # Find domain column
        domain_col = None
        for col in SitemapConfig.DOMAIN_COLUMNS:
            if col in df.columns:
                domain_col = col
                break
        
        if not domain_col:
            raise KeyError(f"No domain column found. Expected one of: {SitemapConfig.DOMAIN_COLUMNS}")
        
        # Find client name column
        client_col = None
        for col in SitemapConfig.CLIENT_COLUMNS:
            if col in df.columns:
                client_col = col
                break
        client_col = client_col or domain_col
        
        # Create output directory
        sitemaps_dir = Path(SitemapConfig.SITEMAPS_DIR)
        sitemaps_dir.mkdir(parents=True, exist_ok=True)
        
        # Process each row
        sitemap_files = []
        total_urls = 0
        
        for i, row in df.iterrows():
            raw_domain = str(row.get(domain_col, "")).strip()
            if not raw_domain or raw_domain.lower() == 'nan':
                report.append(f"Row {i+1}: Skipped - empty domain")
                continue
            
            domain = ensure_https(raw_domain)
            if is_placeholder_domain(domain):
                report.append(f"Row {i+1}: Skipped - placeholder domain: {domain}")
                continue
            
            client_name = str(row.get(client_col, f"client_{i+1}")).strip()
            client_slug = "".join(c if c.isalnum() else "_" for c in client_name.lower())
            
            # Find files for this client
            client_data = {'domain': domain, **row.to_dict()}
            files = find_files_for_client(client_data)
            
            if not files:
                report.append(f"Row {i+1}: Warning - no files found for {client_name}")
                # Still create empty sitemap for consistency
            
            # Create sitemap
            sitemap_filename = f"{client_slug}_sitemap.xml"
            sitemap_path = sitemaps_dir / sitemap_filename
            
            urls_added = create_sitemap(client_data, files, sitemap_path)
            
            if urls_added > 0:
                sitemap_files.append(sitemap_path)
                total_urls += urls_added
                report.append(f"Row {i+1}: Created {sitemap_filename} with {urls_added} URLs for {domain}")
            else:
                report.append(f"Row {i+1}: Created empty {sitemap_filename} for {domain}")
        
        # Create sitemap index
        if sitemap_files and SitemapConfig.GENERATE_INDEX:
            index_path = sitemaps_dir / SitemapConfig.SITEMAP_INDEX_FILE
            if create_sitemap_index(sitemap_files, index_path):
                report.append(f"Created sitemap index with {len(sitemap_files)} sitemaps")
        
        report.append(f"Completed: {len(sitemap_files)} sitemaps, {total_urls} total URLs")
        log("Sitemap generation completed successfully")
    
    except Exception as e:
        error_msg = f"ERROR: {str(e)}"
        report.append(error_msg)
        report.append(f"TRACEBACK:\n{traceback.format_exc()}")
        log(error_msg, "ERROR")
    
    # Write report
    report_path = Path(SitemapConfig.SITEMAPS_DIR) / "_report.txt"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(report), encoding="utf-8")
    
    # Print report
    print("\n".join(report))

if __name__ == "__main__":
    main()
```

### 3. Custom Workflow Templates

#### Multi-Environment Workflow Template

**File**: `.github/workflows/multi-environment.yml`

```yaml
name: Multi-Environment Deployment

on:
  push:
    branches: 
      - main
      - staging
      - develop
    paths: 
      - 'data/client-data.xlsx'
  workflow_dispatch:
    inputs:
      environment:
        description: 'Target environment'
        required: true
        default: 'staging'
        type: choice
        options:
        - development
        - staging
        - production

permissions:
  contents: write

jobs:
  determine-environment:
    runs-on: ubuntu-latest
    outputs:
      environment: ${{ steps.set-env.outputs.environment }}
      site-url: ${{ steps.set-env.outputs.site-url }}
    steps:
    - name: Determine environment
      id: set-env
      run: |
        if [ "${{ github.event_name }}" = "workflow_dispatch" ]; then
          ENV="${{ github.event.inputs.environment }}"
        elif [ "${{ github.ref }}" = "refs/heads/main" ]; then
          ENV="production"
        elif [ "${{ github.ref }}" = "refs/heads/staging" ]; then
          ENV="staging" 
        else
          ENV="development"
        fi
        
        echo "environment=$ENV" >> $GITHUB_OUTPUT
        
        case $ENV in
          production)
            echo "site-url=${{ vars.PRODUCTION_SITE_URL }}" >> $GITHUB_OUTPUT
            ;;
          staging)
            echo "site-url=${{ vars.STAGING_SITE_URL }}" >> $GITHUB_OUTPUT
            ;;
          *)
            echo "site-url=${{ vars.DEVELOPMENT_SITE_URL }}" >> $GITHUB_OUTPUT
            ;;
        esac

  build-and-deploy:
    needs: determine-environment
    runs-on: ubuntu-latest
    environment: ${{ needs.determine-environment.outputs.environment }}
    
    steps:
    - name: Checkout
      uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.11'

    - name: Cache dependencies
      uses: actions/cache@v4
      with:
        path: ~/.cache/pip
        key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r ai-generators/requirements.txt

    - name: Generate files
      env:
        SITE_BASE_URL: ${{ needs.determine-environment.outputs.site-url }}
        ENVIRONMENT: ${{ needs.determine-environment.outputs.environment }}
        LOG_LEVEL: ${{ needs.determine-environment.outputs.environment == 'production' && 'INFO' || 'DEBUG' }}
      run: |
        echo "Generating files for $ENVIRONMENT environment"
        echo "Site URL: $SITE_BASE_URL"
        python ai-generators/generate_files_xlsx.py

    - name: Generate sitemaps
      run: |
        python generate_sitemaps.py

    - name: Validate output
      if: needs.determine-environment.outputs.environment != 'production'
      run: |
        # Run validation in non-production environments
        python -c "
        import xml.etree.ElementTree as ET
        import os
        
        # Validate XML files
        for root, dirs, files in os.walk('sitemaps'):
            for file in files:
                if file.endswith('.xml'):
                    try:
                        ET.parse(os.path.join(root, file))
                        print(f'✓ Valid XML: {file}')
                    except ET.ParseError as e:
                        print(f'✗ Invalid XML: {file} - {e}')
                        exit(1)
        "

    - name: Commit changes
      run: |
        git config --global user.name 'github-actions[bot]'
        git config --global user.email 'github-actions[bot]@users.noreply.github.com'
        git add .
        if git diff --cached --quiet; then
          echo "No changes to commit"
        else
          git commit -m "Deploy to ${{ needs.determine-environment.outputs.environment }} environment"
          git push
        fi

    - name: Notify search engines
      if: needs.determine-environment.outputs.environment == 'production'
      run: |
        SITEMAP_URL="${{ needs.determine-environment.outputs.site-url }}/ai-sitemap.xml"
        echo "Notifying search engines about $SITEMAP_URL"
        
        curl -f -m 30 "http://www.google.com/ping?sitemap=$SITEMAP_URL" || echo "Google ping failed (normal)"
        curl -f -m 30 "https://www.bing.com/ping?sitemap=$SITEMAP_URL" || echo "Bing ping failed (normal)"

    - name: Upload artifacts
      uses: actions/upload-artifact@v4
      with:
        name: generated-files-${{ needs.determine-environment.outputs.environment }}
        path: |
          schema-files/
          sitemaps/
          ai-sitemap.xml
        retention-days: ${{ needs.determine-environment.outputs.environment == 'production' && 30 || 7 }}
```

#### Quality Assurance Workflow Template

**File**: `.github/workflows/quality-assurance.yml`

```yaml
name: Quality Assurance

on:
  pull_request:
    paths:
      - 'data/**'
      - 'ai-generators/**'
      - '*.py'
  push:
    branches: [ main ]
  schedule:
    - cron: '0 6 * * 1'  # Weekly on Monday

jobs:
  data-validation:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        pip install pandas openpyxl pyyaml lxml
    
    - name: Validate Excel data
      run: |
        python -c "
        import pandas as pd
        import sys
        
        try:
            df = pd.read_excel('data/client-data.xlsx')
            print(f'✓ Excel file loaded: {df.shape}')
            
            # Check for required columns
            required_cols = ['client_name', 'website']
            missing_cols = [col for col in required_cols if col not in df.columns]
            if missing_cols:
                print(f'✗ Missing required columns: {missing_cols}')
                sys.exit(1)
            
            # Check for empty data
            if len(df) == 0:
                print('✗ No data rows found')
                sys.exit(1)
            
            # Check for placeholder domains
            if 'website' in df.columns:
                placeholders = df[df['website'].str.contains('example.com|yourdomain.com', na=False, regex=True)]
                if len(placeholders) > 0:
                    print(f'⚠️ Warning: {len(placeholders)} placeholder domains found')
                    for idx, row in placeholders.iterrows():
                        print(f'  Row {idx}: {row.get(\"client_name\", \"unknown\")} - {row.get(\"website\", \"unknown\")}')
            
            print('✓ Data validation passed')
            
        except Exception as e:
            print(f'✗ Data validation failed: {e}')
            sys.exit(1)
        "
    
    - name: Test file generation
      env:
        SITE_BASE_URL: "https://test-validation.example.com"
      run: |
        cd ai-generators
        python generate_files_xlsx.py
        cd ..
        
        # Check output
        if [ ! -d "schema-files" ]; then
          echo "✗ No schema-files directory created"
          exit 1
        fi
        
        file_count=$(find schema-files -name "*.json" | wc -l)
        echo "✓ Generated $file_count JSON files"
        
        if [ $file_count -eq 0 ]; then
          echo "✗ No files generated"
          exit 1
        fi
    
    - name: Test sitemap generation
      run: |
        python generate_sitemaps.py
        
        if [ ! -f "sitemaps/_report.txt" ]; then
          echo "✗ No sitemap report generated"
          exit 1
        fi
        
        echo "=== Sitemap Report ==="
        cat sitemaps/_report.txt
        
        # Check for errors in report
        if grep -i "error" sitemaps/_report.txt; then
          echo "✗ Errors found in sitemap generation"
          exit 1
        fi
    
    - name: Validate generated XML
      run: |
        python -c "
        import xml.etree.ElementTree as ET
        import os
        import sys
        
        xml_files = []
        if os.path.exists('ai-sitemap.xml'):
            xml_files.append('ai-sitemap.xml')
        
        if os.path.exists('sitemaps'):
            for file in os.listdir('sitemaps'):
                if file.endswith('.xml'):
                    xml_files.append(os.path.join('sitemaps', file))
        
        if not xml_files:
            print('⚠️ No XML files found to validate')
            sys.exit(0)
        
        print(f'Validating {len(xml_files)} XML files...')
        
        for xml_file in xml_files:
            try:
                tree = ET.parse(xml_file)
                root = tree.getroot()
                
                # Check namespace
                if 'sitemaps.org' not in root.tag:
                    print(f'✗ {xml_file}: Invalid namespace')
                    sys.exit(1)
                
                # Count URLs
                if 'urlset' in root.tag:
                    urls = root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}url')
                    print(f'✓ {xml_file}: {len(urls)} URLs')
                elif 'sitemapindex' in root.tag:
                    sitemaps = root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}sitemap')
                    print(f'✓ {xml_file}: {len(sitemaps)} sitemaps in index')
                
            except ET.ParseError as e:
                print(f'✗ {xml_file}: Parse error - {e}')
                sys.exit(1)
            except Exception as e:
                print(f'✗ {xml_file}: Error - {e}')
                sys.exit(1)
        
        print('✓ All XML files valid')
        "

  security-scan:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    - name: Check for secrets in code
      run: |
        # Basic secret scanning
        if grep -r -i "password\|secret\|key\|token" --include="*.py" --include="*.yml" --include="*.yaml" .; then
          echo "⚠️ Potential secrets found in code. Please review:"
          grep -r -n -i "password\|secret\|key\|token" --include="*.py" --include="*.yml" --include="*.yaml" .
        else
          echo "✓ No obvious secrets found in code"
        fi
    
    - name: Check file permissions
      run: |
        echo "Checking for overly permissive files..."
        find . -type f -perm /o+w -not -path "./.git/*" | while read file; do
          echo "⚠️ World-writable file: $file"
        done || echo "✓ No world-writable files found"

  performance-test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        pip install pandas openpyxl pyyaml time
    
    - name: Performance test
      env:
        SITE_BASE_URL: "https://performance-test.example.com"
      run: |
        echo "Testing performance with current dataset..."
        
        start_time=$(date +%s)
        cd ai-generators
        python generate_files_xlsx.py
        cd ..
        python generate_sitemaps.py
        end_time=$(date +%s)
        
        duration=$((end_time - start_time))
        echo "Total execution time: ${duration} seconds"
        
        if [ $duration -gt 300 ]; then  # 5 minutes
          echo "⚠️ Warning: Execution took longer than expected (${duration}s > 300s)"
        else
          echo "✓ Performance test passed (${duration}s)"
        fi
        
        # Check file sizes
        if [ -d "schema-files" ]; then
          total_size=$(du -sh schema-files | cut -f1)
          echo "Generated files total size: $total_size"
        fi
```

### 4. Docker Configuration Template

**File**: `Dockerfile`

```dockerfile
# Multi-stage Docker build for the GitHub workflow system
FROM python:3.11-slim as builder

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY ai-generators/requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Production stage
FROM python:3.11-slim as production

# Set working directory
WORKDIR /app

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    curl \
    xmlstarlet \
    && rm -rf /var/lib/apt/lists/*

# Copy Python packages from builder stage
COPY --from=builder /root/.local /root/.local

# Make sure scripts in .local are usable:
ENV PATH=/root/.local/bin:$PATH

# Copy application files
COPY ai-generators/ ai-generators/
COPY generate_sitemaps.py .
COPY data/ data/

# Set default environment variables
ENV SITE_BASE_URL=https://example.com
ENV ENVIRONMENT=production
ENV LOG_LEVEL=INFO

# Create output directories
RUN mkdir -p schema-files sitemaps

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD python -c "import pandas as pd; print('OK')" || exit 1

# Default command
CMD ["python", "ai-generators/generate_files_xlsx.py"]
```

**File**: `docker-compose.yml`

```yaml
version: '3.8'

services:
  file-generator:
    build: .
    environment:
      - SITE_BASE_URL=https://your-domain.com
      - ENVIRONMENT=production
      - LOG_LEVEL=INFO
    volumes:
      - ./data:/app/data:ro
      - ./output:/app/schema-files
      - ./sitemaps:/app/sitemaps
    command: |
      sh -c "
        echo 'Starting file generation...' &&
        python ai-generators/generate_files_xlsx.py &&
        echo 'Starting sitemap generation...' &&
        python generate_sitemaps.py &&
        echo 'Process complete.'
      "
  
  file-generator-dev:
    build: .
    environment:
      - SITE_BASE_URL=http://localhost:8080
      - ENVIRONMENT=development
      - LOG_LEVEL=DEBUG
    volumes:
      - ./data:/app/data:ro
      - ./output:/app/schema-files
      - ./sitemaps:/app/sitemaps
      - .:/app:ro  # Mount entire directory for development
    command: |
      sh -c "
        while true; do
          echo 'Running development cycle...'
          python ai-generators/generate_files_xlsx.py
          python generate_sitemaps.py
          echo 'Waiting 60 seconds...'
          sleep 60
        done
      "
    profiles:
      - dev

  nginx:
    image: nginx:alpine
    ports:
      - "8080:80"
    volumes:
      - ./output:/usr/share/nginx/html/schema-files:ro
      - ./sitemaps:/usr/share/nginx/html/sitemaps:ro
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - file-generator
    profiles:
      - serve
```

### 5. Development Configuration Templates

**File**: `.env.development`

```bash
# Development Environment Configuration
SITE_BASE_URL=http://localhost:8080
ENVIRONMENT=development
LOG_LEVEL=DEBUG

# Feature flags for development
GENERATE_JSON=true
GENERATE_YAML=true
GENERATE_MD=true
GENERATE_LLM=true
GENERATE_SITEMAP=true

# Development-specific settings
FILTER_EMPTY_FIELDS=false
MIN_FIELDS_REQUIRED=1
ENABLE_SEARCH_PING=false
VALIDATE_URLS=false

# File paths (relative to project root)
DATA_FILE=data/client-data.xlsx
OUTPUT_DIR=schema-files
SITEMAP_FILE=ai-sitemap.xml

# Performance settings
MAX_URLS_PER_SITEMAP=1000
GENERATE_INDEX=true
```

**File**: `.env.staging`

```bash
# Staging Environment Configuration
SITE_BASE_URL=https://staging.client-domain.com
ENVIRONMENT=staging
LOG_LEVEL=INFO

# Feature flags
GENERATE_JSON=true
GENERATE_YAML=true
GENERATE_MD=true
GENERATE_LLM=true
GENERATE_SITEMAP=true

# Staging-specific settings
FILTER_EMPTY_FIELDS=true
MIN_FIELDS_REQUIRED=2
ENABLE_SEARCH_PING=false
VALIDATE_URLS=true

# Standard paths
DATA_FILE=data/client-data.xlsx
OUTPUT_DIR=schema-files
SITEMAP_FILE=ai-sitemap.xml

# Performance settings
MAX_URLS_PER_SITEMAP=10000
GENERATE_INDEX=true
```

**File**: `.env.production`

```bash
# Production Environment Configuration
SITE_BASE_URL=https://www.client-domain.com
ENVIRONMENT=production
LOG_LEVEL=ERROR

# All features enabled for production
GENERATE_JSON=true
GENERATE_YAML=true
GENERATE_MD=true
GENERATE_LLM=true
GENERATE_SITEMAP=true

# Production settings
FILTER_EMPTY_FIELDS=true
MIN_FIELDS_REQUIRED=3
ENABLE_SEARCH_PING=true
VALIDATE_URLS=true

# Standard paths
DATA_FILE=data/client-data.xlsx
OUTPUT_DIR=schema-files
SITEMAP_FILE=ai-sitemap.xml

# Performance settings
MAX_URLS_PER_SITEMAP=50000
GENERATE_INDEX=true
```

## Sample Data Templates

### 1. Comprehensive Excel Template

Save this as `client-data-template.xlsx`:

| client_name | website | category | tagline | description | business_hours | year_founded | number_of_employees | address | phone | email | locations_file | products_file | team_file |
|-------------|---------|----------|---------|-------------|----------------|--------------|-------------------|---------|-------|-------|----------------|---------------|-----------|
| Acme Corporation | https://acme-corp.com | Technology | "Innovation at Scale" | "Leading provider of enterprise technology solutions with global reach and local expertise." | Monday-Friday 9:00 AM - 6:00 PM | 2015 | 250 | 123 Technology Drive, Silicon Valley, CA 94000 | +1-555-ACME-123 | info@acme-corp.com | locations/acme-locations.json | products/acme-products.yaml | team/acme-team.json |
| Beta Services Inc | https://beta-services.net | Professional Services | "Your Success Partner" | "Comprehensive business consulting and professional services for growing companies." | Monday-Friday 8:00 AM - 5:00 PM, Saturday 9:00 AM - 1:00 PM | 2010 | 45 | 456 Business Avenue, Downtown, NY 10001 | +1-555-BETA-456 | contact@beta-services.net | | products/beta-services.yaml | |
| Gamma Industries | https://gamma-industries.org | Manufacturing | "Built to Last" | "Premium manufacturing solutions with a focus on quality, sustainability, and innovation." | Monday-Friday 7:00 AM - 4:00 PM | 1998 | 500 | 789 Industrial Boulevard, Manufacturing District, TX 77001 | +1-555-GAMMA-789 | sales@gamma-industries.org | locations/gamma-locations.json | products/gamma-catalog.json | team/gamma-leadership.yaml |

### 2. Multi-Sheet Excel Template Structure

**Sheet 1: Clients (main data)**
```
client_id | client_name | website | category | description | ...
1 | Acme Corp | https://acme-corp.com | Technology | Leading tech solutions | ...
2 | Beta Services | https://beta-services.net | Consulting | Business consulting | ...
```

**Sheet 2: Locations**
```
client_id | location_name | address | city | state | zip | phone | email
1 | Headquarters | 123 Tech Drive | Silicon Valley | CA | 94000 | 555-0001 | hq@acme-corp.com
1 | West Coast Office | 456 West Ave | Los Angeles | CA | 90001 | 555-0002 | west@acme-corp.com
```

**Sheet 3: Products**
```
client_id | product_name | category | description | price | availability
1 | Enterprise Suite | Software | Complete business solution | Contact for pricing | Available
1 | Cloud Platform | Infrastructure | Scalable cloud services | $99/month | Available
```

### 3. JSON Data Templates

**File**: `locations/sample-locations.json`

```json
{
  "client_name": "Sample Company",
  "locations": [
    {
      "name": "Headquarters",
      "type": "main_office",
      "address": {
        "street": "123 Business Street",
        "city": "Business City",
        "state": "BC",
        "zip": "12345",
        "country": "US"
      },
      "contact": {
        "phone": "+1-555-123-4567",
        "email": "hq@sample-company.com",
        "fax": "+1-555-123-4568"
      },
      "hours": {
        "monday": "9:00 AM - 6:00 PM",
        "tuesday": "9:00 AM - 6:00 PM",
        "wednesday": "9:00 AM - 6:00 PM",
        "thursday": "9:00 AM - 6:00 PM",
        "friday": "9:00 AM - 6:00 PM",
        "saturday": "10:00 AM - 2:00 PM",
        "sunday": "Closed"
      },
      "services": ["consulting", "support", "training"],
      "coordinates": {
        "latitude": 40.7128,
        "longitude": -74.0060
      }
    },
    {
      "name": "West Coast Branch",
      "type": "branch_office",
      "address": {
        "street": "456 Pacific Avenue", 
        "city": "Los Angeles",
        "state": "CA",
        "zip": "90001",
        "country": "US"
      },
      "contact": {
        "phone": "+1-555-987-6543",
        "email": "west@sample-company.com"
      },
      "hours": {
        "monday": "8:00 AM - 5:00 PM",
        "tuesday": "8:00 AM - 5:00 PM",
        "wednesday": "8:00 AM - 5:00 PM",
        "thursday": "8:00 AM - 5:00 PM",
        "friday": "8:00 AM - 5:00 PM",
        "saturday": "Closed",
        "sunday": "Closed"
      },
      "services": ["sales", "support"],
      "coordinates": {
        "latitude": 34.0522,
        "longitude": -118.2437
      }
    }
  ],
  "metadata": {
    "last_updated": "2024-01-15T10:30:00Z",
    "version": "1.0",
    "total_locations": 2
  }
}
```

**File**: `products/sample-products.yaml`

```yaml
client_name: "Sample Company"
products:
  - name: "Enterprise Solution"
    category: "Software"
    description: "Comprehensive business management software suite"
    features:
      - "Customer relationship management"
      - "Inventory tracking"
      - "Financial reporting"
      - "Analytics dashboard"
    pricing:
      model: "subscription"
      tiers:
        - name: "Starter"
          price: "$99/month"
          users: "Up to 5"
          features: ["Basic CRM", "Basic reporting"]
        - name: "Professional"
          price: "$299/month"
          users: "Up to 25"
          features: ["Full CRM", "Advanced reporting", "API access"]
        - name: "Enterprise"
          price: "Custom"
          users: "Unlimited"
          features: ["Everything included", "Custom integrations", "Dedicated support"]
    availability: "Available"
    support_level: "24/7"
    
  - name: "Cloud Infrastructure"
    category: "Infrastructure"
    description: "Scalable cloud hosting and infrastructure services"
    features:
      - "Auto-scaling servers"
      - "Load balancing"
      - "Database management"
      - "Security monitoring"
    pricing:
      model: "usage-based"
      starting_price: "$0.10/hour"
    availability: "Available"
    support_level: "Business hours"

metadata:
  last_updated: "2024-01-15T10:30:00Z"
  version: "2.1"
  total_products: 2
```

## Quick Start Configuration Scripts

### Setup Script Template

**File**: `setup-system.sh`

```bash
#!/bin/bash

# GitHub Workflow System Setup Script
# Run this script in your repository root to set up the basic structure

set -e

echo "🚀 Setting up GitHub Workflow System..."

# Create directory structure
echo "📁 Creating directory structure..."
mkdir -p .github/workflows
mkdir -p ai-generators
mkdir -p data
mkdir -p schema-files
mkdir -p sitemaps
mkdir -p locations
mkdir -p products
mkdir -p team

# Set permissions
chmod 755 .github/workflows
chmod 755 ai-generators
chmod 755 data
chmod 755 schema-files
chmod 755 sitemaps

echo "📦 Directory structure created successfully"

# Check for required files
echo "🔍 Checking for required files..."

MISSING_FILES=()

if [ ! -f "ai-generators/generate_files_xlsx.py" ]; then
    MISSING_FILES+=("ai-generators/generate_files_xlsx.py")
fi

if [ ! -f "ai-generators/requirements.txt" ]; then
    MISSING_FILES+=("ai-generators/requirements.txt")
fi

if [ ! -f "generate_sitemaps.py" ]; then
    MISSING_FILES+=("generate_sitemaps.py")
fi

if [ ! -f "data/client-data.xlsx" ]; then
    MISSING_FILES+=("data/client-data.xlsx")
fi

if [ ${#MISSING_FILES[@]} -gt 0 ]; then
    echo "⚠️  Missing required files:"
    for file in "${MISSING_FILES[@]}"; do
        echo "   - $file"
    done
    echo ""
    echo "Please copy the required files from your setup package."
else
    echo "✅ All required files present"
fi

# Check workflow files
echo "🔍 Checking workflow files..."

WORKFLOW_FILES=(
    ".github/workflows/auto-refresh.yml"
    ".github/workflows/build_ai_files_and_ping_xlsx.yml"
    ".github/workflows/sitemap.yml"
)

MISSING_WORKFLOWS=()

for workflow in "${WORKFLOW_FILES[@]}"; do
    if [ ! -f "$workflow" ]; then
        MISSING_WORKFLOWS+=("$workflow")
    fi
done

if [ ${#MISSING_WORKFLOWS[@]} -gt 0 ]; then
    echo "⚠️  Missing workflow files:"
    for workflow in "${MISSING_WORKFLOWS[@]}"; do
        echo "   - $workflow"
    done
else
    echo "✅ All workflow files present"
fi

# Test Python environment
echo "🐍 Testing Python environment..."

if command -v python >/dev/null 2>&1; then
    PYTHON_VERSION=$(python --version 2>&1)
    echo "   Python found: $PYTHON_VERSION"
    
    if [ -f "ai-generators/requirements.txt" ]; then
        echo "   Testing dependencies..."
        python -c "
import sys
missing = []
try:
    import pandas
    print('   ✅ pandas available')
except ImportError:
    missing.append('pandas')

try:
    import yaml
    print('   ✅ PyYAML available')
except ImportError:
    missing.append('PyYAML')

try:
    import openpyxl
    print('   ✅ openpyxl available')
except ImportError:
    missing.append('openpyxl')

if missing:
    print(f'   ⚠️ Missing dependencies: {missing}')
    print('   Run: pip install -r ai-generators/requirements.txt')
    sys.exit(1)
else:
    print('   ✅ All dependencies available')
"
    fi
else
    echo "   ⚠️  Python not found in PATH"
fi

# Check git configuration
echo "📝 Checking git configuration..."

if command -v git >/dev/null 2>&1; then
    if git rev-parse --git-dir > /dev/null 2>&1; then
        echo "   ✅ Git repository detected"
        
        REMOTE_URL=$(git remote get-url origin 2>/dev/null || echo "")
        if [ -n "$REMOTE_URL" ]; then
            echo "   Remote: $REMOTE_URL"
        else
            echo "   ⚠️  No remote origin configured"
        fi
    else
        echo "   ⚠️  Not a git repository"
        echo "   Run: git init && git remote add origin <your-repo-url>"
    fi
else
    echo "   ⚠️  Git not found"
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "1. Copy your workflow files to .github/workflows/"
echo "2. Copy your Python scripts to ai-generators/"
echo "3. Add your data file to data/client-data.xlsx"
echo "4. Configure repository variables:"
echo "   - Go to Settings → Secrets and variables → Actions → Variables"
echo "   - Add SITE_BASE_URL with your domain"
echo "5. Enable Actions in repository settings"
echo "6. Test locally: cd ai-generators && python generate_files_xlsx.py"
echo ""
echo "For detailed instructions, see the setup documentation."
```

### Testing Configuration Script

**File**: `test-configuration.py`

```python
#!/usr/bin/env python3
"""
Configuration testing script to validate setup before deployment.
Run this script to check if everything is configured correctly.
"""

import os
import sys
import json
from pathlib import Path

def test_environment_variables():
    """Test environment variable configuration."""
    print("🌍 Testing environment variables...")
    
    site_url = os.environ.get('SITE_BASE_URL')
    if site_url:
        print(f"   ✅ SITE_BASE_URL: {site_url}")
        if 'example.com' in site_url or 'yourdomain.com' in site_url:
            print("   ⚠️  Warning: Using placeholder domain")
    else:
        print("   ⚠️  SITE_BASE_URL not set")
    
    environment = os.environ.get('ENVIRONMENT', 'not set')
    print(f"   Environment: {environment}")
    
    return site_url is not None

def test_file_structure():
    """Test required file structure."""
    print("📁 Testing file structure...")
    
    required_dirs = [
        '.github/workflows',
        'ai-generators',
        'data',
        'schema-files',
        'sitemaps'
    ]
    
    required_files = [
        'ai-generators/generate_files_xlsx.py',
        'ai-generators/requirements.txt',
        'generate_sitemaps.py',
        'data/client-data.xlsx'
    ]
    
    all_good = True
    
    for directory in required_dirs:
        if Path(directory).exists():
            print(f"   ✅ {directory}/")
        else:
            print(f"   ❌ {directory}/ (missing)")
            all_good = False
    
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"   ✅ {file_path}")
        else:
            print(f"   ❌ {file_path} (missing)")
            all_good = False
    
    return all_good

def test_python_imports():
    """Test Python dependencies."""
    print("🐍 Testing Python imports...")
    
    required_packages = {
        'pandas': 'pandas',
        'yaml': 'PyYAML',
        'openpyxl': 'openpyxl',
        'xml.etree.ElementTree': 'Built-in'
    }
    
    all_good = True
    
    for module, package in required_packages.items():
        try:
            __import__(module)
            print(f"   ✅ {module} ({package})")
        except ImportError:
            print(f"   ❌ {module} ({package}) - run: pip install {package}")
            all_good = False
    
    return all_good

def test_data_file():
    """Test Excel data file."""
    print("📊 Testing data file...")
    
    try:
        import pandas as pd
        
        if not Path('data/client-data.xlsx').exists():
            print("   ❌ data/client-data.xlsx not found")
            return False
        
        df = pd.read_excel('data/client-data.xlsx')
        print(f"   ✅ Excel file loaded: {df.shape[0]} rows, {df.shape[1]} columns")
        
        # Check required columns
        required_columns = ['client_name', 'website']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            print(f"   ⚠️  Missing recommended columns: {missing_columns}")
            print(f"   Available columns: {list(df.columns)}")
        
        # Check for placeholder data
        if 'website' in df.columns:
            placeholder_count = df['website'].str.contains(
                'example.com|yourdomain.com|your-domain.com', 
                na=False, 
                regex=True
            ).sum()
            
            if placeholder_count > 0:
                print(f"   ⚠️  {placeholder_count} placeholder domains found")
            else:
                print("   ✅ No placeholder domains")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error reading Excel file: {e}")
        return False

def test_workflow_files():
    """Test GitHub workflow files."""
    print("⚙️  Testing workflow files...")
    
    workflow_files = [
        '.github/workflows/auto-refresh.yml',
        '.github/workflows/build_ai_files_and_ping_xlsx.yml',
        '.github/workflows/sitemap.yml'
    ]
    
    all_good = True
    
    for workflow_file in workflow_files:
        if Path(workflow_file).exists():
            print(f"   ✅ {workflow_file}")
            
            # Basic syntax check
            with open(workflow_file, 'r') as f:
                content = f.read()
                if 'SITE_BASE_URL' in content:
                    print(f"      Environment variable configured")
                else:
                    print(f"      ⚠️  No SITE_BASE_URL reference found")
        else:
            print(f"   ❌ {workflow_file} (missing)")
            all_good = False
    
    return all_good

def test_local_generation():
    """Test local file generation."""
    print("🏗️  Testing local generation...")
    
    try:
        # Set environment for testing
        if not os.environ.get('SITE_BASE_URL'):
            os.environ['SITE_BASE_URL'] = 'https://test-configuration.example.com'
        
        # Test file generation
        sys.path.append('ai-generators')
        
        try:
            from generate_files_xlsx import load_client_data, generate_files_from_row
            
            df = load_client_data('data/client-data.xlsx')
            print(f"   ✅ Data loaded: {len(df)} rows")
            
            if len(df) > 0:
                # Test processing first row
                first_row = df.iloc[0]
                success = generate_files_from_row(first_row)
                if success:
                    print("   ✅ File generation test successful")
                else:
                    print("   ⚠️  File generation test failed")
            
            return True
            
        except ImportError as e:
            print(f"   ❌ Import error: {e}")
            return False
            
    except Exception as e:
        print(f"   ❌ Generation test failed: {e}")
        return False

def generate_report(results):
    """Generate configuration report."""
    report = {
        'timestamp': '2024-01-15T10:30:00Z',
        'overall_status': 'PASS' if all(results.values()) else 'FAIL',
        'test_results': results,
        'recommendations': []
    }
    
    if not results['environment']:
        report['recommendations'].append('Set SITE_BASE_URL environment variable')
    
    if not results['file_structure']:
        report['recommendations'].append('Create missing directories and files')
    
    if not results['python_imports']:
        report['recommendations'].append('Install missing Python dependencies')
    
    if not results['data_file']:
        report['recommendations'].append('Fix data file issues')
    
    if not results['workflow_files']:
        report['recommendations'].append('Add missing workflow files')
    
    if not results['local_generation']:
        report['recommendations'].append('Fix file generation issues')
    
    # Save report
    with open('configuration-test-report.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n📋 Configuration report saved to configuration-test-report.json")
    
    return report

def main():
    """Main testing function."""
    print("🧪 GitHub Workflow System Configuration Test")
    print("=" * 50)
    
    results = {
        'environment': test_environment_variables(),
        'file_structure': test_file_structure(),
        'python_imports': test_python_imports(),
        'data_file': test_data_file(),
        'workflow_files': test_workflow_files(),
        'local_generation': test_local_generation()
    }
    
    print("\n" + "=" * 50)
    
    report = generate_report(results)
    
    if report['overall_status'] == 'PASS':
        print("🎉 All tests passed! System is ready for deployment.")
        return 0
    else:
        print("❌ Some tests failed. Please address the issues above.")
        print("\nRecommendations:")
        for rec in report['recommendations']:
            print(f"   • {rec}")
        return 1

if __name__ == '__main__':
    sys.exit(main())
```

Make the script executable:
```bash
chmod +x setup-system.sh
chmod +x test-configuration.py
```

---

**📋 Configuration Checklist**

Use this checklist when configuring a new deployment:

**Environment Setup:**
- [ ] Repository variables configured (`SITE_BASE_URL`)
- [ ] Environment-specific configs created (`.env.*` files)
- [ ] GitHub Actions permissions enabled
- [ ] Branch protection configured (if needed)

**File Structure:**
- [ ] All required directories created
- [ ] Workflow files deployed (`.github/workflows/`)
- [ ] Python scripts in place (`ai-generators/`)
- [ ] Data file added (`data/client-data.xlsx`)

**Testing:**
- [ ] Local environment tested
- [ ] Python dependencies installed
- [ ] File generation tested locally
- [ ] Sitemap generation tested
- [ ] Configuration test script passed

**Deployment:**
- [ ] Files committed to repository
- [ ] Manual workflow test completed
- [ ] Automated triggers verified
- [ ] Search engine pings tested
- [ ] Performance validated

**Documentation:**
- [ ] Configuration documented for team
- [ ] Environment-specific notes added
- [ ] Troubleshooting contacts updated
- [ ] Backup procedures documented
