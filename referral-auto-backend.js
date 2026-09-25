// =======================================================
// PASTE THIS INSIDE YOUR doPost(e) FUNCTION AT THE END
// =======================================================

    var data = null;
    try {
      var payloadStr = e.parameter.payload || (e.postData ? e.postData.contents : null);
      if(payloadStr) data = JSON.parse(payloadStr);
    } catch(err) {}

    if (data && data.action === "register_referral") {
      var ss = SpreadsheetApp.getActiveSpreadsheet();
      var sheet = ss.getSheetByName("ReferralMembers");
      
      // AUTO-CREATE SHEET AND HEADERS IF IT DOESN'T EXIST
      if (!sheet) {
        sheet = ss.insertSheet("ReferralMembers");
        sheet.appendRow([
          "Referral ID", "Full Name", "First Name", "Mobile Number", "WhatsApp Number", 
          "Email", "DOB", "Address", "Registration Date", "Referral Code", 
          "Total Students", "Approved Students", "Pending Students", "Rejected Students", 
          "Total Earnings", "Paid Amount", "Pending Amount", "Payment Status", 
          "Account Status", "Password"
        ]);
        // Format headers
        sheet.getRange("A1:T1").setFontWeight("bold").setBackground("#f3f3f3");
        sheet.setFrozenRows(1);
      }
      
      // AUTO-CREATE ReferralStudents SHEET IF IT DOESN'T EXIST
      var mapSheet = ss.getSheetByName("ReferralStudents");
      if (!mapSheet) {
        mapSheet = ss.insertSheet("ReferralStudents");
        mapSheet.appendRow([
          "Referral ID", "Referral Person Name", "Referral Code", "Student ID", 
          "Student Name", "Student Mobile Number", "Student Email", 
          "Student Registration Date", "Student Approval Status", "Student Approval Date", 
          "Payment Verification Status", "Referral Amount", "Payment Status", "Remarks"
        ]);
        mapSheet.getRange("A1:N1").setFontWeight("bold").setBackground("#f3f3f3");
        mapSheet.setFrozenRows(1);
      }
      
      var lastRow = sheet.getLastRow();
      var newId = "REF" + (lastRow === 1 ? "001" : lastRow);
      var rDate = new Date().toISOString().split('T')[0];

      // Add Data
      sheet.appendRow([
        newId, data.fullname, data.firstname, data.mobile, data.whatsapp, data.email, data.dob, 
        data.address + ", " + data.city + ", " + data.district + ", " + data.state, 
        rDate, data.referralCode, 
        0, 0, 0, 0, // Students: Total, Approved, Pending, Rejected
        0, 0, 0, // Earnings: Total, Paid, Pending
        "Active", "Active", data.password
      ]);

      return ContentService.createTextOutput(JSON.stringify({status: "success", refCode: data.referralCode}))
        .setMimeType(ContentService.MimeType.JSON);
    }

// =======================================================
// PASTE THIS INSIDE YOUR doGet(e) FUNCTION AT THE START
// =======================================================

  if (e.parameter.action === "verify_referral_login") {
     var code = e.parameter.code;
     var pass = e.parameter.pass;
     var ss = SpreadsheetApp.getActiveSpreadsheet();
     var sheet = ss.getSheetByName("ReferralMembers");
     if (!sheet) return ContentService.createTextOutput(JSON.stringify({status: "success", valid: false})).setMimeType(ContentService.MimeType.JSON);
     
     var data = sheet.getDataRange().getValues();
     for(var i=1; i<data.length; i++) {
        if(data[i][9] === code && data[i][19] === pass) { 
           return ContentService.createTextOutput(JSON.stringify({status: "success", valid: true, name: data[i][1]})).setMimeType(ContentService.MimeType.JSON);
        }
     }
     return ContentService.createTextOutput(JSON.stringify({status: "success", valid: false})).setMimeType(ContentService.MimeType.JSON);
  }
  
  if (e.parameter.action === "get_referral_dashboard") {
     var code = e.parameter.code;
     var ss = SpreadsheetApp.getActiveSpreadsheet();
     
     // 1. Get Students
     var mapSheet = ss.getSheetByName("ReferralStudents");
     var data = mapSheet ? mapSheet.getDataRange().getValues() : [];
     var myStudents = [];
     for(var i=1; i<data.length; i++) {
        if(data[i][2] === code) {
           myStudents.push({ id: data[i][3], name: data[i][4], mobile: data[i][5], date: data[i][7], status: data[i][8], paymentStatus: data[i][10], earning: data[i][11] });
        }
     }
     
     // 2. Get Summary from ReferralMembers
     var refSheet = ss.getSheetByName("ReferralMembers");
     var refData = refSheet ? refSheet.getDataRange().getValues() : [];
     var summary = {};
     for(var i=1; i<refData.length; i++) {
        if(refData[i][9] === code) {
           summary = { total: refData[i][10], approved: refData[i][11], pending: refData[i][12], totalEarning: refData[i][14], paidAmount: refData[i][15] };
           break;
        }
     }
     return ContentService.createTextOutput(JSON.stringify({status: "success", students: myStudents, summary: summary})).setMimeType(ContentService.MimeType.JSON);
  }

  if (e.parameter.action === "get_referral_admin_data") {
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
             refId: sData[i][0], refName: sData[i][1], refCode: sData[i][2],
             id: sData[i][3], name: sData[i][4], mobile: sData[i][5], date: sData[i][7],
             status: sData[i][8], paymentStatus: sData[i][10], earning: sData[i][11]
          });
       }
     }
     
     return ContentService.createTextOutput(JSON.stringify({status: "success", partners: partners, students: students})).setMimeType(ContentService.MimeType.JSON);
  }
