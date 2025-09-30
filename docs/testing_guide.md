# Comprehensive Testing Guide

## Overview

This guide provides step-by-step instructions for testing the GitHub workflow system at every level - from local file generation to complete end-to-end workflow validation. Follow these tests to ensure your system is working correctly before deploying to production.

## Test Environment Setup

### Prerequisites

- Python 3.11+ installed locally
- Git installed and configured
- Access to the GitHub repository
- Basic command line knowledge
- Text editor for viewing generated files

### Local Environment Setup

1. **Clone the repository**:
```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
```

2. **Create virtual environment** (recommended):
```bash
python -m venv testing-env
source testing-env/bin/activate  # On Windows: testing-env\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r ai-generators/requirements.txt
```

4. **Set environment variables**:
```bash
# Linux/Mac
export SITE_BASE_URL="https://your-test-domain.com"

# Windows
set SITE_BASE_URL=https://your-test-domain.com
```

## Test Data Preparation

### Sample Test Data

Create comprehensive test data in `data/client-data.xlsx` for thorough testing:

| client_name | website | category | tagline | description | business_hours | year_founded | number_of_employees | address | phone | email |
|-------------|---------|----------|---------|-------------|----------------|--------------|-------------------|---------|-------|-------|
| Acme Corp | https://acme-corp.com | Technology | "Innovation First" | "Leading tech solutions provider" | Mon-Fri 9AM-6PM | 2015 | 150 | 123 Tech Street, Silicon Valley | 555-0001 | info@acme-corp.com |
| Beta Services | https://beta-services.net | Consulting | "Your Success Partner" | "Professional business consulting" | Mon-Fri 8AM-5PM | 2010 | 25 | 456 Business Ave, Downtown | 555-0002 | contact@beta-services.net |
| Gamma Industries | https://gamma-industries.org | Manufacturing | "Built to Last" | "Quality manufacturing solutions" | Mon-Fri 7AM-4PM | 1998 | 500 | 789 Industrial Blvd, Manufacturing District | 555-0003 | sales@gamma-industries.org |
| Delta Creative | https://delta-creative.co | Design | "Creative Excellence" | "Award-winning design agency" | Tue-Sat 10AM-7PM | 2020 | 12 | 321 Creative Lane, Arts District | 555-0004 | hello@delta-creative.co |

### Edge Case Test Data

Add these rows to test edge cases and error handling:

| client_name | website | category | tagline | description | business_hours | year_founded | number_of_employees | address | phone | email |
|-------------|---------|----------|---------|-------------|----------------|--------------|-------------------|---------|-------|-------|
| Empty Data Test | https://empty-test.com |  |  |  |  |  |  |  |  |  |
| Special Chars | https://special-chars.com | Tech & AI | "Innovation & Growth" | "Testing special characters: @#$%^&*()" | 24/7 | 2023 | 1.5 | 123 Main St, Apt #4B | (555) 123-4567 | test+special@email.com |
| Long Content | https://long-content-test.com | Technology Solutions & Digital Transformation | "This is a very long tagline to test how the system handles extended text content that might exceed normal limits" | "This is a very long description with multiple sentences. It contains various punctuation marks! It also has questions? And it tests how the system handles extensive content that might be longer than typical business descriptions. This should help us verify that our file generation system can handle large amounts of text without breaking or corrupting the output files." | Monday through Friday 9:00 AM to 6:00 PM, Saturday 10:00 AM to 2:00 PM | 2019 | 247 | 1234 Very Long Street Name That Tests Address Field Limits, Suite 567, Extended Business District, Metropolitan Area | +1-555-123-4567 ext. 890 | very.long.email.address.for.testing@extremely-long-domain-name-for-testing.com |
| Unicode Test | https://unicode-test.com | Tëchnölögÿ | "Iññövâtïöñ & Grøwth" | "Testing unicode: café, naïve, résumé, 北京, العربية, русский" | Lunes a Viernes 9:00-18:00 | 2021 | 42 | 123 Üñíçödé St, Tëst Çítÿ | +1-555-üñí-çödé | tëst@üñíçödé.com |
| Placeholder Domain | yourdomain.com | Test | "Should Be Rejected" | "This should be filtered out by sitemap generator" | 9-5 | 2020 | 10 | 123 Test St | 555-0000 | test@yourdomain.com |

