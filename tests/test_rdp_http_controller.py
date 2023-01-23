#|-----------------------------------------------------------------------------
#|            This source code is provided under the MIT license             --
#|  and is provided AS IS with no warranty or guarantee of fit for purpose.  --
#|                See the project's LICENSE.md for details.                  --
#|           Copyright Refinitiv 2023.       All rights reserved.            --
#|-----------------------------------------------------------------------------

"""
Example Code Disclaimer:
ALL EXAMPLE CODE IS PROVIDED ON AN “AS IS” AND “AS AVAILABLE” BASIS FOR ILLUSTRATIVE PURPOSES ONLY. REFINITIV MAKES NO REPRESENTATIONS OR WARRANTIES OF ANY KIND, EXPRESS OR IMPLIED, AS TO THE OPERATION OF THE EXAMPLE CODE, OR THE INFORMATION, CONTENT, OR MATERIALS USED IN CONNECTION WITH THE EXAMPLE CODE. YOU EXPRESSLY AGREE THAT YOUR USE OF THE EXAMPLE CODE IS AT YOUR SOLE RISK.
"""

import pytest
import requests
import json


@pytest.mark.test_valid
@pytest.mark.test_login
def test_rdp_login(supply_test_config,supply_test_class, supply_test_mock_auth_data, requests_mock):
    """
    Test that it can log in to the RDP Auth Service
    """
    
    auth_endpoint = supply_test_config['RDP_BASE_URL'] + supply_test_config['RDP_AUTH_URL']
    username = supply_test_config['RDP_USERNAME']
    password = supply_test_config['RDP_PASSWORD']
    client_id = supply_test_config['RDP_CLIENTID']

    app = supply_test_class

    access_token = None
    refresh_token = None
    expires_in = 0

    requests_mock.post(
        url= auth_endpoint, 
        json = supply_test_mock_auth_data['valid_auth_json'], 
        status_code = 200,
        headers = {'Content-Type':'application/json'}
        )

    # Calling RDPHTTPController rdp_authentication() method
    access_token, refresh_token, expires_in = app.rdp_authentication(auth_endpoint, username, password, client_id)
    assert access_token is not None
    assert refresh_token is not None
    assert expires_in > 0

@pytest.mark.test_valid
@pytest.mark.test_login
def test_login_rdp_refreshtoken(supply_test_config,supply_test_class, supply_test_mock_auth_data, requests_mock):
    """
    Test that it can handle token renewal using the refresh_token
    """
    auth_endpoint = supply_test_config['RDP_BASE_URL'] + supply_test_config['RDP_AUTH_URL']
    username = supply_test_config['RDP_USERNAME']
    password = supply_test_config['RDP_PASSWORD']
    client_id = supply_test_config['RDP_CLIENTID']

    
    access_token = 'new_access_token_mock1mock2mock3mock4mock5mock6'
    refresh_token = supply_test_mock_auth_data['valid_auth_json']['refresh_token']
    expires_in = 0

    app = supply_test_class

    requests_mock.post(
        url= auth_endpoint, 
        json = supply_test_mock_auth_data['valid_auth_json'], 
        status_code = 200,
        headers = {'Content-Type':'application/json'}
        )
    
    access_token, refresh_token, expires_in = app.rdp_authentication(auth_endpoint, username, password, client_id, refresh_token)

    assert access_token is not None
    assert refresh_token is not None
    assert expires_in > 0

