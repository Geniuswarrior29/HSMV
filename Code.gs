var FOLDER_NAME = "HSMV_Uploads";

function getFolder() {
  var folders = DriveApp.getFoldersByName(FOLDER_NAME);
  if (folders.hasNext()) return folders.next();
  return DriveApp.createFolder(FOLDER_NAME);
}

function saveFileToDrive(base64Data, filename) {
  if (!base64Data) return "";
  try {
    var folder = getFolder();
    var split = base64Data.split(',');
    var data = split[1] || split[0];
    var contentType = (split[0].match(/:(.*?);/) || [])[1] || 'image/jpeg';
    var blob = Utilities.newBlob(Utilities.base64Decode(data), contentType, filename);
    var file = folder.createFile(blob);
    file.setSharing(DriveApp.Access.ANYONE_WITH_LINK, DriveApp.Permission.VIEW);
    return file.getUrl();
  } catch (e) {
    return "";
  }
}

function getSheet(sheetName, headers) {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sheet = ss.getSheetByName(sheetName);
  if (!sheet) {
    sheet = ss.insertSheet(sheetName);
    sheet.appendRow(headers);
    sheet.getRange(1, 1, 1, headers.length).setFontWeight("bold").setBackground("#f3f3f3");
    sheet.setFrozenRows(1);
  } else {
    // If sheet exists, check if headers need expansion (for older sheets)
    var currentHeaders = sheet.getRange(1, 1, 1, sheet.getLastColumn() || 1).getValues()[0];
    if (currentHeaders.length < headers.length) {
       for(var i = currentHeaders.length; i < headers.length; i++) {
          sheet.getRange(1, i+1).setValue(headers[i]);
          sheet.getRange(1, i+1).setFontWeight("bold").setBackground("#f3f3f3");
       }
    }
  }
  return sheet;
}

// Ye function form submission ko handle karega (Images + Data)
function doPost(e) {
  var response = { status: "error", message: "Unknown error" };
  try {
    var payloadStr = e.parameter.payload;
    if (!payloadStr) {
      var postData = e.postData && e.postData.contents;
      if(postData) payloadStr = postData;
    }
    
    var data = JSON.parse(payloadStr);
    var action = data.action;

    // --- STUDENT & MEMBER REGISTRATION ---
    if (action === "register" || action === "register_student") {
      var isStudent = (action === "register_student");
      var sheetName = isStudent ? "Students" : "Members";
      var headers = isStudent ? 
        ["memberId", "name", "phone", "email", "college", "fatherName", "address", "aadhar", "pan", "password", "photo", "paymentScreenshot", "status", "submittedAt", "referralCode", "referralId", "referralName", "paymentStatus"] :
        ["memberId", "name", "phone", "email", "dob", "bloodGroup", "fatherName", "address", "aadhar", "pan", "post", "joiningDate", "password", "photo", "paymentScreenshot", "status", "submittedAt"];
      
      var sheet = getSheet(sheetName, headers);
      var mid = data.memberId || ("M-" + Date.now());
      var timestamp = data.submittedAt || new Date().toISOString();
      
      var photoUrl = data.photo ? saveFileToDrive(data.photo, mid + "_photo.jpg") : "";
      var ssUrl = data.paymentScreenshot ? saveFileToDrive(data.paymentScreenshot, mid + "_payment.jpg") : "";
      
      // Look up referral data if student
      var refCode = isStudent ? (data.referralCode || "") : "";
      var refId = "";
      var refName = "";

      if(isStudent && refCode) {
        var refSheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("ReferralMembers");
        if(refSheet) {
          var refData = refSheet.getDataRange().getValues();
          for(var r=1; r<refData.length; r++) {
            if(refData[r][9] === refCode) { 
               refId = refData[r][0];
               refName = refData[r][1];
               break;
            }
          }
        }
      }

      var row = [];
      for (var i = 0; i < headers.length; i++) {
        var field = headers[i];
        if (field === "photo") row.push(photoUrl);
        else if (field === "paymentScreenshot") row.push(ssUrl);
        else if (field === "status") row.push("pending");
        else if (field === "memberId") row.push(mid);
        else if (field === "submittedAt") row.push(timestamp);
        else if (field === "referralCode") row.push(refCode);
        else if (field === "referralId") row.push(refId);
        else if (field === "referralName") row.push(refName);
        else if (field === "paymentStatus") row.push(data.paymentStatus || "Pending Verification");
        else row.push(data[field] || "");
      }
      
      sheet.appendRow(row);
      
      // Update mapping sheet if referred
      if(isStudent && refCode && refId) {
         var mapSheet = getSheet("ReferralStudents", [
          "Referral ID", "Referral Person Name", "Referral Code", "Student ID", 
          "Student Name", "Student Mobile Number", "Student Email", 
          "Student Registration Date", "Student Approval Status", "Student Approval Date", 
          "Payment Verification Status", "Referral Amount", "Payment Status", "Remarks"
         ]);
         
         mapSheet.appendRow([
            refId, refName, refCode, mid, data.name, data.phone, data.email, timestamp, "pending", "", "Pending Verification", 50, "Pending", ""
         ]);
         
         updateReferralCount(refCode);
      }
      
      response = { status: "success", memberId: mid };
    }
    
    // --- REFERRAL REGISTRATION ---
    else if (action === "register_referral") {
      var sheet = getSheet("ReferralMembers", [
          "Referral ID", "Full Name", "First Name", "Mobile Number", "WhatsApp Number", 
          "Email", "DOB", "Address", "Registration Date", "Referral Code", 
          "Total Students", "Approved Students", "Pending Students", "Rejected Students", 
          "Total Earnings", "Paid Amount", "Pending Amount", "Payment Status", 
          "Account Status", "Password"
      ]);
      
      var lastRow = sheet.getLastRow();
      var newId = "REF" + (lastRow === 1 ? "001" : lastRow);
      var rDate = new Date().toISOString().split('T')[0];

      sheet.appendRow([
        newId, data.fullname, data.firstname, data.mobile, data.whatsapp, data.email, data.dob, 
        data.address + ", " + data.city + ", " + data.district + ", " + data.state, 
        rDate, data.referralCode, 
        0, 0, 0, 0, 
        0, 0, 0, 
        "Active", "Active", data.password
      ]);
      
      response = { status: "success", refCode: data.referralCode };
    }
    
  } catch(err) {
    response = { status: "error", message: err.message };
  }
  
  return ContentService.createTextOutput(JSON.stringify(response)).setMimeType(ContentService.MimeType.JSON);
}