### Creating Test Excel File

Use Python to create the test file programmatically:

**File: `create_test_data.py`** (temporary testing script)
```python
import pandas as pd
import os

# Test data
test_data = [
    {
        "client_name": "Acme Corp",
        "website": "https://acme-corp.com",
        "category": "Technology",
        "tagline": "Innovation First",
        "description": "Leading tech solutions provider",
        "business_hours": "Mon-Fri 9AM-6PM",
        "year_founded": 2015,
        "number_of_employees": 150,
        "address": "123 Tech Street, Silicon Valley",
        "phone": "555-0001",
        "email": "info@acme-corp.com"
    },
    {
        "client_name": "Beta Services", 
        "website": "https://beta-services.net",
        "category": "Consulting",
        "tagline": "Your Success Partner",
        "description": "Professional business consulting",
        "business_hours": "Mon-Fri 8AM-5PM",
        "year_founded": 2010,
        "number_of_employees": 25,
        "address": "456 Business Ave, Downtown",
        "phone": "555-0002",
        "email": "contact@beta-services.net"
    },
    {
        "client_name": "Empty Data Test",
        "website": "https://empty-test.com",
        "category": "",
        "tagline": "",
        "description": "",
        "business_hours": "",
        "year_founded": "",
        "number_of_employees": "",
        "address": "",
        "phone": "",
        "email": ""
    },
    {
        "client_name": "Unicode Test",
        "website": "https://unicode-test.com", 
        "category": "Tëchnölögÿ",
        "tagline": "Iññövâtïöñ & Grøwth",
        "description": "Testing unicode: café, naïve, résumé, 北京, العربية, русский",
        "business_hours": "Lunes a Viernes 9:00-18:00",
        "year_founded": 2021,
        "number_of_employees": 42,
        "address": "123 Üñíçödé St, Tëst Çítÿ",
        "phone": "+1-555-üñí-çödé", 
        "email": "tëst@üñíçödé.com"
    },
    {
        "client_name": "Placeholder Domain",
        "website": "yourdomain.com",
        "category": "Test",
        "tagline": "Should Be Rejected",
        "description": "This should be filtered out by sitemap generator",
        "business_hours": "9-5",
        "year_founded": 2020,
        "number_of_employees": 10,
        "address": "123 Test St",
        "phone": "555-0000",
        "email": "test@yourdomain.com"
    }
]

# Create DataFrame and save
df = pd.DataFrame(test_data)
os.makedirs("data", exist_ok=True)
df.to_excel("data/client-data.xlsx", index=False)
print("✓ Test data created at data/client-data.xlsx")
print(f"✓ Created {len(test_data)} test records")
```

Run the script:
```bash
python create_test_data.py
```

## Local File Generation Testing

### Test 1: Basic File Generation

**Objective**: Verify that the file generation script works correctly with test data.

**Steps**:

1. **Run the generator script**:
```bash
cd ai-generators
python generate_files_xlsx.py
cd ..
```

2. **Verify output structure**:
```bash
# Check that directories were created
ls -la schema-files/

# Should see directories for each client
# Expected: acme_corp/, beta_services/, empty_data_test/, etc.
```

3. **Examine generated files**:
```bash
# Check a specific client's files
ls -la schema-files/acme_corp/

# Should contain: acme_corp.json, acme_corp.yaml, acme_corp.md, acme_corp.llm
```

4. **Validate file content**:
```bash
# Check JSON structure
cat schema-files/acme_corp/acme_corp.json | python -m json.tool

# Check YAML format
cat schema-files/acme_corp/acme_corp.yaml

# Check Markdown format
cat schema-files/acme_corp/acme_corp.md

# Check LLM format
cat schema-files/acme_corp/acme_corp.llm
```

**Expected Results**:
- Each client should have its own directory
- Four file types (.json, .yaml, .md, .llm) for each client
- Files should contain properly formatted data
- Empty fields should be filtered out (check empty_data_test)
- Unicode characters should be preserved (check unicode_test)

### Test 2: Sitemap Generation

**Objective**: Verify sitemap generation works and filters placeholder domains correctly.

**Steps**:

1. **Run sitemap generator**:
```bash
python generate_sitemaps.py
```

