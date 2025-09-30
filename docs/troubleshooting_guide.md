# Troubleshooting Guide

## Overview

This comprehensive troubleshooting guide covers common issues, error messages, and solutions for the GitHub workflow system. Use this guide to diagnose and resolve problems quickly.

## Quick Diagnostic Commands

Before diving into specific issues, run these diagnostic commands to gather information:

```bash
# Check system status
echo "=== SYSTEM STATUS ==="
python --version
git --version
git remote -v
git branch --show-current

# Check file structure
echo -e "\n=== FILE STRUCTURE ==="
ls -la .github/workflows/
ls -la ai-generators/
ls -la data/
ls -la schema-files/ 2>/dev/null || echo "schema-files directory not found"
ls -la sitemaps/ 2>/dev/null || echo "sitemaps directory not found"

# Check environment variables
echo -e "\n=== ENVIRONMENT ==="
echo "SITE_BASE_URL: ${SITE_BASE_URL:-not set}"

# Test Python imports
echo -e "\n=== PYTHON IMPORTS ==="
python -c "
try:
    import pandas as pd
    import yaml
    import openpyxl
    import xml.etree.ElementTree as ET
    print('✓ All imports successful')
    print(f'  pandas: {pd.__version__}')
    print(f'  PyYAML: {yaml.__version__}')
except ImportError as e:
    print(f'✗ Import error: {e}')
"

# Check Excel file
echo -e "\n=== DATA FILE ==="
if [ -f "data/client-data.xlsx" ]; then
    echo "✓ client-data.xlsx found"
    python -c "
import pandas as pd
try:
    df = pd.read_excel('data/client-data.xlsx')
    print(f'  Shape: {df.shape}')
    print(f'  Columns: {list(df.columns)[:5]}...' if len(df.columns) > 5 else f'  Columns: {list(df.columns)}')
except Exception as e:
    print(f'✗ Error reading Excel: {e}')
"
else
    echo "✗ client-data.xlsx not found"
fi
```

## Google Sheets Integration Issues

### Issue: "Please set a script property named GH_TOKEN"

**Error Context**: Google Apps Script shows this alert when trying to commit to GitHub.

**Root Causes**:
- GitHub token not configured in script properties
- Token was deleted or reset
- Wrong property name used

**Solutions**:

1. **Verify Script Properties**:
   ```javascript
   // In Apps Script editor, add this function to check properties
   function checkScriptProperties() {
     const props = PropertiesService.getScriptProperties().getProperties();
     console.log('Script properties:', Object.keys(props));
     console.log('GH_TOKEN exists:', 'GH_TOKEN' in props);
     console.log('GH_TOKEN length:', props.GH_TOKEN ? props.GH_TOKEN.length : 0);
   }
   ```

2. **Re-add the Token**:
   - Go to Apps Script → Settings (⚙️) → Script Properties
   - Delete existing GH_TOKEN if present
   - Click "Add script property"
   - Property: `GH_TOKEN`
   - Value: Your GitHub personal access token
   - Save

3. **Verify Token Validity**:
   ```bash
   # Test your token externally
   curl -H "Authorization: Bearer YOUR_TOKEN" https://api.github.com/user
   ```

### Issue: "Export URL returned error" or "Failed to fetch spreadsheet"

**Error Context**: Google Apps Script fails when trying to export the spreadsheet.

**Root Causes**:
- Insufficient permissions
- Spreadsheet too large
- Network connectivity issues
- OAuth token expired

**Solutions**:

1. **Check Spreadsheet Permissions**:
   - Ensure you have "Editor" access to the spreadsheet
   - Try opening the spreadsheet directly to verify access

