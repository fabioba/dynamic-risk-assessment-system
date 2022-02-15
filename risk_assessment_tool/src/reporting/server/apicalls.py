import requests
import logging
from risk_assessment_tool import config

# set logging dict
config.set_logger()

logger=logging.getLogger(__name__)

def get_response(name_endpoint):
    """
    Get the response from server

    Args:
        name_endpoint(str)
    """
    try:
        logger.info('name_endpoint: {}'.format(name_endpoint))

        response=requests.post('http://127.0.0.1:8000/'.format(name_endpoint))

        logger.info('response: {}'.format(response))

        if response.status_code==200: 
            predicts=response.content
        else:
            predicts=''
        


        return predicts
    except Exception as err:
        logger.exception(err)
        raise

if __name__=='__main__':
    
    get_response('test')

    list_response=list()
    #Call each API endpoint and store the responses
    #list_response.append(get_response('prediction'))
    #list_response.append(get_response('scoring'))
    #list_response.append(get_response('summarystats'))
    #list_response.append(get_response('diagnostics'))
    
    # store all responses
    #with open('apireturns.txt','a+') as handler:
    #    for resp in list_response:
    #        handler.write(resp)
        
    #combine all API responses
    #responses = #combine reponses here

    #write the responses to your workspace