import re

with open('admin.html', 'r', encoding='utf-8') as f:
    content = f.read()

sidebar_addition = """
  <div class="nav-item" style="border-bottom:1px solid rgba(255,255,255,0.1); margin-bottom: 10px; flex-direction:column; align-items:flex-start;">
    <label style="color:#E8A020; font-size:0.7rem; margin-bottom: 5px;">Database View</label>
    <select id="dbViewSelect" style="width:100%; padding:5px; border-radius:4px; background:#2d1f05; color:#fff; border:1px solid #E8A020;">
      <option value="members">Regular Members</option>
      <option value="students">Student Members (Firebase)</option>
    </select>
  </div>
  <div class="nav-item" id="n-all">&#128101; All Records</div>"""

content = content.replace('<div class="nav-item" id="n-all">&#128101; All Members</div>', sidebar_addition)

export_btn = """<div class="sb-foot">
    <button class="btn-lo" id="refreshBtn" style="margin-bottom:8px; background:rgba(58,125,68,0.15); color:#3a7d44; border-color:rgba(58,125,68,0.3);">&#8635; Refresh</button>
    <button class="btn-lo" id="exportBtn">&#128190; Export DB</button>
  </div>"""

content = re.sub(r'<div class="sb-foot">.*?</div>', export_btn, content, flags=re.DOTALL)

firebase_scripts = """
<script src="https://www.gstatic.com/firebasejs/8.10.1/firebase-app.js"></script>
<script src="https://www.gstatic.com/firebasejs/8.10.1/firebase-firestore.js"></script>
<script src="firebase-config.js"></script>
<script>
firebase.initializeApp(FIREBASE_CONFIG);
var db = firebase.firestore();
var currentDbType = "members";

document.getElementById("dbViewSelect").addEventListener("change", function() {
  currentDbType = this.value;
  loadData();
});

document.getElementById("exportBtn").addEventListener("click", async function() {
  if (currentDbType !== "students") {
    alert("Export is only available for Student Members (Firebase) right now.");
    return;
  }
  try {
    sb("Exporting...", null);
    var snap = await db.collection("students").get();
    var data = [];
    snap.forEach(doc => data.push(doc.data()));
    var blob = new Blob([JSON.stringify(data, null, 2)], {type: "application/json"});
    var url = URL.createObjectURL(blob);
    var a = document.createElement("a");
    a.href = url;
    a.download = "students_db_export.json";
    a.click();
    sb("Exported successfully", true);
  } catch(e) {
    sb("Export failed: " + e.message, false);
  }
});
</script>
"""

content = content.replace('<script>', firebase_scripts + '<script>')

# Rewrite loadData to handle student fetch
loadData_replacement = """
function loadData() {
  sb("Loading " + currentDbType + "...", null);
  if (currentDbType === "members") {
    // Use GET to avoid CORS
    fetch(SHEET_URL + "?action=get_members")
    .then(function(r) { return r.json(); })
    .then(function(d) {
      if(d.status !== "success") throw new Error(d.message || "Failed");
      allMembers = d.members || [];
      allMembers.forEach(function(m) { if(!m.id) m.id = m.memberId; });
      sb("Loaded " + allMembers.length + " record(s)", true);
      updateStats();
      renderTable();
      var p = allMembers.filter(function(m) { return m.status === "pending"; }).length;
      document.getElementById("pc").textContent = p || "";
    })
    .catch(function(e) {
      sb("Error: " + e.message, false);
      document.getElementById("tbody").innerHTML = "<tr><td colspan='7' class='empty'>Load failed: " + e.message + "</td></tr>";
    });
  } else {
    // Load from Firebase
    db.collection("students").get().then(function(snap) {
      allMembers = [];
      snap.forEach(function(doc) {
        var data = doc.data();
        data.id = doc.id;
        allMembers.push(data);
      });
      sb("Loaded " + allMembers.length + " student(s)", true);
      updateStats();
      renderTable();
      var p = allMembers.filter(function(m) { return m.status === "pending"; }).length;
      document.getElementById("pc").textContent = p || "";
    }).catch(function(e) {
      sb("Error: " + e.message, false);
      document.getElementById("tbody").innerHTML = "<tr><td colspan='7' class='empty'>Load failed: " + e.message + "</td></tr>";
    });
  }
}
"""