2. **Check sitemap directory**:
```bash
ls -la sitemaps/
# Should contain: *_sitemap.xml files and _report.txt
```

3. **Examine report**:
```bash
cat sitemaps/_report.txt
```

4. **Validate sitemap XML**:
```bash
# Check XML structure
xmllint --format sitemaps/acme_corp_sitemap.xml

# Or use Python
python -c "
import xml.etree.ElementTree as ET
tree = ET.parse('sitemaps/acme_corp_sitemap.xml')
print('✓ Valid XML structure')
for url in tree.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}url'):
    loc = url.find('{http://www.sitemaps.org/schemas/sitemap/0.9}loc').text
    print(f'URL: {loc}')
"
```

5. **Verify filtering**:
```bash
# Check that placeholder domain was filtered out
ls sitemaps/ | grep -i "placeholder\|yourdomain"
# Should return nothing (empty result)
```

**Expected Results**:
- Sitemap files generated for valid domains only
- Placeholder domains (yourdomain.com) excluded from sitemaps
- _report.txt shows processing results
- XML files are valid and well-formed
- URLs point to actual generated files

### Test 3: Error Handling

**Objective**: Test system behavior with problematic data.

**Steps**:

1. **Test with missing Excel file**:
```bash
# Rename the data file temporarily
mv data/client-data.xlsx data/client-data.xlsx.backup

# Run generator (should handle gracefully)
cd ai-generators
python generate_files_xlsx.py
cd ..

# Restore file
mv data/client-data.xlsx.backup data/client-data.xlsx
```

2. **Test with corrupted Excel file**:
```bash
# Create a text file with .xlsx extension
echo "This is not Excel data" > data/test-corrupt.xlsx

# Try to process it (should fail gracefully)
cd ai-generators
# Edit the script temporarily to use test-corrupt.xlsx
python -c "
import sys
sys.path.append('.')
from generate_files_xlsx import load_client_data
try:
    load_client_data('../data/test-corrupt.xlsx')
    print('✗ Should have failed')
except Exception as e:
    print(f'✓ Correctly handled error: {e}')
"
cd ..

# Clean up
rm data/test-corrupt.xlsx
```

3. **Test with empty Excel file**:
```bash
# Create empty Excel file
python -c "
import pandas as pd
df = pd.DataFrame()
df.to_excel('data/empty.xlsx', index=False)
print('Created empty Excel file')
"

# Process it (should handle gracefully)
cd ai-generators
python -c "
import sys
sys.path.append('.')
from generate_files_xlsx import load_client_data, generate_files_from_row
try:
    df = load_client_data('../data/empty.xlsx')
    print(f'✓ Loaded empty file: {df.shape}')
    for _, row in df.iterrows():
        print('Processing row (should be none)')
except Exception as e:
    print(f'✓ Handled empty file: {e}')
"
cd ..

rm data/empty.xlsx
```

**Expected Results**:
- Missing files should produce clear error messages
- Corrupted files should be handled gracefully
- Empty files should process without crashing
- Error messages should be informative and actionable

## GitHub Actions Workflow Testing

### Test 4: Manual Workflow Execution

**Objective**: Test GitHub Actions workflows manually before relying on automation.

**Steps**:

1. **Commit test data to repository**:
```bash
git add data/client-data.xlsx
git commit -m "Add test data for workflow testing"
git push origin main
```

2. **Trigger manual workflow**:
   - Go to your GitHub repository
   - Click "Actions" tab
   - Select "Build AI files from XLSX and ping sitemap"
   - Click "Run workflow"
   - Leave branch as "main"
   - Click "Run workflow" button

3. **Monitor workflow execution**:
   - Click on the running workflow
   - Watch each step execute
   - Check for any errors or warnings

4. **Examine workflow logs**:
   - Click on each step to see detailed logs
   - Look for the output from file generation
   - Verify search engine pings were attempted

**Expected Results**:
- All workflow steps complete successfully
- No error messages in logs
- Files are generated and committed back to repository
- Search engine ping attempts are logged

### Test 5: Verify Generated Output in Repository

**Objective**: Confirm that workflows correctly generate and commit files.

**Steps**:

1. **Check repository files after workflow**:
   - Go to repository main page
   - Look for `schema-files/` directory
   - Verify subdirectories for each client
   - Check that files were committed by github-actions[bot]

