/**
 * HSMV Foundation - Google Apps Script Backend Snippets
 * This file contains the updated logic needed for the Referral System.
 * Please copy and merge these functions into your existing Code.gs script in Google Apps Script.
 */

/*
  Required Sheets:
  1. "Students" (Existing - Add columns for Referral Code, Referral ID, Referral Person Name, Payment Status, Remarks, etc.)
  2. "ReferralMembers" (New - Columns: Referral ID, Full Name, First Name, Mobile Number, WhatsApp Number, Email, DOB, Address, Registration Date, Referral Code, Total Students, Approved Students, Pending Students, Rejected Students, Total Earnings, Paid Amount, Pending Amount, Payment Status, Account Status, Password)
  3. "ReferralStudents" (New - Columns: Referral ID, Referral Person Name, Referral Code, Student ID, Student Name, Student Mobile Number, Student Email, Student Registration Date, Student Approval Status, Student Approval Date, Payment Verification Status, Referral Amount, Payment Status, Remarks)
*/

function doPost(e) {
  var payloadStr;
  try {
    // Check if it's sent as x-www-form-urlencoded (from form submission) or pure JSON (fetch POST)
    if (e.postData && e.postData.contents) {
      if (e.parameter && e.parameter.payload) {
        payloadStr = e.parameter.payload;
      } else {
        payloadStr = e.postData.contents;
      }
    } else if (e.parameter && e.parameter.payload) {
      payloadStr = e.parameter.payload;
    }

    var data = JSON.parse(payloadStr);
    
    // EXISTING LOGIC for register_student
    if (data.action === "register_student") {
      var ss = SpreadsheetApp.getActiveSpreadsheet();
      var sheet = ss.getSheetByName("Students");
      
      // Auto-generate ID logic (existing)
      var id = "STU" + (sheet.getLastRow() || 0); 
      
      // Look up referral person details if Referral Code provided
      var refCode = data.referralCode || "";
      var refId = "";
      var refName = "";
      if(refCode) {
         var refSheet = ss.getSheetByName("ReferralMembers");
         var refData = refSheet.getDataRange().getValues();
         for(var i=1; i<refData.length; i++) {
            if(refData[i][9] === refCode) { // Assuming col J (idx 9) is Referral Code
               refId = refData[i][0];
               refName = refData[i][1];
               break;
            }
         }
      }

      sheet.appendRow([
        id, 
        data.name, 
        data.phone, 
        data.email, 
        data.college, 
        data.fatherName, 
        data.address, 
        data.aadhar, 
        data.pan, 
        data.paymentScreenshot, 
        "pending", 
        data.submittedAt,
        refCode,
        refId,
        refName,
        data.paymentStatus || "Pending Verification"
      ]);

      // If referred, add to ReferralStudents mapping sheet
      if(refCode && refId) {
         var mapSheet = ss.getSheetByName("ReferralStudents");
         mapSheet.appendRow([
            refId, refName, refCode, id, data.name, data.phone, data.email, data.submittedAt, "pending", "", "Pending Verification", 0, "Pending", ""
         ]);
         
         // Update referral counts in ReferralMembers sheet
         updateReferralCount(refCode);
      }

      return ContentService.createTextOutput(JSON.stringify({status: "success", id: id}))
        .setMimeType(ContentService.MimeType.JSON);
    }
    
    // NEW LOGIC for register_referral
    if (data.action === "register_referral") {
      var ss = SpreadsheetApp.getActiveSpreadsheet();
      var sheet = ss.getSheetByName("ReferralMembers");
      if(!sheet) return ContentService.createTextOutput(JSON.stringify({status: "error", message: "Sheet not found"}));
      
      var newId = "REF" + (sheet.getLastRow()); // E.g. REF1, REF2
      var rDate = new Date().toISOString().split('T')[0];

      sheet.appendRow([
        newId, data.fullname, data.firstname, data.mobile, data.whatsapp, data.email, data.dob, data.address + ", " + data.city + ", " + data.district + ", " + data.state, 
        rDate, data.referralCode, 
        0, 0, 0, 0, // Students counts: Total, App, Pen, Rej
        0, 0, 0, // Earnings: Total, Paid, Pending
        "Active", "Active", data.password
      ]);

      return ContentService.createTextOutput(JSON.stringify({status: "success", refCode: data.referralCode}))
        .setMimeType(ContentService.MimeType.JSON);
    }

  } catch(e) {
    return ContentService.createTextOutput(JSON.stringify({status: "error", message: e.toString()}))
      .setMimeType(ContentService.MimeType.JSON);
  }
}


