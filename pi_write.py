from requests.auth import HTTPBasicAuth
from requests_kerberos import HTTPKerberosAuth
import requests
import json


OSI_AF_DATABASE = 'HPF'
OSI_AF_ELEMENT = 'PULP PLANT'
OSI_AF_ELEMENT_CHILD = 'LAB DATA'
OSI_AF_ATTRIBUTE_TAG = 'HPF-PI-CH-UPTO-1/8'

def call_headers(include_content_type):
    """ Create API call headers
        @includeContentType boolean: Flag determines whether or not the
        content-type header is included
    """
    if include_content_type is True:
        header = {
            'content-type': 'application/json',
            'X-Requested-With': 'XmlHttpRequest'
        }
    else:
        header = {
            'X-Requested-With': 'XmlHttpRequest'
        }

    return 

def call_security_method(security_method, user_name, user_password):
    """ Create API call security method
        @param security_method string: Security method to use: basic or kerberos
        @param user_name string: The user's credentials name
        @param user_password string: The user's credentials password
    """

    from requests.auth import HTTPBasicAuth
    from requests_kerberos import HTTPKerberosAuth

    if security_method.lower() == 'basic':
        security_auth = HTTPBasicAuth(user_name, user_password)
    else:
        security_auth = HTTPKerberosAuth(mutual_authentication='REQUIRED',
                                         sanitize_mutual_error_response=False)

    return security_auth




def write_single_value(piwebapi_url, asset_server, user_name, user_password,
                       piwebapi_security_method, verify_ssl):
    """ Write a single value to the sampleTag
        @param piwebapi_url string: The URL of the PI Web API
        @param asset_server string: Name of the Asset Server
        @param user_name string: The user's credentials name
        @param user_password string: The user's credentials password
        @param piwebapi_security_method string: Security method: basic or kerberos
        @param verify_ssl: If certificate verification will be performed
    """
    print('writeSingleValue')

    #  create security method - basic or kerberos
    security_method = call_security_method(
        piwebapi_security_method, user_name, user_password)

    #  Get the sample tag
    request_url = '{}/attributes?path=\\\\{}\\{}\\{}\\{}|{}'.format(
        piwebapi_url, asset_server, OSI_AF_DATABASE, OSI_AF_ELEMENT, OSI_AF_ELEMENT_CHILD, OSI_AF_ATTRIBUTE_TAG)
    print(request_url)
    response = requests.get(request_url, auth=security_method, verify=verify_ssl)

    #  Only continue if the first request was successful
    if response.status_code == 200:
        print('Connected with PI server')
        data = json.loads(response.text)
         #  Create the data for this call
        data_value = random.randint(1, 100)
        request_body = {
            'Value': data_value
        }

        #  Create the header
        header = call_headers(True)

        #  Write the single value to the tag
        response = requests.post(data['Links']['Value'], auth=security_method,
                                 verify=verify_ssl, json=request_body, headers=header)

        if response.status_code == 202:
            print('Attribute SampleTag write value ' + str(data_value))
        else:
            print(response.status_code, response.reason, response.text)
    else:
        print(response.status_code, response.reason, response.text)

piwebapi_url = 'https://gilvsfhrh-pi1/piwebapi/'
asset_server = 'GILVSFHRH-PI1'
username = 's.k'
password = '9!qAtW50#'
piwebapi_security_method = 'basic'
write_single_value(piwebapi_url, asset_server, username, password, piwebapi_security_method, False)