2. **Reduce Spreadsheet Size**:
   ```javascript
   // Add size check to your script
   function checkSpreadsheetSize() {
     const ss = SpreadsheetApp.getActive();
     const sheets = ss.getSheets();
     let totalCells = 0;
     
     sheets.forEach(sheet => {
       const range = sheet.getDataRange();
       totalCells += range.getNumRows() * range.getNumColumns();
     });
     
     console.log(`Total cells: ${totalCells}`);
     if (totalCells > 10000) {
       console.log('Warning: Large spreadsheet may cause export issues');
     }
   }
   ```

3. **Refresh OAuth Authorization**:
   - In Apps Script editor: Run → Review permissions
   - Re-authorize the script
   - Clear browser cache if needed

### Issue: GitHub API returns 401 Unauthorized

**Error Context**: Google Apps Script logs show 401 responses from GitHub API.

**Root Causes**:
- Invalid GitHub token
- Token lacks required permissions
- Token expired

**Solutions**:

1. **Regenerate GitHub Token**:
   - Go to GitHub → Settings → Developer settings → Personal access tokens
   - Delete the old token
   - Create new token with these scopes:
     ```
     ✓ repo (Full control of private repositories)
     ✓ workflow (Update GitHub Action workflows)
     ```

2. **Test Token Permissions**:
   ```bash
   # Test repository access
   curl -H "Authorization: Bearer YOUR_NEW_TOKEN" \
        https://api.github.com/repos/YOUR_OWNER/YOUR_REPO
   
   # Test write permissions
   curl -H "Authorization: Bearer YOUR_NEW_TOKEN" \
        -X GET https://api.github.com/repos/YOUR_OWNER/YOUR_REPO/contents/README.md
   ```

3. **Update Script Properties**:
   - Replace the GH_TOKEN value in Apps Script properties
   - Test the integration again

### Issue: "Repository not found" or GitHub API returns 404

**Error Context**: Google Apps Script can authenticate but can't find the repository.

**Root Causes**:
- Incorrect repository owner/name in script
- Repository is private and token lacks access
- Repository was deleted or renamed

**Solutions**:

1. **Verify Repository Details**:
   ```javascript
   // In your Apps Script, add debugging
   function debugRepositoryAccess() {
     const GH_OWNER = 'your-github-username';  // Check this value
     const GH_REPO = 'your-repo-name';         // Check this value
     const token = PropertiesService.getScriptProperties().getProperty('GH_TOKEN');
     
     console.log(`Checking: https://github.com/${GH_OWNER}/${GH_REPO}`);
     
     const url = `https://api.github.com/repos/${GH_OWNER}/${GH_REPO}`;
     const response = UrlFetchApp.fetch(url, {
       headers: { Authorization: 'Bearer ' + token },
       muteHttpExceptions: true
     });
     
     console.log('Status:', response.getResponseCode());
     console.log('Response:', response.getContentText());
   }
   ```

2. **Check Repository Access**:
   - Verify the repository exists: `https://github.com/OWNER/REPO`
   - Ensure your GitHub account has access
   - Check if repository is private (token needs private repo access)

3. **Fix Configuration**:
   - Update GH_OWNER and GH_REPO constants in the script
   - Ensure exact case-sensitive match
   - Save and test again

## File Generation Issues

### Issue: "FileNotFoundError: client-data.xlsx"

**Error Context**: Python script can't find the Excel data file.

**Root Causes**:
- File not in expected location
- Incorrect file path in script
- File has different name

**Solutions**:

1. **Check File Location**:
   ```bash
   # From repository root
   find . -name "*.xlsx" -type f
   ls -la data/
   ```

2. **Fix File Path**:
   ```python
   # In generate_files_xlsx.py, check the DATA_FILE setting
   DATA_FILE = "data/client-data.xlsx"  # Correct path from ai-generators/ directory
   # Should be: DATA_FILE = "../data/client-data.xlsx"
   ```

3. **Verify File Integrity**:
   ```bash
   # Check if file is corrupted
   python -c "
   import pandas as pd
   try:
       df = pd.read_excel('data/client-data.xlsx')
       print(f'✓ File readable, shape: {df.shape}')
   except Exception as e:
       print(f'✗ File error: {e}')
   "
   ```

