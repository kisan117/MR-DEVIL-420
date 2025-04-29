from flask import Flask, request, render_template_string
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# HTML template for the form
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

# Function to extract Messenger Group UID using the cookie
def get_messenger_group_uid(cookie):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Cookie': cookie,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'TE': 'Trailers',
        'Host': 'm.facebook.com'
    }

    url = "https://m.facebook.com/messages"
    
    # Send request to Facebook Messenger
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"Error: Received status code {response.status_code}")
        return []

    # Parse HTML response
    soup = BeautifulSoup(response.text, 'html.parser')
    
    groups = []
    
    # Find all links that lead to message threads
    for a in soup.find_all('a', href=True):
        if '/messages/read/?tid=' in a['href']:
            name = a.text.strip()
            uid = a['href'].split('tid=')[1]
            groups.append({'name': name, 'uid': uid})
    
    return groups

# Home route to display the form and process the input
@app.route('/', methods=['GET', 'POST'])
def index():
    groups = []
    if request.method == 'POST':
        cookie = request.form['cookie']
        groups = get_messenger_group_uid(cookie)
    
    return render_template_string(HTML_CODE, groups=groups)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
