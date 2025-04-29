from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

HTML_CODE = """
<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <title>MR DEVIL UID FINDER (Graph API)</title>
</head>
<body style="text-align:center; font-family:sans-serif;">
    <h2>MR DEVIL UID FINDER (Graph API)</h2>
    <form method="POST">
        <input type="text" name="token" placeholder="Page Access Token" required style="width:300px;"><br><br>
        <button type="submit">Messenger Group UID निकालो</button>
    </form>
    <br>
    {% if groups %}
        <h3>Messenger Conversations:</h3>
        {% for g in groups %}
            <p><b>UID:</b> {{ g['id'] }}</p>
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
        url = f"https://graph.facebook.com/v19.0/me/conversations?access_token={token}"
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
