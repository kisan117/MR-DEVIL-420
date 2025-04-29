from flask import Flask, request, render_template_string
import requests

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
            <button type="submit" class="btn-submit">Get Group UID</button>
        </form>
        {% if uid %}
        <h3>Group UID: {{ uid }}</h3>
        <h3>Group Name: {{ group_name }}</h3>
        {% elif error %}
        <h3 style="color:red;">Error: {{ error }}</h3>
        {% endif %}
    </div>

    <footer>
        <p style="color: #FF5733;">Post Loader Tool</p>
        <p>AFFAN OFFICAL</p>
    </footer>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def get_group_uid():
    if request.method == 'POST':
        token = request.form['token']
        url = f'https://graph.facebook.com/v15.0/me/groups?access_token={token}'

        response = requests.get(url)
        data = response.json()

        if 'data' in data and data['data']:
            group = data['data'][0]  # Get the first group from the list
            group_name = group.get('name')
            group_uid = group.get('id')
            return render_template_string(html_template, uid=group_uid, group_name=group_name)

        else:
            error_message = "No groups found or invalid token."
            return render_template_string(html_template, error=error_message)

    return render_template_string(html_template)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
