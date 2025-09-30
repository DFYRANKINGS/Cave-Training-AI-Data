// google_sheet_push_xlsx_to_github.js
//
// This Google Apps Script exports the entire active spreadsheet as an
// Excel workbook (.xlsx) and commits it to a GitHub repository.  It
// should be attached to your Google Sheets template when using the
// multi‑tab XLSX workflow.  The exported file preserves all tabs in
// your workbook, allowing the downstream Python script to read
// multiple sheets and generate the corresponding YAML/JSON files.
//
// ### How to use this script
//
// 1. Open your Google Sheet and choose **Extensions → Apps Script**.
// 2. Delete any existing code and paste the contents of this file.
// 3. Replace the values of GH_OWNER, GH_REPO, GH_BRANCH, and
//    FILE_PATH to match your GitHub repository details.  FILE_PATH
//    should point to the desired location of the Excel file inside
//    your repo (e.g. 'data/client-data.xlsx').
// 4. Go to **Project Settings** → **Script Properties**, click
//    **Add Script Property**, and create a property named `GH_TOKEN`
//    whose value is your personal access token with `contents:write`
//    permission for the target repository.
// 5. Save the script.  Reload the spreadsheet.  A menu labelled
//    `GitHub` will appear.  Choose **GitHub → Commit XLSX to
//    GitHub** whenever you want to push the current workbook to
//    GitHub.
//
// When invoked, the script downloads the workbook as a .xlsx file,
// encodes it in base64, and uses the GitHub REST API to either
// create or update the file in your repository.  It handles both
// initial uploads and subsequent updates by retrieving the file's
// current SHA.

// === CONFIGURE THESE CONSTANTS ===
const GH_OWNER  = 'your-github-username-or-org'; // e.g. 'example' or 'example-org'
const GH_REPO   = 'your-client-repo';            // repository name, e.g. 'client-website'
const GH_BRANCH = 'main';                        // branch to push to
const FILE_PATH = 'data/client-data.xlsx';       // path inside the repo

/**
 * Adds a custom menu to the spreadsheet for committing the workbook.
 */
function onOpen() {
  SpreadsheetApp.getUi()
    .createMenu('GitHub')
    .addItem('Commit XLSX to GitHub', 'pushXlsxToGithub')
    .addToUi();
}

/**
 * Export the entire spreadsheet as an XLSX blob.  Uses the
 * undocumented export endpoint.  Requires OAuth for the current
 * user (ScriptApp.getOAuthToken).  See
 * https://spreadsheet.dev/comprehensive-guide-export-google-sheets-to-pdf-excel-csv-apps-script
 * for more details on how this works.
 *
 * @return {Blob} An XLSX file representing the current spreadsheet.
 */
function exportSpreadsheetToXlsx() {
  const ss = SpreadsheetApp.getActive();
  const exportUrl = `https://docs.google.com/spreadsheets/d/${ss.getId()}/export?format=xlsx`;
  const params = {
    method: 'get',
    headers: { Authorization: 'Bearer ' + ScriptApp.getOAuthToken() },
    muteHttpExceptions: true
  };
  const response = UrlFetchApp.fetch(exportUrl, params);
  const blob = response.getBlob();
  // Rename the blob to give it a meaningful filename
  blob.setName(ss.getName() + '.xlsx');
  return blob;
}

/**
 * Retrieve the SHA of a file on GitHub if it exists.  This allows
 * updates to existing files rather than creating duplicates.
 *
 * @param {string} token GitHub personal access token.
 * @return {string|null} SHA of the file at FILE_PATH or null if not found.
 */
function getFileSha(token) {
  const url = `https://api.github.com/repos/${GH_OWNER}/${GH_REPO}/contents/${FILE_PATH}?ref=${GH_BRANCH}`;
  const options = {
    method: 'get',
    headers: { Authorization: 'Bearer ' + token },
    muteHttpExceptions: true
  };
  const response = UrlFetchApp.fetch(url, options);
  if (response.getResponseCode() === 200) {
    return JSON.parse(response.getContentText()).sha;
  }
  return null;
}

/**
 * Commit the current workbook as an XLSX file to GitHub.  If the
 * file already exists, it is updated; otherwise it is created.
 */
function pushXlsxToGithub() {
  const token = PropertiesService.getScriptProperties().getProperty('GH_TOKEN');
  if (!token) {
    SpreadsheetApp.getUi().alert('Please set a script property named GH_TOKEN with your GitHub personal access token.');
    return;
  }
  // Export the entire spreadsheet to XLSX
  const xlsxBlob = exportSpreadsheetToXlsx();
  const xlsxBytes = xlsxBlob.getBytes();
  const contentB64 = Utilities.base64Encode(xlsxBytes);
  const sha = getFileSha(token);
  const url = `https://api.github.com/repos/${GH_OWNER}/${GH_REPO}/contents/${FILE_PATH}`;
  const body = {
    message: 'Update client workbook',
    content: contentB64,
    branch: GH_BRANCH
  };
  if (sha) body.sha = sha;
  const options = {
    method: 'put',
    contentType: 'application/json',
    headers: { Authorization: 'Bearer ' + token },
    payload: JSON.stringify(body),
    muteHttpExceptions: true
  };
  const response = UrlFetchApp.fetch(url, options);
  Logger.log(response.getContentText());
}