### Issue: "Missing optional dependency 'openpyxl'"

**Error Context**: Python error when trying to read Excel files.

**Root Causes**:
- openpyxl package not installed
- Wrong pandas version
- Virtual environment issues

**Solutions**:

1. **Install Missing Dependency**:
   ```bash
   pip install openpyxl>=3.1
   # Or install all requirements
   pip install -r ai-generators/requirements.txt
   ```

2. **Verify Installation**:
   ```python
   python -c "
   import openpyxl
   print(f'openpyxl version: {openpyxl.__version__}')
   
   import pandas as pd
   print(f'pandas version: {pd.__version__}')
   "
   ```

3. **Fix Virtual Environment**:
   ```bash
   # If using virtual environment
   deactivate  # Exit current environment
   python -m venv fresh-env
   source fresh-env/bin/activate
   pip install -r ai-generators/requirements.txt
   ```

### Issue: Empty or Missing Generated Files

**Error Context**: Script runs without errors but generates empty or no files.

**Root Causes**:
- All data filtered out due to empty values
- Incorrect data processing logic
- File writing permissions issues

**Solutions**:

1. **Debug Data Processing**:
   ```python
   # Add debugging to generate_files_xlsx.py
   def generate_files_from_row(row):
       print(f"Processing row: {row.get('client_name', 'unnamed')}")
       
       # Filter out empty values
       row_dict = {k: v for k, v in row.to_dict().items() 
                  if pd.notna(v) and str(v).strip()}
       print(f"Filtered data: {len(row_dict)} fields")
       
       if not row_dict:
           print("Warning: No data after filtering")
           return
       
       # Continue with file generation...
   ```

2. **Check File Permissions**:
   ```bash
   # Check if directories are writable
   ls -ld schema-files/
   touch schema-files/test-write.txt && rm schema-files/test-write.txt
   echo "Write test: $?"  # Should be 0
   ```

3. **Validate Input Data**:
   ```python
   # Check for empty data
   import pandas as pd
   df = pd.read_excel('data/client-data.xlsx')
   
   print(f"Total rows: {len(df)}")
   print(f"Rows with client_name: {df['client_name'].notna().sum()}")
   print(f"Rows with website: {df['website'].notna().sum()}")
   
   # Show first few rows
   print("\nFirst 3 rows:")
   for idx, row in df.head(3).iterrows():
       non_empty = {k: v for k, v in row.to_dict().items() 
                   if pd.notna(v) and str(v).strip()}
       print(f"Row {idx}: {len(non_empty)} non-empty fields")
   ```

### Issue: "UnicodeEncodeError" or Character Encoding Problems

**Error Context**: Errors when processing non-ASCII characters in data.

**Root Causes**:
- Incorrect file encoding
- Unicode characters in data
- System locale issues

**Solutions**:

1. **Fix File Encoding**:
   ```python
   # Ensure UTF-8 encoding in file operations
   def save_json(data, path):
       if not data:
           return
       with open(path, "w", encoding="utf-8") as f:
           json.dump(data, f, indent=2, ensure_ascii=False)  # Key: ensure_ascii=False
   
   def save_yaml(data, path):
       if not data:
           return
       with open(path, "w", encoding="utf-8") as f:
           yaml.dump(data, f, allow_unicode=True)  # Key: allow_unicode=True
   ```

2. **Test Unicode Handling**:
   ```python
   # Test script for unicode
   import json
   
   test_data = {
       "name": "Café Naïve",
       "description": "Testing: 北京 العربية русский",
       "location": "123 Üñíçödé Street"
   }
   
   # This should work without errors
   with open("unicode-test.json", "w", encoding="utf-8") as f:
       json.dump(test_data, f, indent=2, ensure_ascii=False)
   
   print("✓ Unicode test passed")
   ```

