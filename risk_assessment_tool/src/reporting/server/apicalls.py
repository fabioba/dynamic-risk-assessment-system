import requests
import logging

logger=logging.getLogger(__name__)

#Specify a URL that resolves to your workspace
URL = "http://127.0.0.1/"



def get_response(name_endpoint):
    """
    Get the response from server

    Args:
        name_endpoint(str)
    """
    try:
        response=requests.get('http://127.0.0.1:8000/'.format(name_endpoint))

        if response.status_code==200: 
            predicts=response.content
        else:
            raise KeyError('status!=200')


        return predicts
    except Exception as err:
        logger.exception(err)

if __name__=='__main__':

    list_response=list()
    #Call each API endpoint and store the responses
    list_response.append(get_response('prediction'))
    list_response.append(get_response('scoring'))
    list_response.append(get_response('summarystats'))
    list_response.append(get_response('diagnostics'))
    
    # store all responses
    with open('apireturns.txt','a+') as handler:
        for resp in list_response:
            handler.write(resp)
        
    #combine all API responses
    #responses = #combine reponses here

    #write the responses to your workspace