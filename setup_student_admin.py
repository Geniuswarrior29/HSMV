import re

with open('admin.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Change title and topbar text
content = content.replace("HSMV Admin<small>PORTAL</small>", "Student Admin<small>PORTAL</small>")
content = content.replace("<title>Admin Portal | HSMV Foundation</title>", "<title>Student Admin Portal | HSMV</title>")

# 2. Change the Database View select box to just a static label
new_db_view = '''
  <div class="nav-item" style="border-bottom:1px solid rgba(255,255,255,0.1); margin-bottom: 10px; flex-direction:column; align-items:flex-start;">
    <label style="color:#3498db; font-size:0.75rem; margin-bottom: 5px;">Database: Firebase (Students)</label>
  </div>
'''

content = re.sub(r'<div class="nav-item"[^>]*>\s*<label[^>]*>Database View.*?</select>\s*</div>', new_db_view, content, flags=re.DOTALL)

# 3. Change theme colors from brown/green to blue/dark blue for student portal distinction
content = content.replace("#E8A020", "#3498db") # gold to blue
content = content.replace("#3a7d44", "#9b59b6") # green to purple
content = content.replace("#1a1209", "#111827") # very dark brown to dark gray
content = content.replace("#2d1f05", "#1f2937") # dark brown to gray
content = content.replace("#8a7455", "#6b7280") # light brown to slate
content = content.replace("#f5f0e8", "#f3f4f6") # body background
content = content.replace("#e0d0b0", "#d1d5db") # borders
content = content.replace("#fffdf7", "#ffffff") 
content = content.replace("#255c2e", "#8e44ad") # dark green to dark purple

# 4. Modify the JS to force students mode and remove select listener
content = content.replace('var currentDbType = "members";', 'var currentDbType = "students";')
content = re.sub(r'document.getElementById\("dbViewSelect"\).addEventListener.*?\n\s*\}\);', '', content, flags=re.DOTALL)

content = re.sub(r'var headRow = document\.querySelector\("thead tr"\);\s*if\(headRow && headRow\.children\[4\]\)\s*\{\s*headRow\.children\[4\]\.textContent = currentDbType === "students" \? "College" : "Post";\s*\}', 'var headRow = document.querySelector("thead tr"); if(headRow && headRow.children[4]){ headRow.children[4].textContent = "College"; }', content, flags=re.DOTALL)

content = content.replace('rows += "<td>" + (currentDbType === "students" ? (m.college||"") : (m.post||"")) + "</td>";', 'rows += "<td>" + (m.college||"") + "</td>";')

# 5. Fix the screenshot display in viewMember modal
content = re.sub(r'<a href=\'\"\s*\+\s*m\.paymentScreenshot\s*\+\s*\"\' target=\'_blank\'[^>]*>View Screenshot</a>', '<br><img src=\'\" + m.paymentScreenshot + \"\' style=\'max-width:100%; border-radius:6px; border:2px solid #3498db; margin-top:5px;\'/>', content)

# 6. Remove the export alert restriction since this is strictly students
content = content.replace('  if (currentDbType !== "students") {\n    alert("Export is only available for Student Members (Firebase) right now.");\n    return;\n  }', '')

with open('student-admin.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Created student-admin.html successfully!")
