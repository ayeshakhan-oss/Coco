/**
 * Sourcing Sheet Helper
 * Manages Google Sheets integration for talent sourcing pipeline tracking
 *
 * Usage:
 *   const helper = require('./sourcing-sheet-helper');
 *   const sheet = await helper.getOrCreateRoleSheet(spreadsheetId, 'product_designer', 'Product Designer');
 *
 * Credentials: Taleemabad Talent Sourcing (agent-coco project)
 * Service Account: taleemabad-sourcing@agent-coco.iam.gserviceaccount.com
 * Master Spreadsheet: 1eFf5ATqDyFvPi0qxgijPCbfrx_AWBvgtnj3ywe4UBNw
 */

const { google } = require('googleapis');
const credentials = require('./agent-coco-914edff20dde.json');

const DEFAULT_SPREADSHEET_ID = '1eFf5ATqDyFvPi0qxgijPCbfrx_AWBvgtnj3ywe4UBNw';

class SourcingSheetHelper {
  constructor() {
    const auth = new google.auth.GoogleAuth({
      credentials: credentials,
      scopes: ['https://www.googleapis.com/auth/spreadsheets']
    });
    this.sheets = google.sheets({ version: 'v4', auth });
  }

  /**
   * Get or create a sheet for a specific role
   * @param {string} spreadsheetId - Google Sheets ID
   * @param {string} roleSlug - Role slug (lowercase, hyphens) e.g., 'product_designer'
   * @param {string} roleTitle - Display title e.g., 'Product Designer'
   */
  async getOrCreateRoleSheet(spreadsheetId, roleSlug, roleTitle) {
    try {
      const spreadsheet = await this.sheets.spreadsheets.get({ spreadsheetId });
      const sheets = spreadsheet.data.sheets || [];

      // Look for existing sheet matching this role
      const existingSheet = sheets.find(s => s.properties.title === roleSlug);

      if (existingSheet) {
        return {
          sheetId: existingSheet.properties.sheetId,
          sheetName: existingSheet.properties.title,
          sheetUrl: `https://docs.google.com/spreadsheets/d/${spreadsheetId}/edit#gid=${existingSheet.properties.sheetId}`,
          created: false
        };
      }

      // Create new sheet
      const addSheetRequest = {
        spreadsheetId,
        resource: {
          requests: [
            {
              addSheet: {
                properties: {
                  title: roleSlug,
                  gridProperties: {
                    rowCount: 1000,
                    columnCount: 12
                  }
                }
              }
            }
          ]
        }
      };

      const response = await this.sheets.spreadsheets.batchUpdate(addSheetRequest);
      const newSheetId = response.data.replies[0].addSheet.properties.sheetId;

      // Add headers
      const headerRow = [
        'Name',
        'LinkedIn URL',
        'Current Role',
        'Current Company',
        'Location',
        'Key Experience',
        'Why Relevant',
        'Panel Fit Signal',
        'Status',
        'DM Sent',
        'Response',
        'Date Added'
      ];

      await this.sheets.spreadsheets.values.update({
        spreadsheetId,
        range: `${roleSlug}!A1:L1`,
        valueInputOption: 'RAW_USER_ENTERED',
        resource: {
          values: [headerRow]
        }
      });

      // Format header row
      await this.sheets.spreadsheets.batchUpdate({
        spreadsheetId,
        resource: {
          requests: [
            {
              repeatCell: {
                range: {
                  sheetId: newSheetId,
                  startRowIndex: 0,
                  endRowIndex: 1
                },
                cell: {
                  userEnteredFormat: {
                    backgroundColor: { red: 0.2, green: 0.3, blue: 0.6 },
                    textFormat: {
                      foregroundColor: { red: 1, green: 1, blue: 1 },
                      bold: true
                    }
                  }
                },
                fields: 'userEnteredFormat(backgroundColor,textFormat)'
              }
            }
          ]
        }
      });

      return {
        sheetId: newSheetId,
        sheetName: roleSlug,
        sheetUrl: `https://docs.google.com/spreadsheets/d/${spreadsheetId}/edit#gid=${newSheetId}`,
        created: true
      };
    } catch (error) {
      console.error('Error in getOrCreateRoleSheet:', error);
      throw error;
    }
  }

  /**
   * Check for duplicate candidates already in the sheet
   * @param {string} spreadsheetId
   * @param {string} sheetName
   * @param {Array} candidates - Array of candidate objects with {name, linkedinUrl}
   * @returns {Object} { newCandidates, skippedCount, duplicates }
   */
  async checkDuplicates(spreadsheetId, sheetName, candidates) {
    try {
      const response = await this.sheets.spreadsheets.values.get({
        spreadsheetId,
        range: `${sheetName}!A2:B1000`
      });

      const existingRows = response.data.values || [];
      const existingUrls = new Set(existingRows.map(row => row[1]?.toLowerCase() || ''));
      const existingNames = new Set(existingRows.map(row => row[0]?.toLowerCase() || ''));

      const newCandidates = [];
      const duplicates = [];

      for (const candidate of candidates) {
        const urlLower = (candidate.linkedinUrl || '').toLowerCase();
        const nameLower = (candidate.name || '').toLowerCase();

        if (existingUrls.has(urlLower) || existingNames.has(nameLower)) {
          duplicates.push(candidate);
        } else {
          newCandidates.push(candidate);
        }
      }

      return {
        newCandidates,
        skippedCount: duplicates.length,
        duplicates,
        totalInSheet: existingRows.length
      };
    } catch (error) {
      console.error('Error in checkDuplicates:', error);
      throw error;
    }
  }

