# Google Sheets to GitHub Integration Setup Guide

## Overview

This section covers setting up the Google Apps Script that automatically exports your Google Sheets as an Excel file (.xlsx) and pushes it to your GitHub repository. This enables a seamless workflow where changes in Google Sheets automatically trigger file generation and sitemap updates.

## Prerequisites

- Google account with access to Google Sheets and Google Apps Script
- GitHub account with repository access
- Basic understanding of Google Cloud Console (for API setup)

## Step 1: Create Google Cloud Project for API Access

### 1.1 Enable Required APIs

1. **Go to Google Cloud Console**: Navigate to [console.cloud.google.com](https://console.cloud.google.com)

2. **Create or Select Project**:
   - Click the project dropdown at the top
   - Either create a new project or select an existing one
   - Note: You can use the default project if you don't have specific requirements

3. **Enable Google Apps Script API**:
   - In the left sidebar, click "APIs & Services" → "Library"
   - Search for "Google Apps Script API"
   - Click on it and press "ENABLE"

4. **Enable Google Sheets API** (if not already enabled):
   - Search for "Google Sheets API"
   - Click on it and press "ENABLE"

### 1.2 Configure OAuth Consent Screen

1. **Navigate to OAuth consent screen**:
   - Go to "APIs & Services" → "OAuth consent screen"
   
2. **Select User Type**:
   - Choose "Internal" if you're part of a Google Workspace organization
   - Choose "External" if using a personal Google account

3. **Fill Required Information**:
   ```
   App name: Your App Name (e.g., "Sheets to GitHub Sync")
   User support email: your-email@domain.com
   Developer contact information: your-email@domain.com
   ```

4. **Save and Continue** through all steps (you can skip optional fields for now)

## Step 2: Set Up GitHub Personal Access Token

### 2.1 Create Personal Access Token

1. **Navigate to GitHub Settings**:
   - Go to GitHub.com → Settings → Developer settings → Personal access tokens → Tokens (classic)

2. **Generate New Token**:
   - Click "Generate new token (classic)"
   - Add note: "Google Sheets to GitHub Integration"
   - Set expiration (recommend 1 year maximum for security)

3. **Select Required Scopes**:
   ```
   ✓ repo (Full control of private repositories)
     ✓ repo:status
     ✓ repo_deployment
     ✓ public_repo
     ✓ repo:invite
     ✓ security_events
   ✓ workflow (Update GitHub Action workflows)
   ```

4. **Generate and Save Token**:
   - Click "Generate token"
   - **⚠️ IMPORTANT**: Copy the token immediately - you won't see it again
   - Store it securely (you'll need it in Step 4)

### 2.2 Test Token Access

Verify your token has the right permissions:

```bash
# Replace YOUR_TOKEN with your actual token
curl -H "Authorization: Bearer YOUR_TOKEN" https://api.github.com/user

# Test repository access (replace with your repo)
curl -H "Authorization: Bearer YOUR_TOKEN" https://api.github.com/repos/your-username/your-repo
```

## Step 3: Prepare Your Google Sheet

### 3.1 Create or Open Your Google Sheet

1. **Create New Sheet** or **Open Existing Sheet**
2. **Set Up Column Headers** (use these exact headers for best compatibility):
   ```
   client_name | website | category | tagline | description | business_hours | year_founded | number_of_employees | address | phone | email
   ```

### 3.2 Add Sample Data

Add at least one row of sample data to test the integration:

```
Sample Client | https://sampleclient.com | Technology | "Innovation at Scale" | "Leading tech company" | 9AM-5PM | 2010 | 50 | 123 Main St | 555-0123 | contact@sample.com
```

### 3.3 Important Sheet Requirements

- **Keep it as the active sheet**: The script exports the currently active spreadsheet
- **Multiple sheets supported**: All tabs will be preserved in the exported Excel file
- **Column flexibility**: The system can handle different column names (see troubleshooting section)

## Step 4: Set Up Google Apps Script

### 4.1 Open Apps Script Editor

1. **From your Google Sheet**:
   - Click "Extensions" → "Apps Script"
   - This opens the Apps Script editor in a new tab

2. **Delete existing code**:
   - Select all code in the editor (Ctrl+A)
   - Delete it

### 4.2 Add the Integration Script

1. **Paste the script code**:
   - Copy the entire contents of `google_sheet_push_xlsx_to_github.js`
   - Paste it into the Apps Script editor

2. **Configure the constants** at the top of the script:
   ```javascript
   // === CONFIGURE THESE CONSTANTS ===
   const GH_OWNER  = 'your-github-username';     // Your GitHub username or org
   const GH_REPO   = 'your-repository-name';     // Repository name
   const GH_BRANCH = 'main';                     // Branch to push to
   const FILE_PATH = 'data/client-data.xlsx';    // Path inside the repo
   ```

   **Example Configuration**:
   ```javascript
   const GH_OWNER  = 'johndoe';
   const GH_REPO   = 'client-website';
   const GH_BRANCH = 'main';
   const FILE_PATH = 'data/client-data.xlsx';
   ```

### 4.3 Add GitHub Token as Script Property

1. **Access Project Settings**:
   - Click the gear icon (⚙️) in the left sidebar
   - Click "Script Properties"

2. **Add Script Property**:
   - Click "Add script property"
   - Property name: `GH_TOKEN`
   - Value: Paste your GitHub personal access token from Step 2
   - Click "Save script properties"

### 4.4 Save and Deploy

1. **Save the script**:
   - Press Ctrl+S or click the save icon
   - Give your project a name (e.g., "GitHub Sheets Sync")

2. **Set permissions**:
   - The script will need permissions to access your spreadsheet and make external requests
   - These will be requested when you first run the script

## Step 5: Test the Integration

### 5.1 First Run and Authorization

1. **Refresh your Google Sheet**:
   - Go back to your Google Sheet tab
   - Refresh the page (F5 or Ctrl+R)

2. **Find the GitHub menu**:
   - A new "GitHub" menu should appear in your sheet's menu bar
   - If you don't see it, wait a minute and refresh again

3. **Run the integration**:
   - Click "GitHub" → "Commit XLSX to GitHub"

4. **Grant permissions** (first run only):
   - A dialog will appear asking for permissions
   - Click "Review permissions"
   - Choose your Google account
   - Click "Advanced" → "Go to [Your App Name] (unsafe)" if prompted
   - Click "Allow" for all requested permissions

### 5.2 Verify Success

1. **Check your GitHub repository**:
   - Navigate to your GitHub repository
   - Look for the file at the path you specified (e.g., `data/client-data.xlsx`)
   - The file should appear with a commit message "Update client workbook"

2. **Check Apps Script logs**:
   - In the Apps Script editor, click "Executions" in the left sidebar
   - You should see a successful execution
   - Click on it to see detailed logs

### 5.3 Test Updates

1. **Make a change** in your Google Sheet (edit any cell)
2. **Run the sync again**: "GitHub" → "Commit XLSX to GitHub"
3. **Verify the update** appears in GitHub with a new commit

## Step 6: Automate the Process (Optional)

### 6.1 Set up Triggers for Automatic Sync

1. **In Apps Script editor**:
   - Click "Triggers" (clock icon) in the left sidebar
   - Click "Add Trigger"

2. **Configure trigger**:
   ```
   Choose which function to run: pushXlsxToGithub
   Choose which deployment should run: Head
   Select event source: From spreadsheet
   Select event type: On edit
   ```

3. **Save trigger**:
   - This will automatically sync changes whenever the sheet is edited
   - **⚠️ Warning**: This might create many commits. Consider using "On form submit" or time-based triggers instead

### 6.2 Alternative: Time-based Triggers

For less frequent syncing:

```
Choose which function to run: pushXlsxToGithub
Choose which deployment should run: Head
Select event source: Time-driven
Select type of time based trigger: Day timer
Select time of day: 9am to 10am (or your preferred time)
```

## Troubleshooting Common Issues

### Issue: "Please set a script property named GH_TOKEN"

**Solution**: 
- Ensure you've added the GH_TOKEN script property correctly
- Double-check the token value has no extra spaces
- Verify the token hasn't expired

### Issue: "Export URL returned error"

**Solution**:
- Make sure you have edit permissions on the spreadsheet
- Try refreshing and running again
- Check if the spreadsheet is too large (limit: ~10MB)

### Issue: GitHub API returns 401 Unauthorized

**Solution**:
- Verify your GitHub token is valid and hasn't expired
- Check that your token has the correct repository permissions
- Ensure GH_OWNER and GH_REPO constants match your repository exactly

### Issue: GitHub API returns 404 Not Found

**Solution**:
- Double-check the GH_OWNER and GH_REPO constants
- Ensure your token has access to the specified repository
- Make sure the repository exists and isn't private (unless your token has private repo access)

### Issue: File not appearing in correct location

**Solution**:
- Check the FILE_PATH constant matches your desired location
- Use forward slashes (/) even on Windows
- Don't include a leading slash (use `data/file.xlsx`, not `/data/file.xlsx`)

## Security Best Practices

### 5.1 Token Management

- **Rotate tokens regularly** (every 6-12 months)
- **Use minimal required permissions**
- **Store tokens securely** (never in code or documentation)
- **Revoke unused tokens** immediately

### 5.2 Script Security

- **Review code** before running
- **Limit script sharing** to necessary collaborators only
- **Monitor execution logs** for unusual activity
- **Use time-based triggers sparingly** to avoid excessive API calls

### 5.3 Repository Security

- **Use branch protection** on your main branch if possible
- **Review commits** from automated systems
- **Set up notifications** for repository changes
- **Consider using a dedicated integration branch**

## Next Steps

After successfully setting up the Google Sheets integration:

1. **Proceed to Deployment Instructions** to set up the GitHub Actions workflows
2. **Configure your repository** with the required files and directory structure
3. **Test the complete end-to-end workflow** from Google Sheets to generated files
4. **Set up monitoring** for the automated processes

---

**📝 Note**: Keep this document updated as you make changes to your setup. Share it with team members who need to maintain or replicate the integration.
