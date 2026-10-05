function doPost(e) {
  try {
    var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
    
    // Check if it's a new donation submission or an admin action
    var action = e.parameter.action;
    
    if (action === 'submitDonation') {
      var id = 'DON-' + new Date().getTime(); // Generate unique ID
      var timestamp = new Date();
      var donorName = e.parameter.donorName || '';
      var mobileNo = e.parameter.mobileNo || '';
      var email = e.parameter.email || '';
      var address = e.parameter.address || '';
      var items = e.parameter.items || '';
      var status = 'Pending';
      
      sheet.appendRow([id, timestamp, donorName, mobileNo, email, address, items, status]);
      
      return ContentService.createTextOutput(JSON.stringify({"result": "success", "id": id}))
        .setMimeType(ContentService.MimeType.JSON);
        
    } else if (action === 'updateStatus') {
      var idToUpdate = e.parameter.id;
      var newStatus = e.parameter.status; // 'Approve', 'Highlight Approve', or 'Delete'
      
      var data = sheet.getDataRange().getValues();
      var rowIndex = -1;
      
      var startIndex = (data.length > 0 && data[0][0] === 'ID') ? 1 : 0;
      
      for (var i = startIndex; i < data.length; i++) {
        if (data[i][0] === idToUpdate) {
          rowIndex = i + 1; // Google Sheets rows are 1-indexed
          break;
        }
      }
      
      if (rowIndex !== -1) {
        if (newStatus === 'Delete') {
          sheet.deleteRow(rowIndex);
          return ContentService.createTextOutput(JSON.stringify({"result": "success", "message": "Row deleted"}))
            .setMimeType(ContentService.MimeType.JSON);
        } else {
          sheet.getRange(rowIndex, 8).setValue(newStatus); // Status is column H (8th)
          return ContentService.createTextOutput(JSON.stringify({"result": "success", "message": "Status updated"}))
            .setMimeType(ContentService.MimeType.JSON);
        }
      } else {
        return ContentService.createTextOutput(JSON.stringify({"result": "error", "error": "ID not found"}))
          .setMimeType(ContentService.MimeType.JSON);
      }
    } else if (action === 'getDonors') {
      var data = sheet.getDataRange().getValues();
      var donorsList = [];
      
      var startIndex = (data.length > 0 && data[0][0] === 'ID') ? 1 : 0;
      
      for (var i = startIndex; i < data.length; i++) {
        var row = data[i];
        if (!row[0]) continue; // Skip completely empty rows
        
        var status = row[7];
        
        if (status === 'Approve' || status === 'Highlight Approve') {
          donorsList.push({
            id: row[0],
            name: row[2],
            items: row[6],
            status: status
          });
        }
      }
      
      return ContentService.createTextOutput(JSON.stringify({"result": "success", "donors": donorsList}))
        .setMimeType(ContentService.MimeType.JSON);
        
    } else if (action === 'getAllDonations') { // For Admin Portal
      var data = sheet.getDataRange().getValues();
      var donations = [];
      
      var startIndex = (data.length > 0 && data[0][0] === 'ID') ? 1 : 0;
      
      for (var i = startIndex; i < data.length; i++) {
        var row = data[i];
        if (!row[0]) continue; // Skip empty rows
        
        donations.push({
          id: row[0],
          timestamp: row[1],
          name: row[2],
          mobile: row[3],
          email: row[4],
          address: row[5],
          items: row[6],
          status: row[7]
        });
      }
      
      return ContentService.createTextOutput(JSON.stringify({"result": "success", "donations": donations}))
        .setMimeType(ContentService.MimeType.JSON);
    }
    
    return ContentService.createTextOutput(JSON.stringify({"result": "error", "error": "Invalid action"}))
      .setMimeType(ContentService.MimeType.JSON);
      
  } catch (error) {
    return ContentService.createTextOutput(JSON.stringify({"result": "error", "error": error.toString()}))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

function doGet(e) {
  // Can be used to just get data via GET if required, or fallback to doPost for getting data.
  // Actually, for getDonors and getAllDonations, we can use doGet for CORS simplicity.
  return doPost(e); // Simple fallback to handle same logic
}

function setup() {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  sheet.appendRow(['ID', 'Timestamp', 'Donor Name', 'Mobile No', 'Email', 'Address', 'Item Details', 'Status']);
}
