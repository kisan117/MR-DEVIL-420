from flask import Flask, request, render_template_string
import requests
import re
import os

app = Flask(__name__)

# HTML template
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Group UID Finder</title>
    <style>
        body {
            background-image: url('https://i.ibb.co/19kSMz4/In-Shot-20241121-173358587.jpg');
            background-size: cover;
            background-repeat: no-repeat;
            color: white;
            font-family: Arial, sans-serif;
            display: flex;
            flex-direction: column;
            min-height: 100vh;
        }
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 20px;
            background: rgba(0, 0, 0, 0.7);
        }
        .header h1 {
            margin: 0;
            font-size: 24px;
        }
        .container {
            background-color: rgba(0, 0, 0, 0.7);
            padding: 20px;
            border-radius: 10px;
            max-width: 600px;
            margin: 40px auto;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }
        .form-control {
            width: 100%;
            padding: 10px;
            margin-bottom: 10px;
            border-radius: 5px;
            border: none;
        }
        .btn-submit {
            background-color: #4CAF50;
            color: white;
            padding: 10px 20px;
            border: none;
            cursor: pointer;
            border-radius: 5px;
            width: 100%;
        }
        footer {
            text-align: center;
            padding: 20px;
            background-color: rgba(0, 0, 0, 0.7);
            margin-top: auto;
        }
        footer p {
            margin: 5px 0;
        }
    </style>
</head>
<body>
    <header class="header">
        <h1 style="color: red;">  HIPHOP AFFAN ENSIDE</h1>
        <h1 style="color: blue;">AFFAN MARK )</h1>
    </header>

    <div class="container">
        <form action="/" method="post">
            <div class="mb-3">
                <label for="token">Enter Facebook Token:</label>
                <input type="text" class="form-control" id="token" name="token" required>
            </div>
            <div class="mb-3">
                <label for="groupUrl">Enter Group URL:</label>
                <input type="text" class="form-control" id="groupUrl" name="groupUrl" required>
            </div>
            <button type="submit" class="btn-submit">Get Group UID</button>
        </form>
    </div>

    <footer>
        <p style="color: #FF5733;">Group UID Finder</p>
        <p>Powered by MR DEVIL</p>
    </footer>
</body>
</html>
"""

def get_group_info(token, group_url):
    headers = {
        'Authorization': f'Bearer {token}'
    }
    
    try:
        response = requests.get(group_url, headers=headers)
        
        if response.status_code == 200:
            html = response.text
            
            # Extract Group UID from the page
            uid_match = re.search(r'group_id=(\d+)', html)
            group_name_match = re.search(r'<title>(.*?)</title>', html)
            
            uid = uid_match.group(1) if uid_match else "Not Found"
            group_name = group_name_match.group(1).replace(" | Facebook", "") if group_name_match else "Unknown"
            
            return uid, group_name
        else:
            return None, "Failed to retrieve the group. Please check the token and URL."
    except Exception as e:
        return None, str(e)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        token = request.form.get('token')
        group_url = request.form.get('groupUrl')

        uid, group_name = get_group_info(token, group_url)

        if uid:
            return render_template_string(html_template, uid=uid, group_name=group_name)
        else:
            return render_template_string(html_template, error=group_name)

    return render_template_string(html_template)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
