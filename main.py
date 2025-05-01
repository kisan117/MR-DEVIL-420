from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

HTML_CODE = """
<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <title>MR DEVIL UID FINDER (Graph API)</title>
    <style>
        body {
            text-align: center;
            font-family: sans-serif;
            background-image: url('https://iili.io/3hK9Vqv.md.jpg');
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
            color: white;
        }
        input, button {
            padding: 10px;
            border: none;
            border-radius: 5px;
            font-size: 16px;
        }
        button {
            background-color: #ff4444;
            color: white;
            cursor: pointer;
        }
        h2, h3 {
            background-color: rgba(0, 0, 0, 0.5);
            display: inline-block;
            padding: 10px 20px;
            border-radius: 10px;
        }
        form {
            background-color: rgba(0, 0, 0, 0.4);
            display: inline-block;
            padding: 20px;
            border-radius: 10px;
        }
        .group-box {
            background-color: rgba(0, 0, 0, 0.4);
            padding: 10px;
            margin: 10px auto;
            width: 80%;
            border-radius: 10px;
        }
    </style>
</head>
<body>
    <h2>MR DEVIL UID FINDER (Graph API)</h2><br><br>
    <form method="POST">
        <input type="text" name="token" placeholder="Page Access Token" required style="width:300px;"><br><br>
        <button type="submit">Messenger Group UID निकालो</button>
    </form>
    <br><br>
    {% if groups %}
        <h3>Messenger Conversations:</h3>
        {% for g in groups %}
            <div class="group-box">
                <p><b>नाम:</b> {{ g.get('name', 'नाम नहीं मिला') }}</p>
                <p><b>UID:</b> {{ g['id'] }}</p>
            </div>
        {% endfor %}
    {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    groups = []
    if request.method == "POST":
        token = request.form.get("token")
        url = f"https://graph.facebook.com/v19.0/me/conversations?fields=name,id&access_token={token}"
        try:
            res = requests.get(url)
            if res.status_code == 200:
                data = res.json()
                groups = data.get("data", [])
            else:
                groups = [{"id": f"Error: {res.status_code} - {res.text}"}]
        except Exception as e:
            groups = [{"id": f"Exception: {str(e)}"}]
    return render_template_string(HTML_CODE, groups=groups)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
