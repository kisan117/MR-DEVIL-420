from flask import Flask, request, render_template_string
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

html_form = """
<!DOCTYPE html>
<html>
<head>
    <title>MR DEVIL FORM SERVER</title>
    <style>
        body { font-family: Arial; padding: 20px; }
        input, label { display: block; margin: 10px 0; }
    </style>
</head>
<body>
    <h2>MR DEVIL POST SERVER</h2>
    <form method="POST" enctype="multipart/form-data">
        <label>Target UID:</label>
        <input type="text" name="uid" required>

        <label>Upload Token File:</label>
        <input type="file" name="token_file" required>

        <label>Upload Message File (np.txt):</label>
        <input type="file" name="message_file" required>

        <input type="submit" value="Submit">
    </form>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        uid = request.form.get("uid")
        token_file = request.files["token_file"]
        message_file = request.files["message_file"]

        # Save files with UID-specific names
        token_path = os.path.join(UPLOAD_FOLDER, f"{uid}_token.txt")
        msg_path = os.path.join(UPLOAD_FOLDER, f"{uid}_message.txt")

        token_file.save(token_path)
        message_file.save(msg_path)

        return f"Success! UID: {uid} files uploaded."

    return render_template_string(html_form)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
