import requests
from bs4 import BeautifulSoup

def get_messenger_group_uid(cookie):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Cookie': cookie,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'TE': 'Trailers',
        'Host': 'm.facebook.com'
    }

    url = "https://m.facebook.com/messages"
    
    # Send request to Facebook Messenger
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"Error: Received status code {response.status_code}")
        return []

    # Parse HTML response
    soup = BeautifulSoup(response.text, 'html.parser')
    
    groups = []
    
    # Find all links that lead to message threads
    for a in soup.find_all('a', href=True):
        if '/messages/read/?tid=' in a['href']:
            name = a.text.strip()
            uid = a['href'].split('tid=')[1]
            groups.append({'name': name, 'uid': uid})
    
    return groups

# Example usage with cookie
cookie = "YOUR_FACEBOOK_COOKIE_HERE"
groups = get_messenger_group_uid(cookie)

if groups:
    for group in groups:
        print(f"Group Name: {group['name']} - UID: {group['uid']}")
else:
    print("No groups found or invalid cookie.")
