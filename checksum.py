from flask import Flask,request,jsonify
import json
import os

import urlparse
import hmac
import hashlib
import base64
import urllib


app = Flask(__name__)


SECRET_KEY = os.urandom(20) #For now, use random secret_key

#/createchecksum verifies
@app.route("/createchecksum",methods=["POST"])
def create_check_sum():
	try:
		req_body = json.loads(request.data)
		callback_url = req_body['url']
	except KeyError, e:
		return jsonify({'error':'no json key url' }),400
	except ValueError,e:
		return jsonify({'error':'no json in body'}),400
		
	
	signature = create_signature(callback_url)
	
	final_url = add_checksum(callback_url,signature)

	
	
	return jsonify({"callback_url":final_url})

@app.route("/checkchecksum",methods=["POST"])
def check_check_sum():
	try:
		req_body = json.loads(request.data)
		callback_url = req_body['callback_url']
	except KeyError, e:
		return jsonify({'error':'no json key url' }),400
	except ValueError,e:
		return jsonify({'error':'no json in body'}),400

	try:
		clean_callback,checksum = callback_without_checksum(callback_url)
	except KeyError:
		return jsonify({'error':'no checksum in url' }),400
	#recreate checksum
	recreate_checksum = create_signature(clean_callback)
	if recreate_checksum == checksum:
		return jsonify({"status":"Valid"}),200
	else:
		return jsonify({"status":"Invalid"}),400
	

def create_signature(callback_url):
	digest = hmac.new(SECRET_KEY, msg=callback_url, digestmod=hashlib.sha256).digest()
	
	
	signature = base64.b64encode(digest)
	return signature

def add_checksum(callback_url,signature):
	url_parts = list(urlparse.urlparse(callback_url))
	query = dict(urlparse.parse_qsl(url_parts[4]))
	query.update({'checksum':signature})
	url_parts[4] = urllib.urlencode(query)
	return urlparse.urlunparse(url_parts)

def callback_without_checksum(callback_url):
	url_parts = list(urlparse.urlparse(callback_url))
	query = dict(urlparse.parse_qsl(url_parts[4]))
	try:
		checksum= query['checksum']
	except KeyError,e:
		raise

	del query['checksum']
	
	url_parts[4] = urllib.urlencode(query)
	new_url = urlparse.urlunparse(url_parts)
	
	return new_url,checksum



if __name__ == "__main__":
	app.debug = True
	app.run()