import os, sys
from flask import Flask, request
from docbot import wit_ai_response
from salesforce_integration import connect

import json
import requests
import base64
import traceback

app = Flask(__name__)

PAGE_ACCESS_TOKEN = ""

@app.route('/', methods=['GET'])
def verify():
	# Webhook verification
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == "": #put your varify token
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200   
    return "Hello world", 200


def get_messaging_text_sender_id_recipient_id_from_messenger(data):
	try:
		if data['object'] == 'page':
			for entry in data['entry']:
				for messaging_event in entry['messaging']:
					# IDs
					sender_id = messaging_event['sender']['id']
					recipient_id = messaging_event['recipient']['id']

					if messaging_event.get('message'):
						# Extracting text message
						if 'text' in messaging_event['message']:
							messaging_text = messaging_event['message']['text']
						else:
							messaging_text = 'no_text'	
						return messaging_text,sender_id,recipient_id									
	except Exception as ex:
		print ("get_messaging_text_sender_id_recipient_id_from_messenger exception "+str(ex))
		print("There is an exception from function " + str(traceback.extract_stack(None, 2)[0][2]))

def check_for_greeting_messages(messaging_text):
	try:
		greetlist=['hi','hii','hiii','hey','thanks','thank','thank you','thank u','hello','helloo']
		greetlist1=['thanks','thank','thank you','thank u']
		is_greetresp=False
		if(messaging_text.lower() in greetlist):
								is_greetresp=True
								if(messaging_text.lower() in greetlist1):
									greetresp='Your Welcome.'
								else:	
									greetresp='Hi, I am you personal document bot. I can send you document regarding your query.'
								return greetresp,is_greetresp
		else:
			is_greetresp=False
			return "no_text",is_greetresp
									
	except Exception as ex:
			print ("check_for_greeting_messages exception "+str(ex))
			print("There is an exception from function " + str(traceback.extract_stack(None, 2)[0][2]))

def prepare_response_content_generic(sender_id,text):
	try:
		response_content = {
							"recipient":{
							"id": sender_id
										},
											"message": {
											"text": str(text)	            
											}
							}
		return response_content
	except Exception as ex:
		print ("prepare_response_content_generic exception "+str(ex))
		print("There is an exception from function " + str(traceback.extract_stack(None, 2)[0][2]))	

def prepare_response_content_blob(sender_id,text,url,title='View Document'):
	try:
		response_content = {
								"recipient": {
											"id": sender_id
											},
								"message":{
											"attachment":{
											"type":"template",
											"payload":{
											"template_type":"button",
											"text":text,
											"buttons":[
											{
											"type":"web_url",
											"url":url,
											"title":title
											}]}}}
							}
		return response_content
	except Exception as ex:
		print ("prepare_response_content_blob exception "+str(ex))
		print("There is an exception from function " + str(traceback.extract_stack(None, 2)[0][2]))	


def prepare_response_content_buttons(sender_id,text,url,title='Read More'):
	try:
			response_content = {
								"recipient": {
											"id": sender_id
											},
								"message":{
											"attachment":{
											"type":"template",
											"payload":{
											"template_type":"button",
											"text":text,
											"buttons":[
											{
											"type":"web_url",
											"url":url,
											"title":title
											}]}}}}
			return response_content
	except Exception as ex:
			print ("prepare_response_content_buttons exception "+str(ex))
			print("There is an exception from function " + str(traceback.extract_stack(None, 2)[0][2]))	

def send_response_to_messenger(response_content):
	try:
			headers = {"Content-Type": "application/json"}
			url = "https://graph.facebook.com/v2.6/me/messages?access_token=%s" % PAGE_ACCESS_TOKEN
			resp_str = requests.post(url, data=json.dumps(response_content), headers=headers)
			return resp_str
	except Exception as ex:
			print ("send_response_to_messenger exception "+str(ex))
			print("There is an exception from function " + str(traceback.extract_stack(None, 2)[0][2]))				

@app.route('/', methods=['POST'])
def webhook():
	data = request.get_json()
	#log(body)
	try:
		messaging_text,sender_id,recipient_id=get_messaging_text_sender_id_recipient_id_from_messenger(data)
		greetresp,is_greetresp=check_for_greeting_messages(messaging_text)
		if is_greetresp is True:
			response_content=prepare_response_content_generic(sender_id,greetresp)
			resp_str=send_response_to_messenger(response_content)
		else:	
			resplist= wit_ai_response(messaging_text)
			#print(resplist)
			#response_content=prepare_response_content_generic(sender_id,resplist)
			#resp_str=send_response_to_messenger(response_content)
			responseCode,docBodyList=connect(sender_id,''.join(resplist))
			if responseCode=='200':
				response_content=prepare_response_content_blob(sender_id,'This is your '+''.join(resplist),str(docBodyList),title='View Document')
				resp_str=send_response_to_messenger(response_content)
				print(resp_str)
				print(str(resp_str.status_code))
				print(str(resp_str.headers))
				print(str(resp_str.text))
			else:
				response_content=prepare_response_content_generic(sender_id,"There is no document related to your query")
				resp_str=send_response_to_messenger(response_content)
	except Exception as ex:
    		print ("main class exp "+str(ex))	

	return "ok", 200

def log(message):
	print(message)
	sys.stdout.flush()

if __name__ == "__main__":
	app.run(debug=True)