3. **Set System Locale**:
   ```bash
   # For Linux/Mac
   export LC_ALL=en_US.UTF-8
   export LANG=en_US.UTF-8
   
   # Verify
   python -c "import sys; print(sys.stdout.encoding)"
   ```

## GitHub Actions Workflow Issues

### Issue: "Resource not accessible by integration"

**Error Context**: GitHub Actions workflow fails with permission errors.

**Root Causes**:
- Insufficient workflow permissions
- Repository settings restrict Actions
- GITHUB_TOKEN lacks required scopes

**Solutions**:

1. **Fix Repository Permissions**:
   - Go to repository Settings → Actions → General
   - Under "Workflow permissions":
     ```
     ✓ Read and write permissions
     ✓ Allow GitHub Actions to create and approve pull requests
     ```

2. **Check Workflow Permissions**:
   ```yaml
   # In your workflow files, ensure permissions are set
   permissions:
     contents: write
     actions: read
   ```

3. **Verify Repository Settings**:
   - Settings → Actions → General → "Allow all actions and reusable workflows"
   - Ensure Actions are enabled for the repository

### Issue: "Environment variable not found" or Wrong Domain in Generated Files

**Error Context**: Generated files use default domain instead of configured one.

**Root Causes**:
- SITE_BASE_URL variable not set in repository
- Variable name mismatch
- Workflow not reading environment variables

**Solutions**:

1. **Set Repository Variables**:
   - Go to repository Settings → Secrets and variables → Actions
   - Click "Variables" tab
   - Add variable:
     ```
     Name: SITE_BASE_URL
     Value: https://your-actual-domain.com
     ```

2. **Verify Variable Usage**:
   ```yaml
   # In workflow file, check environment section
   - name: Generate files and sitemap
     env:
       SITE_BASE_URL: "${{ vars.SITE_BASE_URL }}"
     run: |
       python ai-generators/generate_files_xlsx.py
   ```

3. **Test Variable Access**:
   ```python
   # Add to your Python script for debugging
   import os
   site_base = os.environ.get("SITE_BASE_URL", "DEFAULT_VALUE")
   print(f"Using SITE_BASE_URL: {site_base}")
   ```

### Issue: Workflow Runs Forever or Times Out

**Error Context**: GitHub Actions workflow doesn't complete within the time limit.

**Root Causes**:
- Infinite loops in code
- Large dataset processing
- Network timeouts
- Dependency installation issues

**Solutions**:

1. **Add Debugging and Timeouts**:
   ```yaml
   - name: Generate files with timeout
     timeout-minutes: 10  # Add timeout
     run: |
       echo "Starting file generation..."
       python ai-generators/generate_files_xlsx.py
       echo "File generation completed"
   ```

2. **Optimize Data Processing**:
   ```python
   # Add progress indicators and limits
   def generate_all_files():
       ensure_output_dir()
       df = load_client_data(DATA_FILE)
       
       print(f"Processing {len(df)} rows...")
       for i, (_, row) in enumerate(df.iterrows()):
           if i % 10 == 0:  # Progress indicator
               print(f"Processed {i}/{len(df)} rows")
           generate_files_from_row(row)
       print("All files generated")
   ```

3. **Check for Infinite Loops**:
   ```python
   # Add safety counters
   def generate_sitemap(root_dir=OUTPUT_DIR, output_file=SITEMAP_FILE):
       file_count = 0
       max_files = 10000  # Safety limit
       
       for dirpath, _, filenames in os.walk(root_dir):
           for fname in filenames:
               file_count += 1
               if file_count > max_files:
                   print(f"Warning: Processing stopped at {max_files} files")
                   break
               # Process file...
   ```

### Issue: "Push rejected" or Git Conflicts

**Error Context**: Workflow can't push generated files back to repository.

**Root Causes**:
- Multiple workflows running simultaneously
- Branch protection rules
- Git conflicts with manual commits

**Solutions**:

