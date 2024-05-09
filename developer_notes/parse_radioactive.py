"""
    i few code samples that lets you communicate with https://radioactive.digital/communication
"""
import bs4 as bs
import requests

# login to session with developer credentials
login_url = 'https://radioactive.digital/login'
session = requests.Session()
session.post(login_url, json={ 'email': email, 'password': password})

# send request to communicate
comm_url = 'https://radioactive.digital/communication'
data = {'frequency': freq, "id": id, "password": pw, "command": command}
x = session.post(comm_url, json=data)

# parse response
soup = bs.BeautifulSoup(x.content, 'html.parser')
supa = soup.find(attrs={'id': 'enc_message'})
print(supa.text)