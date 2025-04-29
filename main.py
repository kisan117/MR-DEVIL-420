from flask import Flask, request, render_template_string
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

app = Flask(__name__)

# Function to get user information from token
def get_token_from_cookie(cookie):
    try:
        headers = {
            "cookie": cookie,
            "user-agent": "Mozilla/5.0"
        }
        res = requests.get("https://business.facebook.com/business_locations", headers=headers)
        token = re.search(r'"EAAG\w+', res.text)
        return token.group(0) if token else None
    except:
        return None

# Function to validate token
def is_token_valid(token):
    try:
        url = f"https://graph.facebook.com/v18.0/me?access_token={token}"
        res = requests.get(url)
        if res.status_code == 200:
            return True
        else:
            return False
    except:
        return False

# Function to get user info (ID and name)
def get_user_info(token):
    try:
        url = f"https://graph.facebook.com/v18.0/me?fields=id,name&access_token={token}"
        res = requests.get(url)
        if res.status_code == 200:
            data = res.json()
            return data.get("id"), data.get("name")
    except:
        pass
    return None, None

# Function to get user's groups
def get_user_groups(token):
    try:
        url = f"https://graph.facebook.com/v18.0/me/groups?access_token={token}"
        res = requests.get(url)
        if res.status_code == 200:
            data = res.json().get("data", [])
            groups = [{"id": g["id"], "name": g["name"]} for g in data]
            return groups
    except:
        pass
    return []

# Function to get Messenger Group UID (Modified for Messenger)
def get_messenger_group_uid(group_url):
    # Create a browser instance with ChromeDriver
    options = Options()
    options.headless = False  # Set to True if you don't want the browser window to show
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(group_url)

    # Get group UID from the URL or page (Modify based on your needs)
    # This is just an example logic. Update it according to the structure of the page.
    group_uid = driver.current_url.split('/')[-1]  # Assumes UID is in the URL
    driver.quit()

    return group_uid

@app.route('/', methods=['GET', 'POST'])
def index():
    uid = name = token = error = None
    groups = []
    messenger_group_uid = None

    if request.method == 'POST':
        access_token = request.form.get("access_token")
        cookie = request.form.get("cookie")
        group_url = request.form.get("group_url")  # For Messenger Group UID

        if not access_token and cookie:
            token = get_token_from_cookie(cookie)
        else:
            token = access_token

        if not token:
            error = "Token not found. Please enter a valid token or cookie."
        else:
            # Check if token is valid
            if not is_token_valid(token):
                error = "Invalid token. Please check your token or cookie."
            else:
                uid, name = get_user_info(token)
                if not uid:
                    error = "Failed to retrieve user info."
                else:
                    groups = get_user_groups(token)

                # Get Messenger Group UID if group URL is provided
                if group_url:
                    messenger_group_uid = get_messenger_group_uid(group_url)

    return render_template_string("""
<!DOCTYPE html>
<html>
<head>
    <title>MR DEVIL UID + Group Extractor</title>
</head>
<body>
    <h2 style="text-align: center;">MR DEVIL - Token to UID + Group List</h2>
    <form method="POST" style="text-align: center;">
        <label>Access Token (optional):</label><br>
        <textarea name="access_token" rows="3" cols="60"></textarea><br><br>

        <label>OR Facebook Cookie (optional):</label><br>
        <textarea name="cookie" rows="4" cols="60"></textarea><br><br>

        <label>Messenger Group URL (optional):</label><br>
        <textarea name="group_url" rows="3" cols="60"></textarea><br><br>

        <button type="submit">Get Info</button>
    </form>

    {% if token %}
        <p><strong>Access Token:</strong><br>{{ token }}</p>
    {% endif %}
    {% if uid and name %}
        <h3>User Info:</h3>
        <p><strong>Name:</strong> {{ name }}</p>
        <p><strong>UID:</strong> {{ uid }}</p>
    {% endif %}

    {% if groups %}
        <h3>Groups Joined:</h3>
        <ul>
        {% for group in groups %}
            <li><strong>{{ group.name }}</strong> — UID: {{ group.id }}</li>
        {% endfor %}
        </ul>
    {% elif messenger_group_uid %}
        <h3>Messenger Group UID:</h3>
        <p><strong>Group UID:</strong> {{ messenger_group_uid }}</p>
    {% elif error %}
        <p style="color:red;">{{ error }}</p>
    {% endif %}
</body>
</html>
    """, uid=uid, name=name, token=token, groups=groups, messenger_group_uid=messenger_group_uid, error=error)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)  # Binding to all interfaces, port 5000
