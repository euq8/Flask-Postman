#!/usr/bin/env node

const https = require('https'); // used when a server uses https
const http = require('http');   // used when a server users http
const fs = require('fs');       // used for file system operations

//------------------------------------------CLIENT-------------------------------------------------------
let test_url = 'http://127.0.0.1:5000/test_js';
let post_slack_url = 'http://127.0.0.1:5000/slack-post';

// LIST OF ATTACHMENT FILES
// EACH ATTACHMENT FILE - ('name', 'content-bytes like object or str', 'type')
const files_list = [
	['iphone.png', '/home/ashfaque/Documents/SLACK_APIs/sBot/s5.png', 'png'],
	['tester.py', '/home/ashfaque/Documents/SLACK_APIs/sBot/app_ui.py', 'python']
]

// MESSAGE FILE
const payload = {
    channel: 'audit-alerts',
    text: 'Hello World',
};


// FILES <- MESSAGE FILE
const files = {
	message_file : ['message', JSON.stringify(payload), 'application/json']
}

// FILES <- ATTACHMENT FILES
for (const file of files_list){
	files[`attachment_${file[0]}`] = [file[0], fs.readFileSync(file[1]), file[2]];
}

// (OPTIONS for REQUEST CONFIG) / HEADERS
const options = {
	host: 'localhost',
	port: 5000,
	path: '/slack-post',
	method: 'POST',
	headers: {
		'Accept': 'application/json',
		'Content-Type': 'application/json; charset=UTF-8',
		'User-Agent': 'ES6' // set User-Agent = 'Python3'
	}
};

// CREATE REQUEST OBJECT
let request = http.request(options, (res)=>{
				if( res.statusCode !== 201 && res.statusCode !== 200 ) {
					console.error(`Did not get a Created from the server. Code: ${res.statusCode}`);
					res.resume();
					return;
				}

				let data = '';
				res.on('data', (chunk) => {data += chunk;});
				res.on('close', () => {console.log(JSON.parse(data));});
			});

// POST POST POST
request.write(JSON.stringify(files));
request.end();
request.on('error', (err)=>{
	console.error(`Encountered an error trying to make a request: ${err.message}`);
});

//-------------------------------------------------------------------------------------------------------