from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_all_group_uids', methods=['POST'])
def get_all_group_uids():
    access_token = request.form['access_token']
    # Facebook Graph API URL with version
    url = f'https://graph.facebook.com/v12.0/me/groups?access_token={access_token}'
    
    response = requests.get(url)
    data = response.json()

    # Check if the API responded with group data
    if response.status_code == 200 and 'data' in data:
        if data['data']:
            group_details = [{'name': g['name'], 'uid': g['id']} for g in data['data']]
            return render_template('result.html', group_details=group_details)
        else:
            return render_template('result.html', group_details=[], message="No groups found. Please check your token's permissions.")
    else:
        error_message = data.get('error', {}).get('message', 'Unknown error occurred.')
        return render_template('result.html', group_details=[], message=f"Error: {error_message}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
