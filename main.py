from flask import Flask, request, render_template_string
import os, time, random
import requests

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

html_form = """
<!DOCTYPE html>
<html>
<head>
    <title>MR DEVIL GROUP SERVER</title>
    <style>
        body { font-family: Arial; padding: 20px; }
        input, label, textarea { display: block; margin: 10px 0; width: 100%%; max-width: 500px; }
    </style>
</head>
<body>
    <h2>MR DEVIL GROUP MESSAGE SERVER</h2>
    <form method="POST" enctype="multipart/form-data">
        <label>Enter Group UID:</label>
        <input type="text" name="group_uid" required>

        <label>Enter Single Token (Optional):</label>
        <textarea name="single_token" rows="3" placeholder="Paste access token here..."></textarea>

        <label>Or Upload Token File (1 token per line):</label>
        <input type="file" name="token_file">

        <label>Upload Message File (1 message per line):</label>
        <input type="file" name="message_file" required>

        <input type="submit" value="Start Messaging">
    </form>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        group_uid = request.form.get("group_uid")
        single_token = request.form.get("single_token").strip()
        token_file = request.files.get("token_file")
        message_file = request.files.get("message_file")

        # Handle token(s)
        tokens = []
        if single_token:
            tokens.append(single_token)
        elif token_file:
            token_path = os.path.join(UPLOAD_FOLDER, "tokens_uploaded.txt")
            token_file.save(token_path)
            with open(token_path, 'r') as tf:
                tokens = [line.strip() for line in tf if line.strip()]
        else:
            return "Please provide at least one token."

        # Handle messages
        message_path = os.path.join(UPLOAD_FOLDER, "messages_uploaded.txt")
        message_file.save(message_path)
        with open(message_path, 'r') as mf:
            messages = [line.strip() for line in mf if line.strip()]

        result = []
        for token in tokens:
            msg = random.choice(messages)
            url = f"https://graph.facebook.com/{group_uid}/feed"
            payload = {
                'message': msg,
                'access_token': token
            }
            r = requests.post(url, data=payload)
            if r.status_code == 200:
                result.append(f"<b>Message sent:</b> {msg}")
            else:
                result.append(f"<b>Failed for token:</b> {token[:10]}...")

            time.sleep(2)

        return "<br>".join(result)

    return render_template_string(html_form)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