@pytest.mark.test_login
def test_login_rdp_invalid(supply_test_config,supply_test_class, supply_test_mock_auth_data, requests_mock):
    """
    Test that it can handle some invalid credentials
    """
    auth_endpoint = supply_test_config['RDP_BASE_URL'] + supply_test_config['RDP_AUTH_URL']
    app = supply_test_class

    access_token = None
    refresh_token = None
    expires_in = 0

    requests_mock.post(
        url= auth_endpoint, 
        json = supply_test_mock_auth_data['invalid_auth_json'], 
        status_code = 401,
        headers = {'Content-Type':'application/json'}
        )


    username = 'wrong_user1'
    password = 'wrong_password1'
    client_id = 'XXXXX'
    access_token = None
    refresh_token = None
    expires_in = 0

    with pytest.raises(requests.exceptions.HTTPError) as excinfo:
        access_token, refresh_token, expires_in = app.rdp_authentication(auth_endpoint, username, password, client_id)
    
    assert access_token is None, "Invalid Login returns Access Token"
    assert refresh_token is None, "Invalid Login returns Refresh Token"
    assert expires_in == 0, "Invalid Login returns expires_in"
    assert '401' in str(excinfo.value), "Invalid Login returns wrong HTTP Status Code"
    assert 'RDP authentication failure' in str(excinfo.value),"Invalid Login returns wrong Exception description"

    json_error = json.loads(str(excinfo.value).split('-')[1])
    assert type(json_error) is dict, "Invalid Login returns wrong Exception detail type"

@pytest.mark.empty_case
@pytest.mark.test_login
def test_login_rdp_none_empty_params(supply_test_class):
    """
    Test that the function can handle none/empty input
    """

    app = supply_test_class

    # Set None or Empty parameters
    auth_endpoint = None
    username = ''
    password = None
    client_id = 'XXXXX'
        
    access_token = None
    refresh_token = None
    expires_in = 0

    # Check if TypeError exception is raised
    with pytest.raises(TypeError) as excinfo:
        access_token, refresh_token, expires_in = app.rdp_authentication(auth_endpoint, username, password, client_id)
    
    assert access_token is None, "Empty Login returns Access Token"
    assert refresh_token is None,"Empty Login returns Refresh Token"
    assert expires_in == 0, "Empty Login returns expires_in"
    # Check if the exception message is correct
    assert 'Received invalid (None or Empty) arguments' in str(excinfo.value),"Empty Login returns wrong Exception description"

@pytest.mark.test_valid
@pytest.mark.test_esg
def test_request_esg(supply_test_config,supply_test_class, supply_test_mock_auth_data,supply_test_mock_esg_data, requests_mock):
    """
    Test that it can request ESG Data
    """
    esg_endpoint = supply_test_config['RDP_BASE_URL'] + supply_test_config['RDP_ESG_URL']

    app = supply_test_class

    universe = 'TEST.RIC'

    requests_mock.get(
        url= esg_endpoint, 
        json = supply_test_mock_esg_data['valid_esg_json'], 
        status_code = 200,
        headers = {'Content-Type':'application/json'}
        )

    # Calling RDPHTTPController rdp_request_esg() method
    response = app.rdp_request_esg(
        esg_endpoint, supply_test_mock_auth_data['valid_auth_json']['access_token'], 
        universe)
    # verifying basic response
    assert type(response) is dict, 'Invalid Data type returns'
    assert 'data' in response
    assert 'headers' in response
    assert 'universe' in response

@pytest.mark.test_esg
def test_request_esg_token_expire(supply_test_config,supply_test_class, supply_test_mock_auth_data, requests_mock):
    """
    Test that it can handle token expiration requests
    """
    esg_endpoint = supply_test_config['RDP_BASE_URL'] + supply_test_config['RDP_ESG_URL']
    app = supply_test_class
    universe = 'TEST.RIC'

    requests_mock.get(
        url= esg_endpoint, 
        json = supply_test_mock_auth_data['token_expire_json'], 
        status_code = 401,
        headers = {'Content-Type':'application/json'}
        )
    
    # Calling RDPHTTPController rdp_request_esg() method
    with pytest.raises(requests.exceptions.HTTPError) as excinfo:
        response = app.rdp_request_esg(
            esg_endpoint, supply_test_mock_auth_data['valid_auth_json']['access_token'], 
            universe)
    # verifying basic response

    print('Exception = ' + str(excinfo.value))
    assert '401' in str(excinfo.value), 'Access Token Expire returns wrong HTTP Status Code'
    assert 'Unauthorized' in str(excinfo.value), 'Access Token Expire returns wrong error message'

    json_error = json.loads(str(excinfo.value).split('401 -')[1])
    assert type(json_error) is dict, 'Access Token Expire returns wrong data type'
    assert 'error' in json_error, 'Access Token Expire returns wrong JSON error response'
    assert 'message' in json_error['error'], 'Access Token Expire returns wrong JSON error response'
    assert 'status' in json_error['error'], 'Access Token Expire returns wrong JSON error response'