function doGet(e) {
  var action = e.parameter.action;
  
  if (action === "verify_referral_login") {
     var code = e.parameter.code;
     var pass = e.parameter.pass;
     var ss = SpreadsheetApp.getActiveSpreadsheet();
     var sheet = ss.getSheetByName("ReferralMembers");
     var data = sheet.getDataRange().getValues();
     for(var i=1; i<data.length; i++) {
        if(data[i][9] === code && data[i][19] === pass) { // Assuming col J=Code, T=Pass
           return ContentService.createTextOutput(JSON.stringify({status: "success", valid: true, name: data[i][1]}))
              .setMimeType(ContentService.MimeType.JSON);
        }
     }
     return ContentService.createTextOutput(JSON.stringify({status: "success", valid: false}))
        .setMimeType(ContentService.MimeType.JSON);
  }
  
  if (action === "get_referral_dashboard") {
     var code = e.parameter.code;
     var ss = SpreadsheetApp.getActiveSpreadsheet();
     var mapSheet = ss.getSheetByName("ReferralStudents");
     var data = mapSheet.getDataRange().getValues();
     
     var myStudents = [];
     for(var i=1; i<data.length; i++) {
        if(data[i][2] === code) {
           myStudents.push({
              id: data[i][3],
              name: data[i][4],
              mobile: data[i][5],
              date: data[i][7],
              status: data[i][8],
              paymentStatus: data[i][10],
              earning: data[i][11]
           });
        }
     }
     
     var refSheet = ss.getSheetByName("ReferralMembers");
     var refData = refSheet.getDataRange().getValues();
     var summary = {};
     for(var i=1; i<refData.length; i++) {
        if(refData[i][9] === code) {
           summary = {
              total: refData[i][10],
              approved: refData[i][11],
              pending: refData[i][12],
              totalEarning: refData[i][14],
              paidAmount: refData[i][15]
           };
           break;
        }
     }
     
     return ContentService.createTextOutput(JSON.stringify({status: "success", students: myStudents, summary: summary}))
        .setMimeType(ContentService.MimeType.JSON);
  }
  
  if (action === "get_referral_admin_data") {
     var ss = SpreadsheetApp.getActiveSpreadsheet();
     var refSheet = ss.getSheetByName("ReferralMembers");
     var mapSheet = ss.getSheetByName("ReferralStudents");
     
     var pData = refSheet.getDataRange().getValues();
     var partners = [];
     for(var i=1; i<pData.length; i++) {
        partners.push({
           id: pData[i][0],
           name: pData[i][1],
           mobile: pData[i][3],
           regDate: pData[i][8],
           code: pData[i][9],
           totStudents: pData[i][10],
           appStudents: pData[i][11],
           penStudents: pData[i][12],
           totEarning: pData[i][14],
           paidAmt: pData[i][15]
        });
     }
     
     var sData = mapSheet.getDataRange().getValues();
     var students = [];
     for(var i=1; i<sData.length; i++) {
        students.push({
           refId: sData[i][0],
           refName: sData[i][1],
           refCode: sData[i][2],
           id: sData[i][3],
           name: sData[i][4],
           mobile: sData[i][5],
           date: sData[i][7],
           status: sData[i][8],
           paymentStatus: sData[i][10],
           earning: sData[i][11]
        });
     }
     
     return ContentService.createTextOutput(JSON.stringify({status: "success", partners: partners, students: students}))
        .setMimeType(ContentService.MimeType.JSON);
  }
  
  // Existing logic for getting students / updating status...
}

function updateReferralCount(refCode) {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var mapSheet = ss.getSheetByName("ReferralStudents");
  var refSheet = ss.getSheetByName("ReferralMembers");
  
  var mapData = mapSheet.getDataRange().getValues();
  var total = 0, app = 0, pen = 0, rej = 0;
  var totalEarnings = 0;
  
  for(var i=1; i<mapData.length; i++) {
     if(mapData[i][2] === refCode) {
        total++;
        var st = mapData[i][8];
        if(st === "approved") { app++; totalEarnings += mapData[i][11]; } // Sum earnings
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
        refSheet.getRange(i+1, 15).setValue(totalEarnings); // Earnings calculation
        break;
     }
  }
}
