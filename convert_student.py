import re

with open('membership.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace "Membership Registration" with "Student Membership Registration"
content = content.replace("<title>Membership Registration | HSMV Foundation</title>", "<title>Student Membership Registration | HSMV Foundation</title>")

# Strip base64 image to make it readable and editable, replacing with icon.jpg
new_content = re.sub(r'data:image/[^;]+;base64,[^"]+', 'icon.jpg', content)

with open('student-membership.html', 'w', encoding='utf-8') as f:
    f.write(new_content)
