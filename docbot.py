from wit import Wit

#global vlues from wit.ai as keywords defines in wit.ai
academics=['PG','Graduation','12','10']
doctype_academics=['marksheet','degree']
doctype_nonacademics=['Adhaar Card','Pan Card','Driving Licence','Passport','Voter Id','Resume']

acctoken=""
client=Wit(access_token=acctoken)

def wit_ai_response(msg):
	try:
		resplist=[]
		errorlist=[]
		resp=client.message(msg)
		#print(resp)
		entities_dict,entities_list=resp['entities'],list(resp['entities'])
		#print(entities_dict)
		#print(entities_list)
		if 'academics' in entities_list and 'doctype_nonacademics' in entities_list or not entities_list:
			#print('Please ask the right document.')
			errorlist.append('Please ask the right document.')

		for i in entities_list:
			#print(entities_dict[i][0]['value'])
			resplist.append(entities_dict[i][0]['value'])	

		if not errorlist:
			print(''.join(resplist))
			return resplist
		else:
			#print(errorlist)
			return errorlist
	except Exception as ex:
		print ("wit_ai_response exception "+str(ex))
#wit_ai_response()		