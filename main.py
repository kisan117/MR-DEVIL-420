from flask import Flask, request, render_template_string
import requests
import re
import os

app = Flask(__name__)

# HTML code
html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Group UID Finder</title>
</head>
<body>
    <h2>Enter Your Facebook Cookie</h2>
    <form method="POST">
        <textarea name="cookie" rows="5" cols="60" placeholder="Paste full Facebook cookie here..." required></textarea><br><br>
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
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10)',
        'Cookie': cookie
    }

    # Replace with a working group URL (make sure it’s public or you're a member)
    group_url = 'https://mbasic.facebook.com/groups/yourgroupid_or_slug'

    try:
        res = requests.get(group_url, headers=headers)
        if "Log in" in res.text or "login" in res.url:
            return None, None  # Facebook redirected to login

        # Try multiple UID patterns
        uid = None
        for pattern in [r'group_id=(\d+)', r'entity_id":"(\d+)"', r'"group_id":"(\d+)"']:
            match = re.search(pattern, res.text)
            if match:
                uid = match.group(1)
                break

        name_match = re.search(r'<title>(.*?)</title>', res.text)
        name = name_match.group(1).replace(" | Facebook", "") if name_match else "Unknown"

        return uid, name
    except Exception as e:
        return None, None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        cookie = request.form.get('cookie')
        uid, name = get_group_info(cookie)
        if uid:
            return render_template_string(html_template, uid=uid, name=name)
        else:
            return render_template_string(html_template, error="Invalid cookie or cannot access group.")
    return render_template_string(html_template)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
