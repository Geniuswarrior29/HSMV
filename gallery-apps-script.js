function doPost(e) {
  try {
    var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
    var action = e.parameter.action;
    
    if (action === 'uploadPhoto') {
      var date = e.parameter.date || new Date().toISOString().split('T')[0];
      var description = e.parameter.description || '';
      var fileData = e.parameter.fileData; // base64
      var fileName = e.parameter.fileName;
      var mimeType = e.parameter.mimeType;
      
      // Get or create Drive folder
      var folder;
      var folders = DriveApp.getFoldersByName("HSMV Gallery");
      if (folders.hasNext()) {
        folder = folders.next();
      } else {
        folder = DriveApp.createFolder("HSMV Gallery");
        folder.setSharing(DriveApp.Access.ANYONE_WITH_LINK, DriveApp.Permission.VIEW);
      }
      
      // Decode base64 and create file
      var decodedData = Utilities.base64Decode(fileData);
      var blob = Utilities.newBlob(decodedData, mimeType, fileName);
      var file = folder.createFile(blob);
      
      // Ensure file is publicly accessible
      file.setSharing(DriveApp.Access.ANYONE_WITH_LINK, DriveApp.Permission.VIEW);
      
      var fileId = file.getId();
      var imageUrl = "https://drive.google.com/uc?export=view&id=" + fileId;
      var downloadUrl = "https://drive.google.com/uc?export=download&id=" + fileId;
      
      // Save to sheet
      sheet.appendRow([fileId, date, description, imageUrl, downloadUrl, new Date()]);
      
      return ContentService.createTextOutput(JSON.stringify({"result": "success", "fileId": fileId}))
        .setMimeType(ContentService.MimeType.JSON);
        
    } else if (action === 'getPhotos') {
      var data = sheet.getDataRange().getValues();
      var photos = [];
      
      var startIndex = (data.length > 0 && data[0][0] === 'File ID') ? 1 : 0;
      
      for (var i = startIndex; i < data.length; i++) {
        var row = data[i];
        if (!row[0]) continue;
        
        photos.push({
          id: row[0],
          date: row[1],
          description: row[2],
          imageUrl: row[3],
          downloadUrl: row[4],
          uploadTimestamp: row[5]
        });
      }
      
      return ContentService.createTextOutput(JSON.stringify({"result": "success", "photos": photos}))
        .setMimeType(ContentService.MimeType.JSON);
        
    } else if (action === 'deletePhoto') {
      var idToDelete = e.parameter.id;
      var data = sheet.getDataRange().getValues();
      var rowIndex = -1;
      
      var startIndex = (data.length > 0 && data[0][0] === 'File ID') ? 1 : 0;
      
      for (var i = startIndex; i < data.length; i++) {
        if (data[i][0] === idToDelete) {
          rowIndex = i + 1;
          break;
        }
      }
      
      if (rowIndex !== -1) {
        sheet.deleteRow(rowIndex);
        
        // Optionally delete from Drive too
        try {
          var file = DriveApp.getFileById(idToDelete);
          file.setTrashed(true);
        } catch (e) {
          // Ignore if file doesn't exist
        }
        
        return ContentService.createTextOutput(JSON.stringify({"result": "success", "message": "Photo deleted"}))
          .setMimeType(ContentService.MimeType.JSON);
      } else {
        return ContentService.createTextOutput(JSON.stringify({"result": "error", "error": "Photo not found"}))
          .setMimeType(ContentService.MimeType.JSON);
      }
    }
    
    return ContentService.createTextOutput(JSON.stringify({"result": "error", "error": "Invalid action"}))
      .setMimeType(ContentService.MimeType.JSON);
      
  } catch (error) {
    return ContentService.createTextOutput(JSON.stringify({"result": "error", "error": error.toString()}))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

function doGet(e) {
  return doPost(e);
}

function setup() {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  sheet.appendRow(['File ID', 'Date', 'Description', 'Image URL', 'Download URL', 'Upload Timestamp']);
}