1. **Add Git Pull Before Push**:
   ```yaml
   - name: Commit and push changes
     run: |
       git config --global user.name 'github-actions[bot]'
       git config --global user.email 'github-actions[bot]@users.noreply.github.com'
       git pull --rebase origin main  # Add this line
       git add .
       git commit -m "Update generated files" || echo "No changes"
       git push
   ```

2. **Handle Concurrent Workflows**:
   ```yaml
   # Add concurrency control to workflow
   concurrency:
     group: file-generation
     cancel-in-progress: true
   ```

3. **Check Branch Protection**:
   - Go to repository Settings → Branches
   - Review protection rules for main branch
   - Ensure "Restrict pushes that create files" is not enabled
   - Allow Actions to bypass restrictions if needed

## Sitemap Generation Issues

### Issue: "Placeholder domain detected" in Sitemap Report

**Error Context**: Sitemap generation report shows domains being filtered out.

**Root Causes**:
- Test domains in data (yourdomain.com, example.com)
- Incorrect domain configuration
- Client hasn't updated their domain

**Solutions**:

1. **Review Filtered Domains**:
   ```bash
   # Check sitemap report
   cat sitemaps/_report.txt | grep -i "placeholder\|error"
   ```

2. **Update Domain Data**:
   - Edit `data/client-data.xlsx`
   - Replace placeholder domains with real domains
   - Common placeholders to replace:
     ```
     yourdomain.com → actual-client-domain.com
     example.com → real-website.com
     your-domain.com → client-site.org
     ```

3. **Customize Placeholder Detection**:
   ```python
   # In generate_sitemaps.py, modify the function
   def is_placeholder_domain(domain: str) -> bool:
       low = domain.lower()
       placeholders = [
           "example.com", 
           "yourdomain.com", 
           "your-domain.com",
           "test.com",  # Add client-specific test domains
           "staging.com"
       ]
       return any(p in low for p in placeholders)
   ```

### Issue: "No files found" for Sitemap Generation

**Error Context**: Sitemap generation runs but finds no files to include.

**Root Causes**:
- Generated files not in expected locations
- File scanning configuration incorrect
- Files filtered out due to size or format

**Solutions**:

1. **Check File Locations**:
   ```bash
   # Verify generated files exist
   find schema-files -name "*.json" -o -name "*.yaml" -o -name "*.yml"
   
   # Check file sizes (empty files are excluded)
   find schema-files -name "*.json" -exec ls -la {} \;
   ```

2. **Debug File Scanning**:
   ```python
   # Add debugging to generate_sitemaps.py
   def debug_file_scanning():
       import os
       from pathlib import Path
       
       folders = ["locations", "products", "team", "schema-files"]
       for folder in folders:
           if Path(folder).exists():
               files = list(Path(folder).rglob("*"))
               print(f"{folder}: {len(files)} total files")
               
               valid_files = [f for f in files 
                            if f.suffix.lower() in {".json", ".yaml", ".yml"}
                            and f.is_file() 
                            and f.stat().st_size > 0]
               print(f"{folder}: {len(valid_files)} valid files")
           else:
               print(f"{folder}: directory not found")
   ```

3. **Adjust Scanning Configuration**:
   ```python
   # In generate_sitemaps.py, modify scanning logic
   DEFAULT_FOLDERS = ["locations", "products", "team", "schema-files"]  # Add schema-files
   VALID_EXTS = {".json", ".yaml", ".yml", ".md"}  # Add .md if needed
   ```

### Issue: Invalid XML in Generated Sitemaps

**Error Context**: XML validation fails for generated sitemap files.

**Root Causes**:
- Special characters in URLs or data
- Incorrect XML formatting
- Encoding issues

**Solutions**:

1. **Validate XML Structure**:
   ```bash
   # Check XML validity
   xmllint --noout sitemaps/*.xml
   xmllint --noout ai-sitemap.xml
   ```

