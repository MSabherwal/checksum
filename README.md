= Checksum_authentication


Checksum authentication contains a flask server that speaks json,
Taking a url as input and returning that same url with a checksum of the 
current url(query parameters included)

= Routes

  POST '/createchecksum'
  	-Data
  		Type: application/json
  		Values:
  			{'url':'url_to_be_checksumed'}
  	-Return value:
  		-On Success:
  			Status_code: 200
  			Data:
  				{'callback_url': 'url_with_checksum'}
  		-On Failure
  			Status_code: 400
  			Data:
  				{'error':'error description'}
  		-On Error:
  			Status_code: 400
  			Data:
  				{'error': 'some error message'}

  POST '/checkchecksum'
  	-Data:
  		Type: application/json
  		Values:
  			{'callback_url': 'url_with_checksum'}
  	-Return value:
  		-On Success:
  			Status_code: 200
  			Data:
  				{'status': 'Valid'}
  		-On Failure:
  			Status_code: 400
  			Data:
  				{'status':'Invalid'}
  		-On Error:
  			Status_code: 400
  			Data:
  				{'error': 'some error message'}

=Running code
	#python checksum.py