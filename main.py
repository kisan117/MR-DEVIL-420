from flask import Flask, request, render_template_string
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import re

app = Flask(__name__)

def extract_uid_from_messenger(cookie):
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        driver = webdriver.Chrome(options=chrome_options)
        driver.get("https://www.messenger.com")

        driver.delete_all_cookies()
        for part in cookie.split(";"):
            name, value = part.strip().split("=", 1)
            driver.add_cookie({"name": name, "value": value, "domain": ".messenger.com"})

        driver.get("https://www.messenger.com")
        time.sleep(5)

        # Get current URL (after opening a group)
        current_url = driver.current_url
        match = re.search(r"/t/(\d+)", current_url)
        uid = match.group(1) if match else None

        driver.quit()
        return uid
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/', methods=['GET', 'POST'])
def index():
    uid = error = None
    if request.method == 'POST':
        cookie = request.form.get('cookie')
        if cookie:
            uid = extract_uid_from_messenger(cookie)
            if "Error" in str(uid):
                error = uid
                uid = None
    return render_template_string("""
        <h2 style="text-align:center;">MR DEVIL - Messenger UID Extractor</h2>
        <form method="POST" style="text-align:center;">
            <label>Facebook Cookie:</label><br>
            <textarea name="cookie" rows="4" cols="60" required></textarea><br><br>
            <button type="submit">Extract UID</button>
        </form>
        {% if uid %}
            <h3 style="text-align:center;">Messenger Group UID: <span style="color:green;">{{ uid }}</span></h3>
        {% elif error %}
            <p style="color:red; text-align:center;">{{ error }}</p>
        {% endif %}
    """, uid=uid, error=error)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)  # Binding to all interfaces, port 8000