  /**
   * Add candidates to sheet
   * @param {string} spreadsheetId
   * @param {string} sheetName
   * @param {Array} candidates - Array of candidate objects
   */
  async addCandidatesToSheet(spreadsheetId, sheetName, candidates) {
    try {
      if (candidates.length === 0) {
        return { rowsAdded: 0, startRow: null };
      }

      // Get current row count to append
      const response = await this.sheets.spreadsheets.values.get({
        spreadsheetId,
        range: `${sheetName}!A:A`
      });

      const existingRows = response.data.values || [];
      const startRow = existingRows.length;

      // Prepare data rows
      const dataRows = candidates.map(c => [
        c.name || '',
        c.linkedinUrl || '',
        c.currentRole || '',
        c.currentCompany || '',
        c.location || '',
        c.keyExperience || '',
        c.whyRelevant || '',
        c.panelFitSignal || '',
        'Identified', // Default status
        'No', // DM Sent
        '', // Response (empty initially)
        new Date().toISOString().split('T')[0] // Date Added
      ]);

      // Append to sheet
      await this.sheets.spreadsheets.values.append({
        spreadsheetId,
        range: `${sheetName}!A${startRow + 1}`,
        valueInputOption: 'RAW_USER_ENTERED',
        resource: {
          values: dataRows
        }
      });

      return {
        rowsAdded: dataRows.length,
        startRow: startRow + 1,
        endRow: startRow + dataRows.length
      };
    } catch (error) {
      console.error('Error in addCandidatesToSheet:', error);
      throw error;
    }
  }

  /**
   * Update candidate status in sheet
   * @param {string} spreadsheetId
   * @param {string} sheetName
   * @param {string} linkedinUrl - Candidate's LinkedIn URL (used to find row)
   * @param {Object} updates - Status updates e.g., { status: 'DM Pending', dmSent: 'Awaiting Ayesha' }
   */
  async updateCandidateStatus(spreadsheetId, sheetName, linkedinUrl, updates) {
    try {
      // Find row matching this LinkedIn URL
      const response = await this.sheets.spreadsheets.values.get({
        spreadsheetId,
        range: `${sheetName}!A2:L1000`
      });

      const rows = response.data.values || [];
      let targetRow = null;

      for (let i = 0; i < rows.length; i++) {
        if (rows[i][1]?.toLowerCase() === linkedinUrl.toLowerCase()) {
          targetRow = i + 2; // +2 because headers are row 1, data starts at row 2
          break;
        }
      }

      if (!targetRow) {
        throw new Error(`Candidate with URL ${linkedinUrl} not found in sheet`);
      }

      // Prepare update cells
      const updateRequests = [];
      const columnMap = {
        'status': 9, // Column I (0-indexed: 8, but 1-indexed: 9)
        'dmSent': 10, // Column J
        'response': 11 // Column K
      };

      for (const [field, value] of Object.entries(updates)) {
        const colIndex = columnMap[field];
        if (colIndex) {
          updateRequests.push({
            updateCells: {
              rows: [{
                values: [{
                  userEnteredValue: { stringValue: String(value) }
                }]
              }],
              fields: 'userEnteredValue',
              range: {
                sheetId: 0, // Assumes first/main sheet
                rowIndex: targetRow - 1,
                columnIndex: colIndex - 1
              }
            }
          });
        }
      }

      if (updateRequests.length > 0) {
        await this.sheets.spreadsheets.batchUpdate({
          spreadsheetId,
          resource: { requests: updateRequests }
        });
      }

      return { updated: true, row: targetRow };
    } catch (error) {
      console.error('Error in updateCandidateStatus:', error);
      throw error;
    }
  }

  /**
   * Get all candidates from a sheet with a specific status
   * @param {string} spreadsheetId
   * @param {string} sheetName
   * @param {string} status - Status to filter by e.g., 'Identified', 'DM Pending', 'Confirmed'
   */
  async getCandidatesByStatus(spreadsheetId, sheetName, status) {
    try {
      const response = await this.sheets.spreadsheets.values.get({
        spreadsheetId,
        range: `${sheetName}!A2:L1000`
      });

      const rows = response.data.values || [];
      const candidates = [];

      rows.forEach(row => {
        if (row[8]?.toLowerCase() === status.toLowerCase()) {
          candidates.push({
            name: row[0],
            linkedinUrl: row[1],
            currentRole: row[2],
            currentCompany: row[3],
            location: row[4],
            keyExperience: row[5],
            whyRelevant: row[6],
            panelFitSignal: row[7],
            status: row[8],
            dmSent: row[9],
            response: row[10],
            dateAdded: row[11]
          });
        }
      });

      return candidates;
    } catch (error) {
      console.error('Error in getCandidatesByStatus:', error);
      throw error;
    }
  }
}

module.exports = SourcingSheetHelper;
