import re
import codecs

# Read the files
with codecs.open('card-generator.html', 'r', 'utf-8') as f:
    card_html_full = f.read()

with codecs.open('letter-generator.html', 'r', 'utf-8') as f:
    letter_html_full = f.read()

with codecs.open('member-login.html', 'r', 'utf-8') as f:
    member_login = f.read()

# Extract Card CSS
card_css_match = re.search(r'(/\* ID CARD CONTAINER VISUALS \*/.*?)</style>', card_html_full, re.DOTALL)
card_css = card_css_match.group(1) if card_css_match else ""

# Remove print media queries that hide stuff in card css
card_css = re.sub(r'@media print \{.*?\}', '', card_css, flags=re.DOTALL)

# Extract Letter CSS
letter_css_match = re.search(r'(/\* ================= APPOINTMENT LETTER DESIGN ================= \*/.*?)</style>', letter_html_full, re.DOTALL)
letter_css = letter_css_match.group(1) if letter_css_match else ""

# Remove print media queries in letter css
letter_css = re.sub(r'@media print \{.*?\}', '', letter_css, flags=re.DOTALL)

# Extract Card HTML
card_html_match = re.search(r'(<!-- ================= FRONT SIDE ================= -->.*?)</div>\s*<!-- LOGIC MANAGEMENT SCRIPT -->', card_html_full, re.DOTALL)
card_html = card_html_match.group(1) if card_html_match else ""

# Extract Letter HTML
letter_html_match = re.search(r'(<!-- ================= APPOINTMENT LETTER PAGE CONTAINER ================= -->.*?)<!-- LOGIC MANAGEMENT SCRIPT -->', letter_html_full, re.DOTALL)
letter_html = letter_html_match.group(1) if letter_html_match else ""

# Build the injected hidden div
injected_html = f"""
<!-- HIDDEN PRINT TEMPLATES -->
<div id="hiddenPrintTemplates" style="display: none; position: absolute; left: -9999px; top: -9999px;">
    <style>
        /* Card Styles */
        {card_css}
        /* Letter Styles */
        {letter_css}
        
        .id-card-wrapper {{ display: flex; flex-direction: column; gap: 20px; }}
    </style>
    
    <div id="hiddenIdCardContainer">
        <div class="id-card-wrapper" id="idCardContent">
            {card_html}
        </div>
    </div>
    
    <div id="hiddenLetterContainer">
        {letter_html}
    </div>
</div>
"""

# Replace head
if 'html2pdf.bundle.min.js' not in member_login:
    member_login = member_login.replace('</head>', '<script src="https://cdnjs.cloudflare.com/ajax/libs/html2pdf.js/0.10.1/html2pdf.bundle.min.js"></script>\n</head>')

# Replace body
member_login = member_login.replace('</body>', injected_html + '\n</body>')

# Update Javascript functions using string replace to be safer
# First let's extract the exact blocks if possible or just use a more careful regex

# We need to replace async function downloadIDCard()
member_login = re.sub(r'async function downloadIDCard\(\)\{.*?(?=\nasync function downloadCertificate\(\)\{)', 
"""async function downloadIDCard(){
  var m = memberData;
  if (!m) return;
  
  document.getElementById("cardName").innerText = m.name || "";
  document.getElementById("cardDesignation").innerText = m.post || "Member";
  document.getElementById("cardBloodGroup").innerText = m.bloodGroup || "-";
  document.getElementById("cardFather").innerText = m.fatherName || "-";
  document.getElementById("cardMobile").innerText = m.phone || "-";
  document.getElementById("cardFooterMobile").innerText = m.phone || "-";
  document.getElementById("cardAddress").innerText = m.address || "-";
  
  if (m.dob) {
    document.getElementById("cardDOB").innerText = m.dob;
  } else {
    document.getElementById("cardDOB").innerText = "-";
  }

  var cardPhoto = document.getElementById("cardPhoto");
  if(m.photo && m.photo.startsWith("data:image")) {
      cardPhoto.src = m.photo;
  } else {
      cardPhoto.src = "data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='100' height='100' viewBox='0 0 24 24'><path fill='%23ccc' d='M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5-4-8-4z'/></svg>";
  }

  var d = new Date();
  var mo = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"];
  var day = (d.getDate()<10?"0":"")+d.getDate();
  var yr = d.getFullYear();
  
  var vFrom = day+"-"+mo[d.getMonth()]+"-"+yr;
  
  document.getElementById("cardValidFrom").innerText = vFrom;
  var nextYr = new Date(d.getFullYear()+1, d.getMonth(), d.getDate()-1);
  document.getElementById("cardValidTo").innerText = (nextYr.getDate()<10?"0":"")+nextYr.getDate()+"-"+mo[nextYr.getMonth()]+"-"+nextYr.getFullYear();
  document.getElementById("cardID").innerText = m.memberId || m.id || "0000";

  var element = document.getElementById('idCardContent');
  document.getElementById('hiddenPrintTemplates').style.display = 'block';

  var opt = {
    margin:       [10, 0, 10, 0],
    filename:     'HSMV-ID-Card-' + (m.memberId || m.id) + '.pdf',
    image:        { type: 'jpeg', quality: 0.98 },
    html2canvas:  { scale: 2, useCORS: true, allowTaint: true },
    jsPDF:        { unit: 'px', format: [400, 1240], orientation: 'portrait' }
  };

  html2pdf().set(opt).from(element).save().then(function() {
      document.getElementById('hiddenPrintTemplates').style.display = 'none';
  });
}
""", member_login, flags=re.DOTALL)

# We need to replace async function downloadJoiningLetter()
member_login = re.sub(r'async function downloadJoiningLetter\(\)\{.*?(?=\n</script>)',
"""async function downloadJoiningLetter(){
  var m = memberData;
  if (!m) return;
  
  document.getElementById("olName").innerText = m.name || "";
  document.getElementById("olDesignation").innerText = m.post || "Member";
  document.getElementById("olFather").innerText = m.fatherName || "-";
  document.getElementById("olID").innerText = m.memberId || m.id || "0000";
  
  var d = new Date();
  var mo = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"];
  var day = (d.getDate()<10?"0":"")+d.getDate();
  var yr = d.getFullYear();
  var issueDate = m.joiningDate ? m.joiningDate : (day+"-"+mo[d.getMonth()]+"-"+yr);
  
  document.getElementById("olDate").innerText = issueDate;
  document.getElementById("olMobile").innerText = m.phone || "-";

  var element = document.querySelector('.offer-letter-page');
  document.getElementById('hiddenPrintTemplates').style.display = 'block';

  var opt = {
    margin:       0,
    filename:     'HSMV-Joining-Letter-' + (m.memberId || m.id) + '.pdf',
    image:        { type: 'jpeg', quality: 0.98 },
    html2canvas:  { scale: 2, useCORS: true, allowTaint: true },
    jsPDF:        { unit: 'px', format: [820, 580], orientation: 'landscape' }
  };

  html2pdf().set(opt).from(element).save().then(function() {
      document.getElementById('hiddenPrintTemplates').style.display = 'none';
  });
}
""", member_login, flags=re.DOTALL)

with codecs.open('member-login.html', 'w', 'utf-8') as f:
    f.write(member_login)

print("Update completed.")