content = re.sub(r'function loadData\(\) \{.*?\n\}', loadData_replacement, content, flags=re.DOTALL)

# Update patchStatus to handle student status updates
patchStatus_replacement = """
function patchStatus(id, status, reason) {
  if (currentDbType === "members") {
    var url = SHEET_URL + "?action=update_status&memberId=" + encodeURIComponent(id) + "&status=" + encodeURIComponent(status) + "&reason=" + encodeURIComponent(reason||"");
    fetch(url)
    .then(function(r) { return r.json(); })
    .then(function(d) {
      if(d.status === "success") {
        alert(status === "approved" ? "Approved!" : "Rejected.");
        loadData();
      } else {
        alert("Error: " + (d.message||"Unknown"));
      }
    })
    .catch(function(e) { alert("Error: " + e.message); });
  } else {
    db.collection("students").doc(id).update({
      status: status,
      reason: reason || ""
    }).then(function() {
      alert(status === "approved" ? "Approved!" : "Rejected.");
      loadData();
    }).catch(function(e) {
      alert("Error: " + e.message);
    });
  }
}
"""

content = re.sub(r'function patchStatus\(id, status, reason\) \{.*?\n\}', patchStatus_replacement, content, flags=re.DOTALL)

# Add Edit and Delete functions to the viewMember modal
viewMember_addition = """
  if(st === "pending") {
    actHtml += "<button class='app-btn' style='padding:9px 18px;font-size:0.8rem;' data-id='" + (m.memberId||m.id) + "' id='modalApproveBtn'>&#10003; Approve</button>";
    actHtml += "<button class='rej-btn' style='padding:9px 18px;font-size:0.8rem;' data-id='" + (m.memberId||m.id) + "' id='modalRejectBtn'>&#10007; Reject</button>";
  } else {
    actHtml = "<span style='font-size:0.78rem;color:#8a7455;margin-right:10px;'>Status: " + st + "</span>";
  }
  if (currentDbType === "students") {
    actHtml += "<button class='viw-btn' style='padding:9px 18px;font-size:0.8rem;' data-id='" + (m.memberId||m.id) + "' id='modalEditBtn'>&#9998; Edit</button>";
    actHtml += "<button class='rej-btn' style='padding:9px 18px;font-size:0.8rem;' data-id='" + (m.memberId||m.id) + "' id='modalDeleteBtn'>&#128465; Delete</button>";
  }
  document.getElementById("mact").innerHTML = actHtml;

  if(st === "pending") {
    document.getElementById("modalApproveBtn").addEventListener("click", function() {
      doApprove(this.getAttribute("data-id"));
      closeModal();
    });
    document.getElementById("modalRejectBtn").addEventListener("click", function() {
      doReject(this.getAttribute("data-id"));
      closeModal();
    });
  }
  if (currentDbType === "students") {
    document.getElementById("modalEditBtn").addEventListener("click", function() {
      var newName = prompt("Edit Name:", m.name);
      if (newName !== null) {
        db.collection("students").doc(m.id).update({name: newName}).then(function() {
          alert("Updated successfully!");
          loadData();
          closeModal();
        });
      }
    });
    document.getElementById("modalDeleteBtn").addEventListener("click", function() {
      if(confirm("Are you sure you want to delete this student record completely?")) {
        db.collection("students").doc(m.id).delete().then(function() {
          alert("Deleted successfully!");
          loadData();
          closeModal();
        });
      }
    });
  }
"""

content = re.sub(r'if\(st === "pending"\) \{.*?\n  \}[\s\n]*document\.getElementById\("modal"\)\.classList\.add\("show"\);', viewMember_addition + '\n  document.getElementById("modal").classList.add("show");', content, flags=re.DOTALL)

with open('admin.html', 'w', encoding='utf-8') as f:
    f.write(content)

