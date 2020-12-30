#!/usr/bin/env python3

from flask     import Flask, request
from slack_sdk import WebClient
from pprint    import pprint
from ast       import literal_eval

import requests
import os

# SLACK_TOKEN is an ENVIRONMENT VARIABLE
stoken = os.environ['SLACK_TOKEN']

app = Flask(__name__)

slackClient = WebClient(token=stoken)

@app.route('/test_js', methods=['POST'])
def test_js():
	# you can test javascript client request inside this
	print(request.headers)
	print(request.files)
	data = literal_eval(request.get_data().decode())
	t = data['attachment_file']
	d = data['message_file']
	print('attachment_file - ',t.keys())
	print('type of attachment_file - ', t['type'])
	print('message_file - ', type(d))

	#--------------------------------------------------------------
	# bytes() is used to convert list of int to bytes object, 
	# which is writeable in the original format
	# with open('f.png', 'wb') as f:
	# 	 f.write(bytes(t['data']))
	#--------------------------------------------------------------

	for k,v in data.items():
		print(k,'-------',type(v))
		print()
	print(request.headers)
	print(request.json)
	return {'name':'ashfaque hussain'}

@app.route('/test_py', methods=['POST'])
def test_py():
	# you can test python3 client request inside this
	files = request.files
	files_dict  = files.to_dict(flat=False) # convert ImmutableDict of Flask to Python dict
	print(files_dict.keys())
	print(request.headers['User-Agent'])

	for k,v in files_dict.items():
		print(v[0].filename)
		print(v[0].name)
		with open(v[0].filename, 'wb') as f:
			f.write(v[0].read())

	#r_chat_postMessage = slackClient.api_call('chat.postMessage', json={'channel':, 'text':}) # get parameters from files_dict['message_files']
	#r_fileUpload = slackClient.files_upload(channels=, file=, filename=, filetype=) # get parameters from files_dict[f'attachment_{filename}']

	return 'success'

def handle_python3_requests():
	# python3 client requests handler and slack postman
	files = request.files
	files_dict  = files.to_dict(flat=False)
	print(files_dict.keys(),'\n',request.headers['User-Agent'])

	msg = files_dict['message_file'][0]
	msg_dict = literal_eval(msg.read().decode())
	channel = msg_dict['channel']
	text = msg_dict['text']
	r = []
	r.append(slackClient.api_call('chat.postMessage', json={'channel':channel, 'text':text}))
	for k,v in files_dict.items():
		print(v[0].filename)
		if 'attachment' in k:
			r.append(slackClient.files_upload(channels=channel, file=v[0].read(), filename=v[0].filename))
	return

def handle_es6_requests():
	print('HELLO WORLD')
	data = literal_eval(request.get_data().decode())

	print(data.keys())
	message_file = literal_eval(data['message_file'][1])
	channel = message_file['channel']
	text = message_file['text']
	r = []
	#r.append(slackClient.api_call('chat.postMessage', json={'channel':channel, 'text':text}))
	for k,v in data.items(): 
		if 'attachment' in k:
			print(k, v[0], type(bytes(v[1]['data'])), v[2])
			r.append(slackClient.files_upload(channels=channel, file=bytes(v[1]['data']), filename=v[0], filetype=v[2]))


	#attc = data['attachment_file']
	#attc_type = attc['type']
	#attc_data = attc['data']
	#msg = data['message_file']
	#channel = msg['channel']
	#text = msg['text']
	#file_type = msg['file_type']
	#file_name = msg['file_name']

	#print('attachment_file - ',t.keys())
	#print('type of attachment_file - ', t['type'])
	#print('message_file - ', type(d))

	#r_chat = slackClient.api_call('chat.postMessage', json={'channel':channel, 'text':text})
	#r_fu = slackClient.files_upload(channels=channel, file=bytes(attc_data), filename=file_name, filetype=file_type)

	return 
	# answer mill gaya---------------------------------------------
	#with open('f.png', 'wb') as f:
	#	f.write(bytes(t['data']))
	#--------------------------------------------------------------

	#print()
	#for k,v in data.items():
	#	print(k,'-------',type(v))
	#	print()

@app.route('/slack-post', methods=['POST'])
def slack_post():
	print('before user_agent')
	user_agent = request.headers['User-Agent']
	print('after user_agent')

	if 'python' in user_agent:
		try:
			handle_python3_requests()
		except Exception as e:
			print(e)
	else:
		try:
			handle_es6_requests()
		except Exception as e:
			print(e)

	# status to keep track of error, True everything going fine, else False
	status = True
	print('---------------------------------------------------')
	return '<h1>success</h1>'

if __name__ == "__main__":
	app.run(debug=True, port=5000)
