@RestResource(urlMapping='/V1.0/GetDocumetsViaRest/*')
global class BotAttachmentService {      
    @HttpGet
    global static void getAttachments() {
        RestRequest req = RestContext.request;
        RestResponse res = Restcontext.response;
        res.addHeader('Content-Type', 'application/json');
        res.StatusCode = 200;
        List<string> docBodyList = new List<string>(); 
        Try {
            String userId = RestContext.request.params.get('userId');
            String docType = RestContext.request.params.get('docType');     
            if( !String.isBlank(userId) && !String.isBlank(docType) ) {
                List<Bot_Document__c> docRecList = [select id,doc_url__c from Bot_Document__c where User_Id__c = :userId and Document_Type__c =:docType Limit 1];
                if( !docRecList.isEmpty()) {
                        docBodyList.add(docRecList[0].doc_url__c);               
                    if( !docBodyList.isEmpty() ) {
                        res.responseBody = Blob.valueof(JSON.serialize(new getAttResponse('Success','200',docBodyList)));
                    }//END OF IF 
                    else {
                        res.responseBody = Blob.valueof(JSON.serialize(new getAttResponse('Docs not found','400.1',null))); 
                    }//EN DOF ELSE 
                }
                else {
                    res.responseBody = Blob.valueof(JSON.serialize(new getAttResponse('User record not found','400.2',null)));
                }
            }//END OF IF
            else {
                res.responseBody = Blob.valueof(JSON.serialize(new getAttResponse('Mandatory Field Missing','400.3',null)));    
            }//END OF ELSE
        }//END OF TRY
        Catch( Exception e) {
            res.responseBody = Blob.valueof(JSON.serialize(new getAttResponse('Error while processing request.'+e.getStackTraceString()+'-'+e.getMessage(),'501',null)));
        }//END OF CATCH 
    }//END OF METHOD        
    
    private class getAttResponse {
        String responsemessage;
        String responseCode;
        List<string> docBodyList;
        
        private getAttResponse(String msg, String code, list<string> blobList){
            this.responsemessage = msg;
            this.responseCode = code;
            this.docBodyList = blobList;
        }//END OF CONST 
    }//END OF WRAPPER

}//END OF CLASS