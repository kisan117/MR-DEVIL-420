from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Home page route jahan user apna Access Token daalega
@app.route('/')
def home():
    return render_template('index.html')

# Access Token se sabhi group UID aur names nikaalne ke liye route
@app.route('/get_all_group_uids', methods=['POST'])
def get_all_group_uids():
    access_token = request.form['access_token']  # User ke daale hua Access Token

    # Facebook Graph API ka URL jahan se user ke sabhi groups ka data fetch karna hai
    url = f'https://graph.facebook.com/me/groups?access_token={access_token}'
    
    # Facebook API request bhejna
    response = requests.get(url)

    if response.status_code == 200:
        group_info = response.json()
        groups = group_info.get('data', [])
        if groups:
            group_details = []
            for group in groups:
                group_name = group.get('name', 'No name available')
                group_uid = group.get('id', 'No UID found')
                group_details.append({'name': group_name, 'uid': group_uid})
            
            return render_template('result.html', group_details=group_details)
        else:
            return f"Error: No groups found for this access token."
    else:
        # Agar error ho, toh user ko batana
        return f"Error: Unable to fetch group details. Status Code: {response.status_code}"

# Flask app ko run karte waqt port ka use render ke environment ke hisaab se hota hai
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
