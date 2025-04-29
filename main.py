from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_all_group_uids', methods=['POST'])
def get_all_group_uids():
    access_token = request.form['access_token']
    url = f'https://graph.facebook.com/me/groups?access_token={access_token}'
    response = requests.get(url)

    if response.status_code == 200:
        groups = response.json().get('data', [])
        group_details = [{'name': g.get('name'), 'uid': g.get('id')} for g in groups]
        return render_template('result.html', group_details=group_details)
    else:
        return f"Error: {response.status_code} - {response.text}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