@pytest.mark.test_esg
def test_request_esg_invalid_ric(supply_test_config,supply_test_class, supply_test_mock_auth_data,supply_test_mock_esg_data, requests_mock):
    """
    Test that it can handle invalid RIC request
    """
    esg_endpoint = supply_test_config['RDP_BASE_URL'] + supply_test_config['RDP_ESG_URL']
    app = supply_test_class
    universe = 'INVALID.RIC'

    requests_mock.get(
        url= esg_endpoint, 
        json = supply_test_mock_esg_data['invalid_esg_ric_json'], 
        status_code = 200,
        headers = {'Content-Type':'application/json'}
        )
    
    # Calling RDPHTTPController rdp_request_esg() method
    response = app.rdp_request_esg(esg_endpoint, supply_test_mock_auth_data['valid_auth_json']['access_token'], universe)

    assert type(response) is dict, 'Invalid ESG request returns wrong data type'
    assert 'error' in response, 'Invalid ESG request returns returns wrong JSON error response'
    assert 'code' in response['error'], 'Invalid ESG request returns wrong JSON error response'
    assert 'description' in response['error'], 'Invalid ESG request returns wrong JSON error response'

@pytest.mark.empty_case
@pytest.mark.test_esg
def test_request_esg_none_empty(supply_test_class, supply_test_mock_auth_data):
    """
    Test that the ESG function can handle none/empty input
    """
    esg_endpoint = None
    app = supply_test_class
    universe = ''

    # Check if TypeError exception is raised
    with pytest.raises(TypeError) as excinfo:
        response = app.rdp_request_esg(esg_endpoint, supply_test_mock_auth_data['valid_auth_json']['access_token'], universe)
    
    # Check if the exception message is correct
    assert 'Received invalid (None or Empty) arguments' in str(excinfo.value),"Empty ESG request returns wrong Exception description"

@pytest.mark.test_valid
@pytest.mark.test_search
def test_request_search_explore(supply_test_config,supply_test_class, supply_test_mock_auth_data,supply_test_mock_search_data, requests_mock):
    """
    Test that it can get RIC's metadata via the RDP Search Explore Service
    """
    search_endpoint = supply_test_config['RDP_BASE_URL'] + supply_test_config['RDP_SEARCH_EXPLORE_URL']
    app = supply_test_class
    universe = 'TEST.RIC'
    payload = supply_test_mock_search_data['search_explore_payload']
    payload['Filter'] =f'RIC eq \'{universe}\''

    requests_mock.post(
        url= search_endpoint, 
        json = supply_test_mock_search_data['valid_search_json'], 
        status_code = 200,
        headers = {'Content-Type':'application/json'}
        )
    
    # Calling RDPHTTPController rdp_request_esg() method
    response = app.rdp_request_search_explore(search_endpoint, supply_test_mock_auth_data['valid_auth_json']['access_token'], payload)

    assert type(response) is dict, 'Search request returns wrong data type'
    assert 'Total' in response
    assert 'Hits' in response

