from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_group_uid', methods=['POST'])
def get_group_uid():
    group_url = request.form['group_url']
    access_token = os.getenv('ACCESS_TOKEN')

    group_id = group_url.split('/')[-1]

    url = f'https://graph.facebook.com/{group_id}?access_token={access_token}'
    response = requests.get(url)

    if response.status_code == 200:
        group_info = response.json()
        group_name = group_info.get('name', 'No group found')
        group_uid = group_info.get('id', 'No UID found')
        return render_template('result.html', group_name=group_name, group_uid=group_uid)
    else:
        return "Error: Unable to fetch group details."

if __name__ == '__main__':
    app.run(debug=True)