2. **Examine generated files online**:
   - Navigate to `schema-files/acme_corp/`
   - Click on `acme_corp.json` and verify content
   - Check other file formats (.yaml, .md, .llm)
   - Verify content matches your test data

3. **Check sitemap files**:
   - Look for `ai-sitemap.xml` in repository root
   - Check `sitemaps/` directory for individual sitemaps
   - View `sitemaps/_report.txt` for processing report

4. **Verify commit history**:
   - Go to repository commits
   - Look for commits by "github-actions[bot]"
   - Check commit messages and file changes

**Expected Results**:
- All generated files present in repository
- File contents match expected format and data
- Commit history shows automated commits
- No placeholder domains in sitemap files

### Test 6: Automated Trigger Testing

**Objective**: Test that workflows trigger automatically on data changes.

**Steps**:

1. **Make a change to Excel data**:
   - Use Google Sheets integration OR
   - Upload updated Excel file directly

2. **Update test data**:
```bash
# Add a new row to test data
python -c "
import pandas as pd
df = pd.read_excel('data/client-data.xlsx')
new_row = {
    'client_name': 'Auto Test Corp',
    'website': 'https://auto-test.com', 
    'category': 'Automation',
    'tagline': 'Testing Automation',
    'description': 'Testing automated workflow triggers',
    'business_hours': 'Always On',
    'year_founded': 2024,
    'number_of_employees': 1,
    'address': 'Cloud Infrastructure',
    'phone': '555-AUTO',
    'email': 'auto@test.com'
}
df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
df.to_excel('data/client-data.xlsx', index=False)
print('✓ Added test row for automation testing')
"

git add data/client-data.xlsx
git commit -m "Add auto-test data to trigger workflow"
git push origin main
```

3. **Monitor automatic execution**:
   - Go to Actions tab
   - Should see new workflow run triggered automatically
   - Wait for completion

4. **Verify new files generated**:
   - Check for `schema-files/auto_test_corp/`
   - Verify new sitemap entries
   - Confirm commit by github-actions[bot]

**Expected Results**:
- Workflow automatically triggers on Excel file changes
- New client data generates appropriate files
- Sitemaps update to include new entries
- Process completes without manual intervention

## End-to-End Integration Testing

### Test 7: Complete Google Sheets Integration

**Objective**: Test the full pipeline from Google Sheets to generated files.

**Prerequisites**: Google Sheets integration must be set up (see Google Sheets Setup Guide).

**Steps**:

1. **Update data in Google Sheets**:
   - Open your connected Google Sheet
   - Add a new row with test data:
     ```
     Integration Test | https://integration-test.com | Testing | Full Pipeline Test | Testing complete Google Sheets integration | 24/7 | 2024 | 999 | Test Location | 555-TEST | test@integration.com
     ```

2. **Trigger Google Apps Script**:
   - In Google Sheets: GitHub → Commit XLSX to GitHub
   - Wait for success confirmation

3. **Monitor automatic workflow**:
   - GitHub repository should show new commit from Google Apps Script
   - This should trigger the build workflow automatically
   - Monitor in Actions tab

4. **Verify end result**:
   - Check for new files in `schema-files/integration_test/`
   - Verify sitemap includes new domain
   - Confirm search engine pings attempted

**Expected Results**:
- Complete pipeline works from Google Sheets to final files
- No manual intervention required after Google Sheets update
- All files generated correctly with new data
- Search engines notified of sitemap updates

### Test 8: Performance and Load Testing

**Objective**: Test system performance with larger datasets.

**Steps**:

1. **Create larger test dataset**:
```bash
python -c "
import pandas as pd
import random

# Generate 50 test records
test_data = []
categories = ['Technology', 'Consulting', 'Manufacturing', 'Design', 'Healthcare', 'Finance', 'Education', 'Retail']
for i in range(50):
    test_data.append({
        'client_name': f'Test Company {i:03d}',
        'website': f'https://test-company-{i:03d}.com',
        'category': random.choice(categories),
        'tagline': f'Test tagline for company {i:03d}',
        'description': f'This is a test description for company {i:03d}. It contains multiple sentences for testing purposes. The company specializes in various business activities.',
        'business_hours': 'Mon-Fri 9AM-5PM',
        'year_founded': random.randint(1990, 2024),
        'number_of_employees': random.randint(1, 1000),
        'address': f'{i*10 + 123} Test Street, Test City {i:02d}',
        'phone': f'555-{i:04d}',
        'email': f'contact{i:03d}@test-company.com'
    })

df = pd.DataFrame(test_data)
df.to_excel('data/client-data-large.xlsx', index=False)
print(f'✓ Created large test dataset with {len(test_data)} records')
"
```