// Ye function Admin panel mein data dikhane aur status approve/reject karne ke kaam aayega
function doGet(e) {
  var action = e.parameter.action;
  var response = { status: "error", message: "Unknown action" };
  
  try {
    if (action === "get_members" || action === "get_students") {
      var isStudent = (action === "get_students");
      var sheetName = isStudent ? "Students" : "Members";
      var ss = SpreadsheetApp.getActiveSpreadsheet();
      var sheet = ss.getSheetByName(sheetName);
      
      var data = [];
      if (sheet) {
        var rows = sheet.getDataRange().getDisplayValues();
        var headers = rows[0];
        for (var i = 1; i < rows.length; i++) {
          var obj = {};
          for (var j = 0; j < headers.length; j++) {
            obj[headers[j]] = rows[i][j];
          }
          data.push(obj);
        }
      }
      response = { status: "success", data: data };
      
    } else if (action === "update_status" || action === "update_student_status") {
      var isStudent = (action === "update_student_status");
      var sheetName = isStudent ? "Students" : "Members";
      var ss = SpreadsheetApp.getActiveSpreadsheet();
      var sheet = ss.getSheetByName(sheetName);
      
      if (!sheet) throw new Error("Sheet not found");
      
      var rows = sheet.getDataRange().getValues();
      var headers = rows[0];
      var idIndex = headers.indexOf("memberId");
      var statusIndex = headers.indexOf("status");
      var refCodeIndex = headers.indexOf("referralCode");
      
      var found = false;
      var changedRefCode = "";
      
      for (var i = 1; i < rows.length; i++) {
        if (rows[i][idIndex] === e.parameter.memberId) {
          sheet.getRange(i + 1, statusIndex + 1).setValue(e.parameter.newStatus);
          
          if(isStudent && refCodeIndex !== -1) {
             changedRefCode = rows[i][refCodeIndex];
          }
          found = true;
          break;
        }
      }
      
      if(found) {
         if(isStudent && changedRefCode) {
            var mapSheet = ss.getSheetByName("ReferralStudents");
            if(mapSheet) {
               var mapRows = mapSheet.getDataRange().getValues();
               for(var m=1; m<mapRows.length; m++) {
                  if(mapRows[m][3] === e.parameter.memberId) { 
                     mapSheet.getRange(m+1, 9).setValue(e.parameter.newStatus); 
                     if (e.parameter.newStatus === "approved") {
                        mapSheet.getRange(m+1, 10).setValue(new Date().toISOString().split('T')[0]);
                     }
                     break;
                  }
               }
            }
            updateReferralCount(changedRefCode);
         }
         response = { status: "success" };
      }
      else throw new Error("Record not found");
      
    } else if (action === "verify_referral_login") {
       var ss = SpreadsheetApp.getActiveSpreadsheet();
       var sheet = ss.getSheetByName("ReferralMembers");
       if (!sheet) {
           response = { status: "success", valid: false };
       } else {
           var data = sheet.getDataRange().getValues();
           var valid = false;
           var rName = "";
           for(var i=1; i<data.length; i++) {
              if(data[i][9] === e.parameter.code && data[i][19] === e.parameter.pass) { 
                 valid = true; rName = data[i][1]; break;
              }
           }
           response = { status: "success", valid: valid, name: rName };
       }
       
    } else if (action === "get_referral_dashboard") {
       var code = e.parameter.code;
       var ss = SpreadsheetApp.getActiveSpreadsheet();
       
       var mapSheet = ss.getSheetByName("ReferralStudents");
       var data = mapSheet ? mapSheet.getDataRange().getValues() : [];
       var myStudents = [];
       for(var i=1; i<data.length; i++) {
          if(data[i][2] === code) {
             myStudents.push({ id: data[i][3], name: data[i][4], mobile: data[i][5], date: data[i][7], status: data[i][8], paymentStatus: data[i][10], earning: data[i][11] });
          }
       }
       
       var refSheet = ss.getSheetByName("ReferralMembers");
       var refData = refSheet ? refSheet.getDataRange().getValues() : [];
       var summary = {};
       for(var i=1; i<refData.length; i++) {
          if(refData[i][9] === code) {
             summary = { total: refData[i][10], approved: refData[i][11], pending: refData[i][12], totalEarning: refData[i][14], paidAmount: refData[i][15] };
             break;
          }
       }
       response = { status: "success", students: myStudents, summary: summary };
       
    } else if (action === "get_referral_admin_data") {
       var ss = SpreadsheetApp.getActiveSpreadsheet();
       var refSheet = ss.getSheetByName("ReferralMembers");
       var mapSheet = ss.getSheetByName("ReferralStudents");
       
       var partners = [];
       if(refSheet) {
         var pData = refSheet.getDataRange().getValues();
         for(var i=1; i<pData.length; i++) {
            partners.push({
               id: pData[i][0], name: pData[i][1], mobile: pData[i][3], regDate: pData[i][8], code: pData[i][9],
               totStudents: pData[i][10], appStudents: pData[i][11], penStudents: pData[i][12], totEarning: pData[i][14], paidAmt: pData[i][15]
            });
         }
       }
       var students = [];
       if(mapSheet) {
         var sData = mapSheet.getDataRange().getValues();
         for(var i=1; i<sData.length; i++) {
            students.push({
               refId: sData[i][0], refName: sData[i][1], refCode: sData[i][2], id: sData[i][3], name: sData[i][4], mobile: sData[i][5], date: sData[i][7], status: sData[i][8], paymentStatus: sData[i][10], earning: sData[i][11]
            });
         }
       }
       response = { status: "success", partners: partners, students: students };
    }
  } catch(err) {
    response = { status: "error", message: err.message };
  }
  
  return ContentService.createTextOutput(JSON.stringify(response)).setMimeType(ContentService.MimeType.JSON);
}

