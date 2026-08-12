import re

with open('student-membership.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add Google Fonts
if 'fonts.googleapis.com' not in content:
    content = content.replace('<head>', '<head>\n<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">\n')

# 2. Replace CSS
new_css = '''
*{margin:0;padding:0;box-sizing:border-box;}
body{font-family:"Inter",sans-serif;background:linear-gradient(135deg,#0f172a,#1e293b,#334155);background-size:200% 200%;animation:gradientBG 10s ease infinite;color:#f8fafc;min-height:100vh;}
@keyframes gradientBG{0%{background-position:0% 50%;}50%{background-position:100% 50%;}100%{background-position:0% 50%;}}
@keyframes fadeInUp{from{opacity:0;transform:translateY(20px);}to{opacity:1;transform:translateY(0);}}
.topbar{background:rgba(15,23,42,0.7);backdrop-filter:blur(10px);padding:12px 5%;display:flex;align-items:center;gap:15px;border-bottom:1px solid rgba(255,255,255,0.1);position:sticky;top:0;z-index:100;box-shadow:0 4px 30px rgba(0,0,0,0.1);}
.topbar img{width:45px;height:45px;border-radius:50%;border:2px solid #3b82f6;box-shadow:0 0 10px rgba(59,130,246,0.5);}
.topbar-title{color:#fff;font-size:0.95rem;font-weight:700;line-height:1.2;}
.topbar-title span{display:block;font-size:0.65rem;color:#60a5fa;letter-spacing:2px;text-transform:uppercase;}
.topbar a{margin-left:auto;color:#fff;text-decoration:none;font-size:0.8rem;background:rgba(255,255,255,0.1);border:1px solid rgba(255,255,255,0.2);padding:6px 14px;border-radius:6px;transition:0.3s;}
.topbar a:hover{background:#3b82f6;border-color:#3b82f6;}
.hero{text-align:center;padding:40px 5% 30px;animation:fadeInUp 0.8s ease-out;}
.hero h1{font-size:1.8rem;font-weight:800;margin-bottom:8px;letter-spacing:-0.5px;}
.hero h1 span{color:#3b82f6;text-shadow:0 0 20px rgba(59,130,246,0.5);}
.hero p{color:#94a3b8;font-size:0.9rem;}
.container{max-width:650px;margin:0 auto;padding:0 15px 60px;}
.progress-bar{height:6px;background:rgba(255,255,255,0.05);border-radius:3px;margin-bottom:25px;overflow:hidden;border:1px solid rgba(255,255,255,0.1);}
.progress-fill{height:100%;background:linear-gradient(90deg,#3b82f6,#8b5cf6);border-radius:3px;transition:width 0.5s cubic-bezier(0.4,0,0.2,1);width:33%;box-shadow:0 0 10px rgba(59,130,246,0.6);}
.step-bar{display:flex;align-items:center;margin-bottom:30px;animation:fadeInUp 0.9s ease-out;}
.step{display:flex;flex-direction:column;align-items:center;gap:5px;flex:1;}
.sc{width:34px;height:34px;border-radius:50%;background:rgba(255,255,255,0.05);color:#64748b;font-size:0.85rem;font-weight:700;display:flex;align-items:center;justify-content:center;border:1px solid rgba(255,255,255,0.1);transition:0.4s;}
.sc.active{background:#3b82f6;color:#fff;border-color:#3b82f6;box-shadow:0 0 15px rgba(59,130,246,0.4);transform:scale(1.1);}
.sc.done{background:#10b981;color:#fff;border-color:#10b981;}
.sl{font-size:0.65rem;color:#64748b;text-transform:uppercase;letter-spacing:1px;font-weight:600;transition:0.4s;}
.sl.active{color:#3b82f6;}
.sline{flex:1;height:2px;background:rgba(255,255,255,0.1);margin-top:-15px;transition:0.4s;}
.sline.done{background:#10b981;}
.card{background:rgba(255,255,255,0.03);backdrop-filter:blur(16px);-webkit-backdrop-filter:blur(16px);border:1px solid rgba(255,255,255,0.08);border-radius:16px;padding:25px 20px;box-shadow:0 10px 30px rgba(0,0,0,0.2);margin-bottom:20px;animation:fadeInUp 1s ease-out;animation-fill-mode:both;}
.card h2{font-size:1.1rem;color:#fff;margin-bottom:20px;display:flex;align-items:center;gap:8px;border-bottom:1px solid rgba(255,255,255,0.05);padding-bottom:12px;}
.frow{display:grid;grid-template-columns:1fr 1fr;gap:15px;}
.fg{margin-bottom:15px;}
.fg label{display:block;font-size:0.75rem;font-weight:600;letter-spacing:0.5px;color:#cbd5e1;margin-bottom:6px;}
.fg label .req{color:#ef4444;}
.fg label .opt{color:#64748b;font-weight:400;text-transform:none;font-size:0.7rem;}
.fg input,.fg select,.fg textarea{width:100%;padding:12px 14px;border:1px solid rgba(255,255,255,0.1);border-radius:8px;font-family:inherit;font-size:0.9rem;color:#fff;background:rgba(0,0,0,0.2);outline:none;transition:all 0.3s cubic-bezier(0.4,0,0.2,1);}
.fg input:focus,.fg textarea:focus{border-color:#3b82f6;background:rgba(0,0,0,0.3);box-shadow:0 0 0 3px rgba(59,130,246,0.2);transform:translateY(-1px);}
.fg input::placeholder{color:#64748b;}
.fg textarea{resize:vertical;min-height:80px;}
.err{color:#ef4444;font-size:0.75rem;margin-top:5px;display:none;animation:fadeInUp 0.2s;}
.fe input,.fe textarea{border-color:#ef4444!important;background:rgba(239,68,68,0.05)!important;}
.upload-box{border:2px dashed rgba(255,255,255,0.2);border-radius:12px;padding:25px 15px;text-align:center;cursor:pointer;transition:0.3s;background:rgba(0,0,0,0.1);}
.upload-box:hover{border-color:#3b82f6;background:rgba(59,130,246,0.05);transform:translateY(-2px);}
.upload-box .ico{font-size:1.8rem;margin-bottom:8px;opacity:0.8;}
.upload-box p{font-size:0.85rem;color:#cbd5e1;margin-bottom:5px;}
.upload-box .fn{font-size:0.75rem;color:#10b981;font-weight:600;}
.qr-card{background:linear-gradient(135deg,rgba(59,130,246,0.1),rgba(139,92,246,0.1));backdrop-filter:blur(10px);border:1px solid rgba(59,130,246,0.2);border-radius:16px;padding:30px 20px;color:#fff;text-align:center;margin-bottom:20px;animation:fadeInUp 1.2s ease-out;animation-fill-mode:both;}
.qr-card h2{font-size:1.2rem;margin-bottom:8px;font-weight:700;}
.qr-card p{font-size:0.85rem;color:#94a3b8;margin-bottom:20px;}
.amt{background:rgba(59,130,246,0.2);border:1px solid rgba(59,130,246,0.4);border-radius:8px;display:inline-block;padding:10px 25px;font-size:1.5rem;font-weight:800;color:#fff;margin-bottom:25px;letter-spacing:1px;box-shadow:0 4px 15px rgba(59,130,246,0.3);}
.qr-card img{width:100%;max-width:260px;height:auto;border-radius:12px;box-shadow:0 8px 25px rgba(0,0,0,0.4);margin:0 auto 15px;display:block;border:3px solid rgba(255,255,255,0.1);transition:transform 0.3s;}
.qr-card img:hover{transform:scale(1.03);}
.upiid{font-size:0.8rem;color:#cbd5e1;font-weight:500;letter-spacing:0.5px;}
.btn-main{width:100%;padding:15px;background:linear-gradient(135deg,#3b82f6,#2563eb);color:#fff;border:none;border-radius:10px;font-size:1rem;font-weight:700;cursor:pointer;transition:all 0.3s;font-family:inherit;box-shadow:0 4px 15px rgba(59,130,246,0.4);text-transform:uppercase;letter-spacing:1px;}
.btn-main:hover{transform:translateY(-2px);box-shadow:0 8px 25px rgba(59,130,246,0.5);background:linear-gradient(135deg,#4f46e5,#3b82f6);}
.btn-main:disabled{background:rgba(255,255,255,0.1);color:#64748b;cursor:not-allowed;box-shadow:none;transform:none;}
@media(max-width:520px){.frow{grid-template-columns:1fr;gap:0;}}
'''

content = re.sub(r'<style>.*?</style>', '<style>\n' + new_css + '\n</style>', content, flags=re.DOTALL)

# 3. Update the QR code image src to qr.jpg
content = re.sub(r'<img src="https://api\.qrserver\.com[^"]+" alt="UCO Bank UPI QR"/>', '<img src="qr.jpg" alt="UCO Bank UPI QR"/>', content)
content = content.replace('<img src="icon.jpg" alt="UCO Bank UPI QR"/>', '<img src="qr.jpg" alt="UCO Bank UPI QR"/>')

with open('student-membership.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Redesign applied successfully!")