2. **Fix XML Encoding Issues**:
   ```python
   # In generate_sitemaps.py, properly escape XML
   import xml.sax.saxutils as saxutils
   
   def write_sitemap_entry(f, domain, file_path, lastmod):
       # Escape special characters
       safe_domain = saxutils.escape(domain)
       safe_path = saxutils.escape(file_path)
       
       f.write("  <url>\n")
       f.write(f"    <loc>{safe_domain}/{safe_path}</loc>\n")
       f.write(f"    <lastmod>{lastmod}</lastmod>\n")
       f.write("  </url>\n")
   ```

3. **Handle Special Characters in URLs**:
   ```python
   import urllib.parse
   
   def sanitize_url_path(path):
       # URL-encode special characters
       return urllib.parse.quote(path, safe='/')
   ```

## Performance Optimization Issues

### Issue: Slow File Generation with Large Datasets

**Error Context**: Processing takes too long with many clients or large Excel files.

**Root Causes**:
- Inefficient data processing
- Large Excel files
- Many output files
- Disk I/O bottlenecks

**Solutions**:

1. **Add Progress Monitoring**:
   ```python
   import time
   
   def generate_all_files():
       start_time = time.time()
       ensure_output_dir()
       df = load_client_data(DATA_FILE)
       
       print(f"Processing {len(df)} clients...")
       
       for i, (_, row) in enumerate(df.iterrows()):
           client_start = time.time()
           generate_files_from_row(row)
           client_time = time.time() - client_start
           
           if i % 10 == 0:
               total_time = time.time() - start_time
               avg_time = total_time / (i + 1)
               remaining = (len(df) - i - 1) * avg_time
               print(f"Progress: {i+1}/{len(df)} ({client_time:.2f}s/client, {remaining:.1f}s remaining)")
   ```

2. **Optimize File I/O**:
   ```python
   def save_all_formats(data, base_path, base_name):
       """Save all formats in one function to reduce file operations"""
       os.makedirs(base_path, exist_ok=True)
       
       if not data:
           return
       
       # Save JSON
       json_path = os.path.join(base_path, f"{base_name}.json")
       with open(json_path, "w", encoding="utf-8") as f:
           json.dump(data, f, indent=2, ensure_ascii=False)
       
       # Save YAML  
       yaml_path = os.path.join(base_path, f"{base_name}.yaml")
       with open(yaml_path, "w", encoding="utf-8") as f:
           yaml.dump(data, f, allow_unicode=True)
       
       # Generate and save markdown
       md_content = f"# {data.get('client_name', base_name)}\n\n"
       for key, value in data.items():
           md_content += f"**{key}:** {value}\n\n"
       
       md_path = os.path.join(base_path, f"{base_name}.md")
       with open(md_path, "w", encoding="utf-8") as f:
           f.write(md_content)
   ```

3. **Implement Batching for Large Datasets**:
   ```python
   def generate_files_in_batches(batch_size=50):
       df = load_client_data(DATA_FILE)
       total_batches = (len(df) + batch_size - 1) // batch_size
       
       for batch_num in range(total_batches):
           start_idx = batch_num * batch_size
           end_idx = min(start_idx + batch_size, len(df))
           batch_df = df.iloc[start_idx:end_idx]
           
           print(f"Processing batch {batch_num + 1}/{total_batches}")
           
           for _, row in batch_df.iterrows():
               generate_files_from_row(row)
           
           # Optional: Add small delay between batches
           time.sleep(0.1)
   ```

### Issue: GitHub Actions Workflow Taking Too Long

**Error Context**: Workflows hit time limits or run very slowly.

**Root Causes**:
- Large datasets
- Slow dependency installation
- Network latency for search engine pings

**Solutions**:

1. **Optimize Dependency Installation**:
   ```yaml
   - name: Cache Python dependencies
     uses: actions/cache@v4
     with:
       path: ~/.cache/pip
       key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
       restore-keys: |
         ${{ runner.os }}-pip-
   
   - name: Install dependencies
     run: |
       python -m pip install --upgrade pip
       pip install -r ai-generators/requirements.txt
   ```

