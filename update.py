import re

with open(r'c:\Users\DELL\Downloads\HSMV\member-login.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Replace CSS
css_start = content.find('/* --- INJECTED CARD STYLES --- */')
css_end = content.find('/* --- PRINT STRATEGY --- */')

new_css = """/* --- INJECTED CARD STYLES --- */
:root {
    --primary-orange: #ff9900;
    --primary-green: #008000;
    --dark-bg: #111111;
    --dark-brown: #4a1504;
}

/* ID CARD CONTAINER VISUALS */
.id-card-wrapper {
    display: flex;
    gap: 40px;
    flex-wrap: wrap;
    justify-content: center;
}
.id-card {
    width: 400px;
    height: 600px;
    background: white;
    border-radius: 15px;
    overflow: hidden;
    box-shadow: 0 10px 25px rgba(0,0,0,0.15);
    position: relative;
    display: flex;
    flex-direction: column;
    border: 1px solid #ddd;
    
    /* Forces backgrounds to show when printing/downloading */
    -webkit-print-color-adjust: exact !important;
    print-color-adjust: exact !important;
}

/* Header section layout */
.card-header {
    background: white !important;
    padding: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
    position: relative;
}
.logo-img {
    width: 65px;
    height: 65px;
    object-fit: contain;
    mix-blend-mode: multiply; 
}
.header-title {
    text-align: center;
    color: black;
    font-weight: 900;
    font-size: 16px;
    line-height: 1.2;
    flex: 1;
}
.sub-header-bar {
    display: flex;
    background: var(--primary-green) !important;
    color: white !important;
    font-size: 11px;
    font-weight: bold;
    padding: 4px 10px;
    justify-content: space-between;
    align-items: center;
    -webkit-print-color-adjust: exact !important;
    print-color-adjust: exact !important;
}
.reg-badge {
    background: #ffcc00 !important;
    color: black !important;
    padding: 2px 8px;
    border-radius: 2px;
}

/* Front Card Specifics */
.photo-container {
    margin: 20px auto 10px auto;
    width: 130px;
    height: 160px;
    border: 2px solid red;
    border-radius: 8px;
    background: #eee;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative; 
    overflow: visible;
}
.photo-container img.profile-pic {
    width: 100%;
    height: 100%;
    object-fit: cover;
    border-radius: 6px;
}

/* ================= FIXED: LOWER RIGHT OVERLAY WITH PRECISION CENTERED SIGNATURE ================= */
.photo-overlay-stamp {
    width: 180px; 
    height: 180px;
    position: absolute;
    bottom: -50px; 
    right: -90px;  
    z-index: 10;
    object-fit: contain;
    pointer-events: none;
}
.photo-overlay-sign {
    width: 210px; 
    height: auto;
    position: absolute;
    bottom: -20px; 
    right: -115px; 
    z-index: 11;
    object-fit: contain;
    pointer-events: none;
}

.member-name {
    text-align: center;
    color: red;
    font-size: 22px;
    font-weight: bold;
    text-transform: uppercase;
    margin: 25px 0 0 0; 
}
.member-desig {
    text-align: center;
    font-size: 16px;
    font-weight: bold;
    margin: 2px 0 15px 0;
}

/* Data Fields Style */
.data-table {
    width: 85%;
    margin: 0 auto;
    font-size: 13px;
    border-collapse: collapse;
}
.data-table td {
    padding: 4px 0;
    vertical-align: top;
}
.field-label {
    font-weight: bold;
    color: red;
    width: 110px;
}
.field-label.back-label {
    color: red;
    width: 90px;
}
.field-sep {
    width: 15px;
    font-weight: bold;
}
.field-value {
    font-weight: bold;
    color: #000;
}

/* Back Card Specifics */
.qr-container {
    margin: 20px auto 10px auto;
    width: 120px;
    height: 120px;
    border: 1px solid red;
    padding: 5px;
    display: flex;
    align-items: center;
    justify-content: center;
}
.qr-container img {
    width: 100%;
    height: 100%;
}
.divider-line {
    border-top: 1px solid #ccc;
    margin: 15px 25px;
}
.legal-notice {
    width: 85%;
    margin: 10px auto;
    font-size: 11px;
    font-weight: bold;
    color: red;
}

/* Footer layouts */
.footer-front {
    position: absolute;
    bottom: 0;
    width: 100%;
    height: 45px;
    background: linear-gradient(115deg, transparent 35%, var(--dark-bg) 35.5%) !important;
    display: flex;
    align-items: center;
    justify-content: flex-end;
    padding-right: 20px;
    box-sizing: border-box;
    color: white !important;
    font-weight: bold;
    font-size: 16px;
    -webkit-print-color-adjust: exact !important;
    print-color-adjust: exact !important;
}
.footer-back {
    position: absolute;
    bottom: 0;
    width: 100%;
    height: 55px;
    background: var(--dark-bg) !important;
    color: white !important;
    display: flex;
    align-items: center;
    padding: 0 15px;
    box-sizing: border-box;
    font-size: 10px;
    font-weight: bold;
    line-height: 1.3;
    -webkit-print-color-adjust: exact !important;
    print-color-adjust: exact !important;
}
.footer-back-icon {
    background: #ffcc00 !important;
    color: black !important;
    border-radius: 50%;
    width: 24px;
    height: 24px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-right: 10px;
    font-size: 14px;
}

/* --- INJECTED LETTER STYLES --- */
/* ================= APPOINTMENT LETTER DESIGN ================= */
.offer-letter-page {
    width: 820px;
    height: 580px;
    background: #fffdf6;
    border: 3px solid #b8860b;
    position: relative;
    box-sizing: border-box;
    padding: 25px;
    overflow: hidden;
    box-shadow: 0 10px 25px rgba(0,0,0,0.15);
    display: flex;
    flex-direction: column;
    -webkit-print-color-adjust: exact !important;
    print-color-adjust: exact !important;
}

/* Background Watermark */
.offer-letter-page::before {
    content: "";
    position: absolute;
    top: 52%; left: 50%;
    width: 260px; height: 260px;
    transform: translate(-50%, -50%);
    background: url('https://i.ibb.co/cKssRvxh/Whats-App-Image-2026-06-21-at-15-39-55.jpg') no-repeat center;
    background-size: contain;
    opacity: 0.05;
    pointer-events: none;
}

.ol-main-header {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 15px;
    border-bottom: 2px solid #ffcc00;
    padding-bottom: 5px;
}
.ol-logo { width: 75px; height: 75px; object-fit: contain; mix-blend-mode: multiply; }
.ol-title {
    font-size: 28px;
    font-weight: 900;
    color: var(--dark-brown);
    text-align: center;
    margin: 0;
    letter-spacing: 0.3px;
}
.ol-gov-bar {
    background: var(--primary-green) !important;
    color: white !important;
    display: flex;
    justify-content: space-between;
    padding: 4px 15px;
    font-weight: bold;
    font-size: 13px;
    margin-top: 5px;
}
.ol-meta-grid {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin: 8px 5px;
    font-size: 12px;
    font-weight: bold;
    color: #333;
}
.ol-badge-title {
    background: linear-gradient(90deg, #b8860b, #e67e22) !important;
    color: white !important;
    font-size: 15px;
    font-weight: bold;
    padding: 3px 22px;
    clip-path: polygon(10% 0%, 90% 0%, 100% 50%, 90% 100%, 10% 100%, 0% 50%);
}

.ol-id-date-row {
    display: flex; 
    justify-content: space-between; 
    padding: 0 5px; 
    font-size: 13px; 
    font-weight: bold; 
    margin-bottom: 12px;
}

/* Hindi Content Box */
.ol-body-content {
    padding: 0 5px;
    font-size: 14px;
    line-height: 1.75;
    color: #111;
    text-align: justify;
    font-weight: bold;
    flex: 1;
}
.highlight-red { color: red; font-weight: bold; }

/* Footer Layout */
.ol-footer-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 5px;
    margin-bottom: 35px;
    position: relative;
}
.ol-social-block {
    display: flex;
    align-items: center;
    gap: 12px;
}
.ol-social-icons-box {
    display: flex;
    gap: 4px;
}
.ol-social-icons-box span {
    width: 18px;
    height: 18px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-size: 10px;
    font-weight: 900;
    border-radius: 3px;
}
.icon-fb { background-color: #3b5998; }
.icon-tw { background-color: #1da1f2; }
.icon-yt { background-color: #ff0000; }
.icon-ig { background-color: #e1306c; }

.ol-mob-box {
    background: var(--dark-brown) !important;
    color: white !important;
    font-size: 13px;
    font-weight: bold;
    padding: 4px 15px;
    border-radius: 2px;
}

/* ================= FIXED: SIGNATURE OVERLAYED EXACTLY IN STAMP'S MIDDLE BLANK SPACE ================= */
.ol-signature-area {
    position: relative;
    width: 180px;
    height: 110px; 
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
    align-items: center; 
}
/* Lower Layer: The Circular Stamp */
.ol-real-stamp {
    width: 100px;
    height: 100px;
    position: absolute;
    bottom: 8px; 
    z-index: 1;
    object-fit: contain;
}
/* Top Layer: Centered perfectly within the blank middle space of the stamp */
.ol-real-sign {
    width: 80px; 
    height: auto;
    position: absolute;
    bottom: 30px; 
    z-index: 2;
    object-fit: contain;
}
.ol-sig-line {
    border-top: 1.5px solid #222;
    font-size: 13px;
    font-weight: bold;
    padding-top: 4px;
    color: #111;
    z-index: 3;
    position: relative;
    width: 100%;
    text-align: center;
}
.ol-base-footer {
    position: absolute;
    bottom: 0; left: 0; right: 0;
    background: var(--dark-brown) !important;
    color: white !important;
    text-align: center;
    font-size: 13px;
    font-weight: bold;
    padding: 8px 0;
    letter-spacing: 0.3px;
}
"""

content = content[:css_start] + new_css + content[css_end:]

# 2. Replace HTML
# The ID card wrapper
html_start1 = content.find('<div class="id-card-wrapper" style="display:none;">')
html_end1 = content.find('<div class="offer-letter-page" style="display:none;">')

new_html1 = """<div class="id-card-wrapper" style="display:none;">
    <!-- ================= FRONT SIDE ================= -->
    <div class="id-card">
        <div class="card-header">
            <img class="logo-img" src="https://i.ibb.co/cKssRvxh/Whats-App-Image-2026-06-21-at-15-39-55.jpg" alt="Logo">
            <div class="header-title">HELPING SOCIETY MISSION &<br>VISION FOUNDATION</div>
        </div>
        <div class="sub-header-bar">
            <span>प्रत्येक सरकार द्वारा मान्यता प्राप्त</span>
            <span class="reg-badge">REG- 231407</span>
        </div>

        <div class="photo-container">
            <img id="cardPhoto" class="profile-pic" src="data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='100' height='100' viewBox='0 0 24 24'><path fill='%23ccc' d='M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5-4-8-4z'/></svg>" alt="Profile Picture">
            <img class="photo-overlay-stamp" src="https://i.ibb.co/HDdVBS1W/vikas-stamp-removebg-preview.png" alt="Stamp">
            <img class="photo-overlay-sign" src="https://i.ibb.co/Pz65fS5B/vikas-sign-removebg-preview.png" alt="Signature">
        </div>

        <h3 class="member-name" id="cardName">DEV</h3>
        <div class="member-desig" id="cardDesignation">web developer and manager</div>

        <table class="data-table">
            <tr>
                <td class="field-label">ID No.</td>
                <td class="field-sep">:</td>
                <td class="field-value" id="cardID">0001</td>
            </tr>
            <tr>
                <td class="field-label">Blood Group</td>
                <td class="field-sep">:</td>
                <td class="field-value" id="cardBloodGroup">O+</td>
            </tr>
            <tr>
                <td class="field-label">Mobile</td>
                <td class="field-sep">:</td>
                <td class="field-value" id="cardMobile">8957799335</td>
            </tr>
            <tr>
                <td class="field-label">Valid From</td>
                <td class="field-sep">:</td>
                <td class="field-value" id="cardValidFrom">02-Jul-2026</td>
            </tr>
            <tr>
                <td class="field-label">Valid To</td>
                <td class="field-sep">:</td>
                <td class="field-value" id="cardValidTo">01-Jul-2027</td>
            </tr>
        </table>

        <div class="footer-front" id="cardFooterMobile">8957799335</div>
    </div>

    <!-- ================= BACK SIDE ================= -->
    <div class="id-card">
        <div class="card-header">
            <img class="logo-img" src="https://i.ibb.co/cKssRvxh/Whats-App-Image-2026-06-21-at-15-39-55.jpg" alt="Logo">
            <div class="header-title">HELPING SOCIETY MISSION &<br>VISION FOUNDATION</div>
        </div>
        <div class="sub-header-bar">
            <span>प्रत्येक सरकार द्वारा मान्यता प्राप्त</span>
            <span class="reg-badge">REG- 231407</span>
        </div>

        <div class="qr-container">
            <img src="https://i.ibb.co/VcCRXTZm/qrcode-hsmvf-com-1.png" alt="qr-code">
        </div>

        <table class="data-table">
            <tr>
                <td class="field-label back-label">S/O</td>
                <td class="field-sep">:</td>
                <td class="field-value" id="cardFather">Gopal Narayan Srivastava</td>
            </tr>
            <tr>
                <td class="field-label back-label">DOB</td>
                <td class="field-sep">:</td>
                <td class="field-value" id="cardDOB">29-Aug-2006</td>
            </tr>
            <tr>
                <td class="field-label back-label">Address</td>
                <td class="field-sep">:</td>
                <td class="field-value" id="cardAddress" style="font-size: 12px; line-height: 1.3;">Ahiyapur Raebareli, 229001 UP</td>
            </tr>
        </table>

        <div class="divider-line"></div>

        <table class="data-table">
            <tr>
                <td class="field-label back-label" style="width:100px;">CIN</td>
                <td class="field-sep">:</td>
                <td class="field-value">U88900UP2025NPL231407</td>
            </tr>
            <tr>
                <td class="field-label back-label">NGO DARPAN</td>
                <td class="field-sep">:</td>
                <td class="field-value">UP/2025/0801291</td>
            </tr>
        </table>

        <div class="legal-notice">80G & 12 A, CSR regd.</div>

        <div class="footer-back">
            <div class="footer-back-icon">📍</div>
            <div>Address - Vijay nagar tripula,<br>Maharajganj road, Raebareli UP india 229306</div>
        </div>
    </div>
</div>
"""

content = content[:html_start1] + new_html1 + content[html_end1:]

# The offer letter page
html_start2 = content.find('<div class="offer-letter-page" style="display:none;">')
html_end2 = content.find('<div class="login-wrap" id="loginWrap">')

new_html2 = """<div class="offer-letter-page" style="display:none;">
    <div class="ol-main-header">
        <img class="ol-logo" src="https://i.ibb.co/cKssRvxh/Whats-App-Image-2026-06-21-at-15-39-55.jpg" alt="Logo">
        <div class="ol-title">HELPING SOCIETY MISSION & VISION FOUNDATION</div>
    </div>
    <div class="ol-gov-bar">
        <span>प्रदेश सरकार द्वारा मान्यता प्राप्त</span>
        <span>Reg. No. : 231407</span>
    </div>
    
    <div class="ol-meta-grid">
        <div>NGO DARPAN : UP/2025/0801291</div>
        <div class="ol-badge-title">नियुक्ति पत्र</div>
        <div>CIN NO. : U88900UP2025NPL231407</div>
    </div>

    <div class="ol-id-date-row">
        <div>ID No. - <span id="olID">0068</span></div>
        <div>Date - <span id="olDate">04-03-2026</span></div>
    </div>

    <div class="ol-body-content">
        आदरणीय श्री/श्रीमती/सुश्री <span class="highlight-red" id="olName">Prashant Tripathi</span> 
        पुत्र/पुत्री/पति <span class="highlight-red" id="olFather">Yogendra kumar Tripathi</span> आपके सामाजिक कार्यों के प्रति आपकी निष्ठा को देखते हुए अपार हर्ष के साथ सूचित किया जाता है कि 
        <span class="highlight-red">"हेल्पिंग सोसाइटी मिशन एंड विजन फाउंडेशन"</span> में आपको 
        <span class="highlight-red" id="olDesignation">मीडिया प्रभारी</span> बनाया जाता है। 
        हमें आशा ही नहीं अपितु पूर्ण विश्वास है कि आप संस्थान की नीतियों व सिद्धांतों से जन-मानस को अवगत करायेंगे/करायेंगी और संस्थान को प्रबल मजबूत बनायेंगे। संस्थापक एवं संचालक जी के नेतृत्व में घर-घर के सम्मान में, हर व्यक्ति को प्रबल, सशक्त, शिक्षित व आत्मनिर्भर बनाने के संकल्प को साकार करते हुए <span class="highlight-red">"हेल्पिंग सोसाइटी मिशन एंड विजन फाउंडेशन"</span> के विचारों को जन-जन तक पहुँचायेंगे व समाज को संगठित कर अपने राष्ट्र को शक्तिशाली बनायेंगे।
    </div>

    <!-- Footer Row Section -->
    <div class="ol-footer-row">
        <div class="ol-social-block">
            <div class="ol-qr-box" style="display: flex; align-items: center; justify-content: center; width: 60px; height: 60px;">
                <img src="https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=https://hsmvf.com" alt="Website QR Code" style="width: 100%; height: 100%; object-fit: contain;">
            </div>
            <div class="ol-mob-box">Mob. No. : <span id="olMobile">6392760740</span></div>
        </div>

        <!-- Signature block with centered layout inside the stamp's white circle space -->
        <div class="ol-signature-area">
            <img class="ol-real-stamp" src="https://i.ibb.co/HDdVBS1W/vikas-stamp-removebg-preview.png" alt="Stamp">
            <img class="ol-real-sign" src="https://i.ibb.co/Pz65fS5B/vikas-sign-removebg-preview.png" alt="Signature">
            <div class="ol-sig-line">Authorised Signature</div>
        </div>
    </div>

    <div class="ol-base-footer">
        Reg. Office - Vijay Nager Tripura, Mahrajganj Road Raebareli, Uttar Pradesh India - 229306
    </div>
</div>
"""

content = content[:html_start2] + new_html2 + content[html_end2:]

with open(r'c:\Users\DELL\Downloads\HSMV\member-login.html', 'w', encoding='utf-8') as f:
    f.write(content)
