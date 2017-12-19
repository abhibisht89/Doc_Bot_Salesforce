import json
import requests


def connect(userId,docType):

	payload = {
	            'grant_type':       'password',
	            'client_id':        '',
	            'client_secret':    '',
	            'username':         '',
	            'password':         ''
			}

	loginUrl = "https://login.salesforce.com/services/oauth2/token"
	headerPayload = {"Content-Type":"application/x-www-form-urlencoded"}

	try:
		resp_str = requests.post(loginUrl, headers=headerPayload,data=payload)
		#print(resp_str)
		#print(str(resp_str.status_code))
		#print(str(resp_str.headers))
		#print(str(resp_str.text))
		resp_dict = json.loads(resp_str.text)
		#print(resp_dict)
		access_token_value=resp_dict.get("access_token")
		instance_url=resp_dict.get("instance_url")
		#print(str(access_token_value))
		#print(str(instance_url))
		get_doc_rest_endpoint='https://abhibisht89-dev-ed.my.salesforce.com/services/apexrest/V1.0/GetDocumetsViaRest?userId=%s&docType=%s' % (userId,docType)
		headerPayload = {'Authorization':'OAuth '+access_token_value,'Content-Type':'/x-www-form-urlencoded'}
		resp_str=requests.get(get_doc_rest_endpoint,headers=headerPayload)
		resp_dict = json.loads(resp_str.text)
		responseCode=resp_dict.get("responseCode")
		#print(responseCode)
		docBodyList=resp_dict.get("docBodyList")[0]
		#print(docBodyList)
		return responseCode,docBodyList
	except Exception as e:
		msg = "Error >> couldn't get login token  >>>>" + str(e)
		print(msg)
#connect()