2. **Add Timeout and Retry Logic**:
   ```yaml
   - name: Generate files with timeout
     timeout-minutes: 15
     run: |
       python ai-generators/generate_files_xlsx.py
   
   - name: Ping search engines with retries
     run: |
       for i in {1..3}; do
         echo "Ping attempt $i"
         curl -m 30 "http://www.google.com/ping?sitemap=${{ vars.SITE_BASE_URL }}/ai-sitemap.xml" && break
         sleep 5
       done
   ```

3. **Parallel Processing** (if applicable):
   ```python
   # For very large datasets, consider parallel processing
   from concurrent.futures import ThreadPoolExecutor
   import threading
   
   def generate_files_parallel(max_workers=4):
       df = load_client_data(DATA_FILE)
       
       def process_row(row_data):
           idx, row = row_data
           try:
               generate_files_from_row(row)
               return f"✓ Row {idx}"
           except Exception as e:
               return f"✗ Row {idx}: {e}"
       
       with ThreadPoolExecutor(max_workers=max_workers) as executor:
           results = list(executor.map(process_row, df.iterrows()))
       
       for result in results:
           print(result)
   ```

## Search Engine Integration Issues

### Issue: Search Engine Pings Failing

**Error Context**: curl commands for Google/Bing ping return errors.

**Root Causes**:
- Invalid sitemap URLs
- Network connectivity issues
- Sitemap not accessible publicly
- Rate limiting

**Solutions**:

1. **Test Sitemap Accessibility**:
   ```bash
   # Test if sitemap is publicly accessible
   curl -I "https://your-domain.com/ai-sitemap.xml"
   # Should return 200 OK
   
   # Test sitemap validity
   curl "https://your-domain.com/ai-sitemap.xml" | head -20
   ```

2. **Add Error Handling to Pings**:
   ```yaml
   - name: Ping search engines with better error handling
     if: github.ref == 'refs/heads/main'
     run: |
       echo "Pinging Google..."
       if curl -f -m 30 "http://www.google.com/ping?sitemap=${{ vars.SITE_BASE_URL }}/ai-sitemap.xml"; then
         echo "✓ Google ping successful"
       else
         echo "⚠️ Google ping failed (this is often normal)"
       fi
       
       echo "Pinging Bing..."
       if curl -f -m 30 "https://www.bing.com/ping?sitemap=${{ vars.SITE_BASE_URL }}/ai-sitemap.xml"; then
         echo "✓ Bing ping successful" 
       else
         echo "⚠️ Bing ping failed (this is often normal)"
       fi
   ```

3. **Verify Sitemap URL Format**:
   ```bash
   # Check that the URL is correctly formatted
   echo "Sitemap URL: https://your-domain.com/ai-sitemap.xml"
   # Should not have double slashes, weird characters, etc.
   ```

### Issue: Generated Files Not Accessible via Web

**Error Context**: Sitemap URLs return 404 errors when accessed.

**Root Causes**:
- Files not deployed to web server
- Incorrect web server configuration
- File permissions issues
- Wrong base URL in sitemap

**Solutions**:

1. **Verify File Deployment**:
   ```bash
   # Check that files are committed to repository
   git log --oneline -10 | grep "github-actions"
   
   # Check recent commits include generated files
   git show --name-only HEAD
   ```

2. **Test Web Access**:
   ```bash
   # Test a few generated file URLs
   curl -I "https://your-domain.com/schema-files/client1/client1.json"
   curl -I "https://your-domain.com/schema-files/client2/client2.yaml"
   ```

3. **Check Base URL Configuration**:
   - Verify SITE_BASE_URL matches your actual domain
   - Ensure no trailing slash issues
   - Check if subdirectories are properly configured

## Emergency Recovery Procedures

### Complete System Reset

If multiple issues persist, perform a complete system reset:

