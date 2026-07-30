import base64
import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

match = re.search(r'data:image/jpeg;base64,([^"]+)', content)
if match:
    img_data = base64.b64decode(match.group(1))
    with open('icon.jpg', 'wb') as f:
        f.write(img_data)
    print("Icon extracted successfully.")
else:
    print("No icon found.")
