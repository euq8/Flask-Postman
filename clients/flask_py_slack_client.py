#!/usr/bin/env python3

import requests
import json
from pprint import pprint

#------------------------------------------CLIENT-------------------------------------------------------

test_url = 'http://127.0.0.1:5000/test_py'
post_slack_url = 'http://127.0.0.1:5000/slack-post'

# LIST OF ATTACHMENT FILES
# EACH ATTACHMENT FILE - ('name', 'content-bytes like object or str', 'type')
files_list = [
	('iphone.png', '/home/ashfaque/Documents/SLACK_APIs/sBot/s5.png', 'png'),
	('tester.py', '/home/ashfaque/Documents/SLACK_APIs/sBot/app_ui.py', 'python')
]

# MESSAGE FILE
payload = {
	'channel':'audit-alerts',
	'text':'Hello World',
}

# FILES <- MESSAGE FILE
files = {
	'message_file' : ('message', json.dumps(payload), 'application/json')
}

# FILES <- ATTACHMENT FILES
for f in files_list:
	files[f'attachment_{f[0]}'] = (f[0], open(f[1], 'rb'), f[2])

# HEADERS
headers = {
	'User-Agent' : 'Python3'
}

# POST POST POST
r = requests.post(post_slack_url, files=files)

print(str(r.content, 'utf-8'))

#--------------------------------------------------------------------------------------------------------