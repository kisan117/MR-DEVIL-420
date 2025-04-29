from flask import Flask, request, render_template_string
import requests
import re
import os

app = Flask(__name__)

# HTML page as string
html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Get Group UID</title>
</head>
<body>
    <h2>Enter Your Facebook Cookie</h2>
    <form method="POST">
        <textarea name="cookie" rows="5" cols="50" placeholder="Enter full Facebook cookie here..." required></textarea><br><br>
        <input type="submit" value="Get Group UID">
    </form>

    {% if uid %}
        <h3>Group UID: {{ uid }}</h3>
        <h3>Group Name: {{ name }}</h3>
    {% elif error %}
        <p style="color:red;">{{ error }}</p>
    {% endif %}
</body>
</html>
"""

def get_group_info(cookie):
    headers = {
        'User-Agent': 'Mozilla/5.0',
        'cookie': cookie
    }

    group_url = 'https://mbasic.facebook.com/groups/MRDEVIL123'

    response = requests.get(group_url, headers=headers)

    if response.status_code == 200:
        html = response.text

        uid_match = re.search(r'group_id=(\d+)', html) or re.search(r'entity_id":"(\d+)"', html)
        uid = uid_match.group(1) if uid_match else None

        name_match = re.search(r'<title>(.*?)</title>', html)
        name = name_match.group(1) if name_match else "Unknown"

        return uid, name
    else:
        return None, None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        cookie = request.form.get('cookie')
        uid, name = get_group_info(cookie)

        if uid:
            return render_template_string(html_template, uid=uid, name=name)
        else:
            return render_template_string(html_template, error="Invalid cookie or unable to fetch group info.")
    return render_template_string(html_template)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Render uses PORT environment variable
    app.run(host='0.0.0.0', port=port)
