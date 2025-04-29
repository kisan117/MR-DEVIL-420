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

    try:
        data = response.json()
        if 'data' in data and data['data']:
            groups = data['data']
            group_details = [{'name': g.get('name'), 'uid': g.get('id')} for g in groups]
            return render_template('result.html', group_details=group_details)
        else:
            return render_template('result.html', group_details=[], message="No groups found or token has limited access.")
    except Exception as e:
        return f"Error occurred: {str(e)}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
