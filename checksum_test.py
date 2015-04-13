import os
import checksum
import unittest
import checksum
import json
import hmac
import base64
import hashlib
import urlparse


class ChecksumTestCase(unittest.TestCase):

    def setUp(self):
        checksum.app.config['TESTING'] = True
        self.app = checksum.app.test_client()

    # def tearDown(self):
    #     return

    def serverChecksum(self,*test_input):
    	# test_input = {'url':'www.google.com?hello=world'}
    	
    	req_data = json.dumps(test_input[1])
    	
    	
    	rv = self.app.post('/createchecksum',data=req_data)
    	
    	resp_body = json.loads(rv.data)

    	callback_url = resp_body['callback_url']
    	
    	url_parts = list(urlparse.urlparse(callback_url))
    	query = dict(urlparse.parse_qsl(url_parts[4]))
    	return query['checksum']

    def createSignature(self,*url):
    	
    	secret_key = checksum.SECRET_KEY
    	digest = hmac.new(secret_key, msg=url[1], digestmod=hashlib.sha256).digest()
    	signature = base64.b64encode(digest)
    	return signature

    def test_createchecksum(self):
    	


    	test_input = [
    	{'url':'www.somthing.com?what=is&hello=world'},
    	{'url':'www.google.com?hello=world'}
    	]
    	for x in test_input:	
    		resp_checksum = self.serverChecksum(self,x)
    		url = x['url']
    		generated_checksum = self.createSignature(self,url)
    		self.assertEqual(resp_checksum, generated_checksum)

    def test_checkchecksum(self):

    	test_input_valid = [
    	{'url':'www.somthing.com?what=is&hello=world'},
    	{'url':'www.google.com?hello=world'}
    	]
    	for x in test_input_valid:
    		req_data = json.dumps(x)
    		# generate callback with checksum
    		rv = self.app.post('/createchecksum',data=req_data)

    		# pass to checkchecksum
    		rv_2 = self.app.post('/checkchecksum',data=rv.data)
    		#ensure that it it works properly
    		self.assertEqual(rv.status_code,200)
    	test_input_invalid = [
    	{'callback_url':'www.google.com'},
    	{'callback_url':'somethinelse'}
    	]
    	for x in test_input_invalid:
    		json_data = json.dumps(x)
    		rv_2 = self.app.post('/checkchecksum',data=json_data)
    		self.assertEqual(rv_2.status_code,400)


if __name__ == '__main__':
    unittest.main()