2. **Test with large dataset**:
```bash
# Backup original data
cp data/client-data.xlsx data/client-data-original.xlsx

# Use large dataset
cp data/client-data-large.xlsx data/client-data.xlsx

# Run local test first
cd ai-generators
time python generate_files_xlsx.py
cd ..

time python generate_sitemaps.py
```

3. **Commit and test workflow**:
```bash
git add data/client-data.xlsx
git commit -m "Test with large dataset (50 records)"
git push origin main
# Monitor workflow performance in Actions tab
```

4. **Measure results**:
   - Record execution time
   - Check file sizes
   - Verify all files generated correctly
   - Monitor GitHub Actions execution time

5. **Restore original data**:
```bash
mv data/client-data-original.xlsx data/client-data.xlsx
git add data/client-data.xlsx
git commit -m "Restore original test data"
git push origin main
```

**Expected Results**:
- System handles larger datasets gracefully
- Performance remains acceptable (< 5 minutes for 50 records)
- All files generated correctly
- Sitemap generation scales properly
- GitHub Actions completes within timeout limits

## Validation and Quality Assurance

### Test 9: Data Integrity Validation

**Objective**: Ensure generated files maintain data integrity and proper formatting.

**Steps**:

1. **Create validation script**:

**File: `validate_output.py`**
```python
import json
import yaml
import xml.etree.ElementTree as ET
import os
from pathlib import Path

def validate_json_files():
    """Validate all generated JSON files"""
    json_files = list(Path("schema-files").rglob("*.json"))
    print(f"Validating {len(json_files)} JSON files...")
    
    for json_file in json_files:
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            # Check for required fields (adjust as needed)
            if 'client_name' not in data and 'name' not in data:
                print(f"⚠️  {json_file}: Missing name field")
            if 'website' not in data:
                print(f"⚠️  {json_file}: Missing website field")
        except json.JSONDecodeError as e:
            print(f"✗ {json_file}: Invalid JSON - {e}")
        except Exception as e:
            print(f"✗ {json_file}: Error - {e}")
    
    print("✓ JSON validation complete")

def validate_yaml_files():
    """Validate all generated YAML files"""
    yaml_files = list(Path("schema-files").rglob("*.yaml"))
    print(f"Validating {len(yaml_files)} YAML files...")
    
    for yaml_file in yaml_files:
        try:
            with open(yaml_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
            if not data:
                print(f"⚠️  {yaml_file}: Empty YAML file")
        except yaml.YAMLError as e:
            print(f"✗ {yaml_file}: Invalid YAML - {e}")
        except Exception as e:
            print(f"✗ {yaml_file}: Error - {e}")
    
    print("✓ YAML validation complete")

def validate_sitemap_xml():
    """Validate sitemap XML files"""
    xml_files = list(Path("sitemaps").glob("*.xml")) + [Path("ai-sitemap.xml")]
    print(f"Validating {len(xml_files)} XML sitemap files...")
    
    for xml_file in xml_files:
        if not xml_file.exists():
            continue
        try:
            tree = ET.parse(xml_file)
            root = tree.getroot()
            
            # Check namespace
            if not root.tag.endswith('}urlset'):
                print(f"⚠️  {xml_file}: Unexpected root element")
            
            # Check URLs
            urls = root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}url')
            if len(urls) == 0:
                print(f"⚠️  {xml_file}: No URLs found")
            
            for url in urls:
                loc = url.find('{http://www.sitemaps.org/schemas/sitemap/0.9}loc')
                if loc is None or not loc.text:
                    print(f"⚠️  {xml_file}: URL missing location")
                elif not loc.text.startswith('http'):
                    print(f"⚠️  {xml_file}: Invalid URL format: {loc.text}")
                    
        except ET.ParseError as e:
            print(f"✗ {xml_file}: Invalid XML - {e}")
        except Exception as e:
            print(f"✗ {xml_file}: Error - {e}")
    
    print("✓ XML validation complete")

def check_file_consistency():
    """Check that each client has all expected file types"""
    client_dirs = [d for d in Path("schema-files").iterdir() if d.is_dir()]
    print(f"Checking consistency for {len(client_dirs)} clients...")
    
    expected_extensions = ['.json', '.yaml', '.md', '.llm']
    
    for client_dir in client_dirs:
        client_name = client_dir.name
        for ext in expected_extensions:
            expected_file = client_dir / f"{client_name}{ext}"
            if not expected_file.exists():
                print(f"⚠️  Missing {ext} file for {client_name}")
    
    print("✓ File consistency check complete")

if __name__ == "__main__":
    print("=== DATA INTEGRITY VALIDATION ===")
    validate_json_files()
    validate_yaml_files() 
    validate_sitemap_xml()
    check_file_consistency()
    print("=== VALIDATION COMPLETE ===")
```

