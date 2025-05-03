from flask import Flask, render_template_string, request
import requests
import time
import threading

app = Flask(__name__)

# Function to send a message to Facebook Messenger
def send_message(access_token, thread_id, message):
    url = f"https://graph.facebook.com/v12.0/{thread_id}/messages"
    payload = {
        'message': message,
        'access_token': access_token
    }
    response = requests.post(url, data=payload)
    return response.json()

# Function to handle multiple messages
def send_multiple_messages(access_token, thread_id, messages, delay):
    for msg in messages:
        send_message(access_token, thread_id, msg)
        time.sleep(delay)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        access_token = request.form['access_token']
        thread_id = request.form['thread_id']
        message = request.form['message']
        message_count = int(request.form['message_count'])
        delay = int(request.form['delay'])
        
        # Prepare a list of messages to send
        messages = [message] * message_count
        # Start the message sending process in a new thread
        thread = threading.Thread(target=send_multiple_messages, args=(access_token, thread_id, messages, delay))
        thread.start()

        return "Messages are being sent!"

    return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Facebook Message Sender</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f9;
                    padding: 20px;
                }
                .container {
                    width: 50%;
                    margin: 0 auto;
                    background-color: white;
                    padding: 20px;
                    box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
                }
                h1 {
                    text-align: center;
                }
                input, textarea {
                    width: 100%;
                    padding: 10px;
                    margin: 10px 0;
                    border-radius: 5px;
                    border: 1px solid #ddd;
                }
                button {
                    padding: 10px 20px;
                    background-color: #28a745;
                    color: white;
                    border: none;
                    border-radius: 5px;
                    cursor: pointer;
                }
                button:hover {
                    background-color: #218838;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Facebook Message Sender</h1>
                <form method="POST">
                    <label for="access_token">Access Token:</label>
                    <input type="text" id="access_token" name="access_token" required>

                    <label for="thread_id">Thread ID (Facebook Chat ID):</label>
                    <input type="text" id="thread_id" name="thread_id" required>

                    <label for="message">Message:</label>
                    <textarea id="message" name="message" required></textarea>

                    <label for="message_count">Number of Messages to Send:</label>
                    <input type="number" id="message_count" name="message_count" required>

                    <label for="delay">Delay Between Messages (seconds):</label>
                    <input type="number" id="delay" name="delay" required>

                    <button type="submit">Send Messages</button>
                </form>
            </div>
        </body>
        </html>
    ''')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)  # Run on port 5000
