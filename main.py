from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

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

def get_user_groups(token):
    try:
        # Fetch Messenger groups along with other groups
        url = f"https://graph.facebook.com/v18.0/me/groups?access_token={token}"
        res = requests.get(url)
        if res.status_code == 200:
            data = res.json().get("data", [])
            groups = [{"id": group["id"], "name": group["name"]} for group in data if "id" in group and "name" in group]
            return groups
    except:
        pass
    return []

@app.route('/', methods=['GET', 'POST'])
def index():
    groups = []
    error = None
    if request.method == 'POST':
        access_token = request.form.get("access_token")

        if not access_token:
            error = "Token not found. Please enter a valid token."
        else:
            # Check if token is valid
            if not is_token_valid(access_token):
                error = "Invalid token. Please check your token."
            else:
                # Fetch groups based on valid token
                groups = get_user_groups(access_token)

    return render_template_string("""
<!DOCTYPE html>
<html>
<head>
    <title>MR DEVIL UID + Group Extractor</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            background-color: #f4f4f4;
        }
        .container {
            text-align: center;
            background-color: #fff;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            width: 400px;
        }
        textarea {
            width: 100%;
            padding: 10px;
            margin-top: 10px;
            margin-bottom: 20px;
            border-radius: 4px;
            border: 1px solid #ddd;
        }
        button {
            padding: 10px 20px;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
        button:hover {
            background-color: #45a049;
        }
        h2 {
            color: #333;
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>MR DEVIL - Token to Group List</h2>
        <form method="POST">
            <label>Enter Access Token:</label><br>
            <textarea name="access_token" rows="3" cols="60"></textarea><br><br>

            <button type="submit">Get Groups</button>
        </form>

        {% if error %}
            <p style="color:red;">{{ error }}</p>
        {% endif %}

        {% if groups %}
            <h3>Groups Joined:</h3>
            <ul>
            {% for group in groups %}
                <li><strong>{{ group.name }}</strong> — Group UID: {{ group.id }}</li>
            {% endfor %}
            </ul>
        {% endif %}
    </div>
</body>
</html>
    """, groups=groups, error=error)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