2. **Run validation**:
```bash
python validate_output.py
```

3. **Fix any issues found** and re-run until clean

**Expected Results**:
- All JSON files are valid JSON
- All YAML files are valid YAML
- All XML files are well-formed
- Each client has all expected file types
- No data corruption or encoding issues

### Test 10: SEO and Accessibility Testing

**Objective**: Verify that generated files are SEO-friendly and accessible.

**Steps**:

1. **Check sitemap compliance**:
```bash
# Validate against sitemap protocol
python -c "
import xml.etree.ElementTree as ET
import urllib.parse
from datetime import datetime

def validate_sitemap(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    # Check namespace
    expected_ns = 'http://www.sitemaps.org/schemas/sitemap/0.9'
    if expected_ns not in root.tag:
        print('✗ Invalid namespace')
        return
    
    urls = root.findall(f'.//{{{expected_ns}}}url')
    print(f'✓ Found {len(urls)} URLs in sitemap')
    
    for i, url in enumerate(urls):
        loc = url.find(f'{{{expected_ns}}}loc')
        lastmod = url.find(f'{{{expected_ns}}}lastmod')
        
        if loc is None:
            print(f'✗ URL {i+1}: Missing location')
            continue
            
        # Validate URL format
        try:
            parsed = urllib.parse.urlparse(loc.text)
            if not all([parsed.scheme, parsed.netloc]):
                print(f'✗ URL {i+1}: Invalid format: {loc.text}')
        except Exception as e:
            print(f'✗ URL {i+1}: Parse error: {e}')
        
        # Validate lastmod format
        if lastmod is not None:
            try:
                datetime.fromisoformat(lastmod.text.replace('Z', '+00:00'))
            except Exception:
                print(f'⚠️  URL {i+1}: Invalid lastmod format: {lastmod.text}')
    
    print('✓ Sitemap validation complete')

# Check main sitemap
if os.path.exists('ai-sitemap.xml'):
    print('=== Validating main sitemap ===')
    validate_sitemap('ai-sitemap.xml')

# Check client sitemaps
import os
for sitemap in os.listdir('sitemaps/'):
    if sitemap.endswith('.xml'):
        print(f'=== Validating {sitemap} ===')
        validate_sitemap(f'sitemaps/{sitemap}')
"
```

2. **Test file accessibility**:
```bash
# Check file permissions
find schema-files -type f -exec ls -la {} \; | head -20

# Check file encoding
file schema-files/*/*.json | head -10
file schema-files/*/*.yaml | head -10
```

3. **Verify URL structure**:
```bash
# Check that all referenced files exist
python -c "
import xml.etree.ElementTree as ET
import urllib.parse
from pathlib import Path
import os

def check_urls_exist(sitemap_path, base_path=''):
    if not os.path.exists(sitemap_path):
        return
        
    tree = ET.parse(sitemap_path)
    urls = tree.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}url')
    
    print(f'Checking {len(urls)} URLs in {sitemap_path}')
    missing = 0
    
    for url in urls:
        loc = url.find('{http://www.sitemaps.org/schemas/sitemap/0.9}loc')
        if loc is not None:
            parsed = urllib.parse.urlparse(loc.text)
            file_path = parsed.path.lstrip('/')
            
            if os.path.exists(file_path):
                print(f'✓ {file_path}')
            else:
                print(f'✗ Missing: {file_path}')
                missing += 1
    
    if missing == 0:
        print('✓ All referenced files exist')
    else:
        print(f'✗ {missing} files missing')

check_urls_exist('ai-sitemap.xml')
"
```

