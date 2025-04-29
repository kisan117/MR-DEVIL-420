import os
import requests

# Facebook Access Token ko environment variable se fetch karein
access_token = os.getenv('ACCESS_TOKEN')

# Group ID (Example: '1234567890')
group_id = 'your_group_id'

# Graph API request
url = f'https://graph.facebook.com/{group_id}?access_token={access_token}'
response = requests.get(url)

# Handle the response
if response.status_code == 200:
    group_info = response.json()
    print(group_info)
else:
    print(f"Error: {response.status_code}")