@pytest.mark.test_search
def test_request_search_explore_token_expire(supply_test_config,supply_test_class, supply_test_mock_auth_data,supply_test_mock_search_data, requests_mock):
    """
    Test that it can handle token expiration requests
    """
    search_endpoint = supply_test_config['RDP_BASE_URL'] + supply_test_config['RDP_SEARCH_EXPLORE_URL']
    app = supply_test_class
    universe = 'TEST.RIC'
    payload = supply_test_mock_search_data['search_explore_payload']
    payload['Filter'] =f'RIC eq \'{universe}\''

    requests_mock.post(
        url= search_endpoint, 
        json = supply_test_mock_auth_data['token_expire_json'], 
        status_code = 401,
        headers = {'Content-Type':'application/json'}
        )
    
    # Calling RDPHTTPController rdp_request_search_explore() method
    with pytest.raises(requests.exceptions.HTTPError) as excinfo:
        response = app.rdp_request_search_explore(search_endpoint, supply_test_mock_auth_data['valid_auth_json']['access_token'], payload)

    # verifying basic response

    print('Exception = ' + str(excinfo.value))
    assert '401' in str(excinfo.value), 'Access Token Expire returns wrong HTTP Status Code'
    assert 'Unauthorized' in str(excinfo.value), 'Access Token Expire returns wrong error message'

    json_error = json.loads(str(excinfo.value).split('401 -')[1])
    assert type(json_error) is dict, 'Access Token Expire returns wrong data type'
    assert 'error' in json_error, 'Access Token Expire returns wrong JSON error response'
    assert 'message' in json_error['error'], 'Access Token Expire returns wrong JSON error response'
    assert 'status' in json_error['error'], 'Access Token Expire returns wrong JSON error response'

@pytest.mark.test_search
def test_request_search_explore_invalid_json(supply_test_config,supply_test_class, supply_test_mock_auth_data,supply_test_mock_search_data, requests_mock):
    """
    Test that it can handle invalid JSON request payload
    """
    search_endpoint = supply_test_config['RDP_BASE_URL'] + supply_test_config['RDP_SEARCH_EXPLORE_URL']
    app = supply_test_class
    payload = {'TestKey': 'InvalidValue'}

    requests_mock.post(
        url= search_endpoint, 
        json = supply_test_mock_search_data['invalid_explore_payload'], 
        status_code = 400,
        headers = {'Content-Type':'application/json'}
        )
    
    # Calling RDPHTTPController rdp_request_search_explore() method
    with pytest.raises(requests.exceptions.HTTPError) as excinfo:
        response = app.rdp_request_search_explore(search_endpoint, supply_test_mock_auth_data['valid_auth_json']['access_token'], payload)

    # verifying basic response

    print('Exception = ' + str(excinfo.value))
    assert '400' in str(excinfo.value), 'Invalid Search explore returns wrong HTTP Status Code'
    assert 'Bad Request' in str(excinfo.value), 'Invalid Search explore returns wrong error message'

    json_error = json.loads(str(excinfo.value).split('400 -')[1])
    assert type(json_error) is dict, 'Invalid Search explore returns wrong data type'
    assert 'error' in json_error, 'Invalid Search explore returns wrong JSON error response'
    assert 'errors' in json_error['error'], 'Invalid Search explore returns wrong JSON error response'
    assert len(json_error['error']['errors']) > 0, 'Invalid Search explore returns wrong JSON error response'
    assert 'key' in json_error['error']['errors'][0], 'Invalid Search explore returns wrong JSON error response'
    assert 'reason' in json_error['error']['errors'][0], 'Invalid Search explore returns wrong JSON error response'

@pytest.mark.empty_case
@pytest.mark.test_search
def test_request_search_explore_none_empty(supply_test_class,supply_test_mock_auth_data):
    """
    Test that the Search Explore function can handle none/empty input
    """
    search_endpoint = ''
    app = supply_test_class
    payload = {}

    # Check if TypeError exception is raised
    with pytest.raises(TypeError) as excinfo:
        response = app.rdp_request_search_explore(search_endpoint, supply_test_mock_auth_data['valid_auth_json']['access_token'], payload)
    
    # Check if the exception message is correct
    assert 'Received invalid (None or Empty) arguments' in str(excinfo.value),"Empty Search explore request returns wrong Exception description"

if __name__ == '__main__':
    print('This is a test file')