**Expected Results**:
- Sitemaps conform to XML sitemap protocol
- All URLs are valid and properly formatted
- Referenced files exist and are accessible
- File permissions allow web server access
- No broken links or missing files

## Testing Documentation and Reporting

### Test 11: Generate Test Report

**Objective**: Create comprehensive test report for stakeholders.

**Steps**:

1. **Create test report generator**:

**File: `generate_test_report.py`**
```python
import os
import json
import xml.etree.ElementTree as ET
from pathlib import Path
from datetime import datetime
import pandas as pd

def generate_test_report():
    report = {
        'timestamp': datetime.now().isoformat(),
        'test_summary': {},
        'file_stats': {},
        'sitemap_stats': {},
        'issues': []
    }
    
    # Count generated files
    schema_files = list(Path("schema-files").rglob("*"))
    report['file_stats'] = {
        'total_files': len([f for f in schema_files if f.is_file()]),
        'json_files': len(list(Path("schema-files").rglob("*.json"))),
        'yaml_files': len(list(Path("schema-files").rglob("*.yaml"))),
        'md_files': len(list(Path("schema-files").rglob("*.md"))),
        'llm_files': len(list(Path("schema-files").rglob("*.llm"))),
        'client_directories': len([d for d in Path("schema-files").iterdir() if d.is_dir()])
    }
    
    # Analyze sitemaps
    sitemap_files = list(Path("sitemaps").glob("*.xml"))
    if Path("ai-sitemap.xml").exists():
        sitemap_files.append(Path("ai-sitemap.xml"))
    
    total_urls = 0
    for sitemap in sitemap_files:
        try:
            tree = ET.parse(sitemap)
            urls = tree.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}url')
            total_urls += len(urls)
        except Exception as e:
            report['issues'].append(f"Error reading {sitemap}: {e}")
    
    report['sitemap_stats'] = {
        'sitemap_files': len(sitemap_files),
        'total_urls': total_urls
    }
    
    # Test summary
    report['test_summary'] = {
        'files_generated': report['file_stats']['total_files'] > 0,
        'sitemaps_created': len(sitemap_files) > 0,
        'no_critical_issues': len(report['issues']) == 0,
        'test_passed': (
            report['file_stats']['total_files'] > 0 and
            len(sitemap_files) > 0 and
            len(report['issues']) == 0
        )
    }
    
    return report

def save_report_markdown(report):
    md_content = f"""# Test Execution Report

**Generated:** {report['timestamp']}

## Test Summary

✅ **Overall Status:** {'PASSED' if report['test_summary']['test_passed'] else 'FAILED'}

- Files Generated: {'✅ Yes' if report['test_summary']['files_generated'] else '❌ No'}
- Sitemaps Created: {'✅ Yes' if report['test_summary']['sitemaps_created'] else '❌ No'}
- No Critical Issues: {'✅ Yes' if report['test_summary']['no_critical_issues'] else '❌ No'}

## File Generation Statistics

- **Total Files Generated:** {report['file_stats']['total_files']}
- **Client Directories:** {report['file_stats']['client_directories']}
- **JSON Files:** {report['file_stats']['json_files']}
- **YAML Files:** {report['file_stats']['yaml_files']}
- **Markdown Files:** {report['file_stats']['md_files']}
- **LLM Files:** {report['file_stats']['llm_files']}

## Sitemap Statistics

- **Sitemap Files:** {report['sitemap_stats']['sitemap_files']}
- **Total URLs:** {report['sitemap_stats']['total_urls']}

## Issues Found

{chr(10).join(f'- {issue}' for issue in report['issues']) if report['issues'] else 'No issues found ✅'}

## Test Environment

- **Python Version:** {os.popen('python --version').read().strip()}
- **Working Directory:** {os.getcwd()}
- **Repository:** {os.popen('git remote get-url origin 2>/dev/null || echo "Not a git repository"').read().strip()}

## Next Steps

{'All tests passed! System is ready for production.' if report['test_summary']['test_passed'] else 'Please address the issues above before proceeding to production.'}

---
*Report generated by automated testing suite*
"""
    
    with open('test_report.md', 'w') as f:
        f.write(md_content)
    
    return md_content

if __name__ == "__main__":
    print("Generating test report...")
    report = generate_test_report()
    
    # Save JSON report
    with open('test_report.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    # Save Markdown report
    md_report = save_report_markdown(report)
    
    print("✓ Test report saved to test_report.json and test_report.md")
    print(f"✓ Test Status: {'PASSED' if report['test_summary']['test_passed'] else 'FAILED'}")
```

