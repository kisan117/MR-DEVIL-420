from flask import Flask, request, render_template_string
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

HTML_CODE = """
<!DOCTYPE html>
<html>
<head>
    <title>MR DEVIL MESSENGER UID FINDER</title>
</head>
<body style="text-align: center;">
    <h2>MR DEVIL MESSENGER UID FINDER</h2>
    <form method="POST">
        <textarea name="cookie" rows="6" cols="60" placeholder="Paste Facebook Cookie Here" required></textarea><br><br>
        <button type="submit">Find Messenger Group UID</button>
    </form>
    <br>
    {% if groups %}
        <h3>Messenger Groups:</h3>
        {% for group in groups %}
            <p><strong>{{ group.name }}</strong> — UID: {{ group.uid }}</p>
        {% endfor %}
    {% endif %}
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    groups = []
    if request.method == 'POST':
        cookie = request.form['cookie']
        headers = {
            'User-Agent': 'Mozilla/5.0',
            'Cookie': cookie
        }
        
        try:
            res = requests.get('https://m.facebook.com/messages', headers=headers)
            soup = BeautifulSoup(res.text, 'html.parser')
            seen = set()
            
            # Extract Group UIDs and Names from the Messenger HTML page
            for a in soup.find_all('a', href=True):
                if '/messages/read/?tid=' in a['href']:
                    name = a.text.strip()
                    uid = a['href'].split('tid=')[1]
                    if uid not in seen:
                        seen.add(uid)
                        groups.append({'name': name, 'uid': uid})
        except:
            groups = [{'name': 'Error', 'uid': 'Invalid cookie or blocked'}]
    
    return render_template_string(HTML_CODE, groups=groups)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
