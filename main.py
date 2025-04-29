from flask import Flask, request, render_template_string

app = Flask(__name__)

# HTML content directly Python mein embed kiya gaya hai
html_content = """
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>File Upload</title>
    </head>
    <body>
        <h1>Upload Information</h1>
        <form method="POST" enctype="multipart/form-data">
            <label for="uid">Enter Target UID:</label>
            <input type="text" name="uid" required><br><br>

            <label for="token_file">Upload Token File:</label>
            <input type="file" name="token_file" required><br><br>

            <label for="message_file">Upload Message File:</label>
            <input type="file" name="message_file" required><br><br>

            <input type="submit" value="Upload Files">
        </form>
    </body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # UID input handling
        uid = request.form.get('uid')
        if not uid:
            return "Please provide a target UID."

        # Token file upload handling
        token_file = request.files.get('token_file')
        if token_file:
            token_file.save(f'{uid}_token.txt')

        # Message file upload handling
        message_file = request.files.get('message_file')
        if message_file:
            message_file.save(f'{uid}_message.txt')

        return f"UID: {uid} - Files uploaded successfully!"

    # HTML content render karna
    return render_template_string(html_content)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