2. **Generate and review report**:
```bash
python generate_test_report.py
cat test_report.md
```

3. **Share report with team**:
```bash
# Commit test results
git add test_report.md test_report.json
git commit -m "Add test execution report"
git push origin main
```

**Expected Results**:
- Comprehensive test report generated
- Clear pass/fail status
- Detailed statistics on generated files
- Issue tracking for follow-up
- Documentation for stakeholders

## Continuous Testing Strategy

### Automated Testing Setup

Add testing to your GitHub Actions workflow:

**File: `.github/workflows/test.yml`**
```yaml
name: Automated Testing

on:
  pull_request:
  push:
    branches: [ main ]
  schedule:
    - cron: '0 6 * * 1'  # Weekly on Monday at 6 AM

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: pip install -r ai-generators/requirements.txt
    
    - name: Run file generation test
      run: |
        cd ai-generators
        python generate_files_xlsx.py
        cd ..
    
    - name: Run sitemap generation test
      run: python generate_sitemaps.py
    
    - name: Validate output
      run: python validate_output.py
    
    - name: Generate test report
      run: python generate_test_report.py
    
    - name: Upload test results
      uses: actions/upload-artifact@v4
      with:
        name: test-results
        path: |
          test_report.md
          test_report.json
          schema-files/
          sitemaps/
```

### Regular Testing Checklist

**Daily (Automated)**:
- [ ] File generation works with current data
- [ ] No broken sitemaps
- [ ] All workflows complete successfully

**Weekly (Manual)**:
- [ ] Test new data additions
- [ ] Verify search engine pings
- [ ] Check file quality and formatting
- [ ] Review workflow performance

**Monthly (Comprehensive)**:
- [ ] Full end-to-end testing
- [ ] Performance testing with large datasets
- [ ] Security validation
- [ ] Documentation updates
- [ ] Stakeholder report generation

## Troubleshooting Test Failures

### Common Test Failures and Solutions

**File Generation Fails**:
1. Check Excel file format and location
2. Verify Python dependencies are installed
3. Check file permissions and disk space
4. Validate Excel data structure

**Workflow Failures**:
1. Check GitHub Actions permissions
2. Verify environment variables are set
3. Check repository secrets configuration
4. Review workflow logs for specific errors

**Sitemap Issues**:
1. Verify domain configurations
2. Check for placeholder domains in data
3. Validate XML structure
4. Ensure referenced files exist

**Performance Issues**:
1. Monitor execution times
2. Check for large file sizes
3. Optimize data processing logic
4. Consider batching for large datasets

---

**📋 Testing Checklist**

Use this checklist for complete testing:

- [ ] Local environment setup complete
- [ ] Test data created and validated
- [ ] File generation works locally
- [ ] Sitemap generation works locally
- [ ] Error handling tested
- [ ] Manual GitHub workflow tested
- [ ] Automatic triggers tested
- [ ] End-to-end Google Sheets integration tested
- [ ] Performance testing completed
- [ ] Data integrity validated
- [ ] SEO compliance verified
- [ ] Test report generated
- [ ] Continuous testing configured
- [ ] Team documentation updated

**🔧 Quick Test Commands**

For rapid testing:

```bash
# Full local test
cd ai-generators && python generate_files_xlsx.py && cd .. && python generate_sitemaps.py

# Validation suite
python validate_output.py && python generate_test_report.py

# Clean up test files
rm -rf schema-files/* sitemaps/* ai-sitemap.xml test_report.*

# Reset to original state
git checkout -- data/client-data.xlsx
```