function updateReferralCount(refCode) {
  if(!refCode) return;
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var mapSheet = ss.getSheetByName("ReferralStudents");
  var refSheet = ss.getSheetByName("ReferralMembers");
  if(!mapSheet || !refSheet) return;
  
  var mapData = mapSheet.getDataRange().getValues();
  var total = 0, app = 0, pen = 0, rej = 0;
  var totalEarnings = 0;
  
  for(var i=1; i<mapData.length; i++) {
     if(mapData[i][2] === refCode) {
        total++;
        var st = mapData[i][8]; 
        var amount = parseInt(mapData[i][11]) || 50; 
        if(st === "approved") { app++; totalEarnings += amount; }
        else if(st === "pending") pen++;
        else if(st === "rejected") rej++;
     }
  }
  
  var refData = refSheet.getDataRange().getValues();
  for(var i=1; i<refData.length; i++) {
     if(refData[i][9] === refCode) {
        refSheet.getRange(i+1, 11).setValue(total);
        refSheet.getRange(i+1, 12).setValue(app);
        refSheet.getRange(i+1, 13).setValue(pen);
        refSheet.getRange(i+1, 14).setValue(rej);
        refSheet.getRange(i+1, 15).setValue(totalEarnings);
        
        var paidAmount = parseInt(refData[i][15]) || 0; 
        refSheet.getRange(i+1, 17).setValue(totalEarnings - paidAmount); 
        break;
     }
  }
}