1. **Backup Current State**:
   ```bash
   # Create backup branch
   git checkout -b backup-$(date +%Y%m%d-%H%M%S)
   git push origin backup-$(date +%Y%m%d-%H%M%S)
   git checkout main
   ```

2. **Clean Generated Files**:
   ```bash
   # Remove all generated files
   rm -rf schema-files/*
   rm -rf sitemaps/*
   rm -f ai-sitemap.xml
   git add -A
   git commit -m "Clean generated files for system reset"
   git push
   ```

3. **Redeploy System Files**:
   ```bash
   # Re-copy all system files from your setup
   # Follow the deployment instructions again
   ```

4. **Run Full Test Suite**:
   ```bash
   # Run complete testing as per testing guide
   python create_test_data.py
   cd ai-generators && python generate_files_xlsx.py && cd ..
   python generate_sitemaps.py
   python validate_output.py
   ```

### Data Recovery from Backup

If data is corrupted:

1. **Identify Good Backup**:
   ```bash
   # Find recent backup with working data
   git log --oneline --grep="Update client workbook" | head -5
   ```

2. **Restore Data File**:
   ```bash
   # Restore from specific commit
   git checkout COMMIT_HASH -- data/client-data.xlsx
   git add data/client-data.xlsx
   git commit -m "Restore data from backup"
   git push
   ```

3. **Trigger Regeneration**:
   - Go to GitHub Actions
   - Manually trigger "Build AI files from XLSX and ping sitemap"
   - Monitor for successful completion

## Getting Help

### Information to Gather Before Seeking Help

When reporting issues, collect this information:

```bash
# System information
echo "=== SYSTEM INFO ==="
python --version
git --version
uname -a

# Repository state  
echo -e "\n=== REPOSITORY INFO ==="
git remote -v
git branch --show-current
git log --oneline -5

# File structure
echo -e "\n=== FILES ==="
find . -name "*.py" -o -name "*.yml" -o -name "*.yaml" | sort

# Environment
echo -e "\n=== ENVIRONMENT ==="
env | grep -E "(SITE_BASE|GITHUB)" || echo "No relevant env vars"

# Error details
echo -e "\n=== RECENT ERRORS ==="
# Include any error messages, stack traces, or workflow logs
```

### Escalation Path

1. **Check this troubleshooting guide** for known issues
2. **Review GitHub Actions logs** for specific error details  
3. **Test locally** to isolate whether issue is local or in workflows
4. **Check repository settings** for permissions and configuration
5. **Create support ticket** with detailed information above

---

**🔧 Quick Fix Commands**

For rapid troubleshooting:

```bash
# Reset permissions
chmod +x ai-generators/*.py
chmod +w schema-files/ sitemaps/

# Reinstall dependencies
pip install -r ai-generators/requirements.txt --force-reinstall

# Test core functionality
python -c "import pandas as pd, yaml, openpyxl; print('✓ All imports OK')"

# Quick file generation test
cd ai-generators && python -c "
from generate_files_xlsx import load_client_data
df = load_client_data('../data/client-data.xlsx')
print(f'✓ Loaded {len(df)} rows')
"

# Check git status
git status --porcelain
```

**📋 Troubleshooting Checklist**

When encountering issues:

- [ ] Run diagnostic commands to gather information
- [ ] Check if it's a known issue in this guide
- [ ] Verify repository settings and permissions
- [ ] Test locally before investigating workflow issues
- [ ] Check GitHub Actions logs for specific errors
- [ ] Validate data integrity and file formats
- [ ] Confirm environment variables are set correctly
- [ ] Test individual components in isolation
- [ ] Document the issue and solution for future reference

**⚡ Emergency Contacts**

- Repository issues: Check GitHub repository settings and permissions
- Google Apps Script: Review script properties and OAuth permissions  
- Workflow failures: Check GitHub Actions logs and repository variables
- Data corruption: Use git history to restore from backup
- Performance issues: Review dataset size and optimization settings
