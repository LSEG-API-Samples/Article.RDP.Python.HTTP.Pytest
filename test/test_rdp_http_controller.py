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
import os
import sys


def test_fixture(supply_test_config, supply_test_app):
    assert supply_test_config['RDP_BASE_URL'] == 'https://api.refinitiv.com', 'RDP URL invalid'
    assert supply_test_app.get_scope() == 'trapi', 'RDP Scope invalid'

def test_fixture_login(supply_test_config,supply_test_app, supply_test_mock_data, requests_mock):
    """
    Test that it can log in to the RDP Auth Service
    """
    
    auth_endpoint = supply_test_config['RDP_BASE_URL'] + supply_test_config['RDP_AUTH_URL']
    username = supply_test_config['RDP_USERNAME']
    password = supply_test_config['RDP_PASSWORD']
    client_id = supply_test_config['RDP_CLIENTID']

    app = supply_test_app

    access_token = None
    refresh_token = None
    expires_in = 0

    requests_mock.post(
        url= auth_endpoint, 
        json = supply_test_mock_data['valid_auth_json'], 
        status_code = 200,
        headers = {'Content-Type':'application/json'}
        )

    # Calling RDPHTTPController rdp_authentication() method
    access_token, refresh_token, expires_in = app.rdp_authentication(auth_endpoint, username, password, client_id)
    assert access_token is not None
    assert refresh_token is not None
    assert expires_in > 0

def test_login_rdp_refreshtoken(supply_test_config,supply_test_app, supply_test_mock_data, requests_mock):
    """
    Test that it can handle token renewal using the refresh_token
    """
    auth_endpoint = supply_test_config['RDP_BASE_URL'] + supply_test_config['RDP_AUTH_URL']
    username = supply_test_config['RDP_USERNAME']
    password = supply_test_config['RDP_PASSWORD']
    client_id = supply_test_config['RDP_CLIENTID']

    
    access_token = 'new_access_token_mock1mock2mock3mock4mock5mock6'
    refresh_token = supply_test_mock_data['valid_auth_json']['refresh_token']
    expires_in = 0

    app = supply_test_app

    requests_mock.post(
        url= auth_endpoint, 
        json = supply_test_mock_data['valid_auth_json'], 
        status_code = 200,
        headers = {'Content-Type':'application/json'}
        )
    
    access_token, refresh_token, expires_in = app.rdp_authentication(auth_endpoint, username, password, client_id, refresh_token)

    assert access_token is not None
    assert refresh_token is not None
    assert expires_in > 0


def test_login_rdp_invalid(supply_test_config,supply_test_app, supply_test_mock_data, requests_mock):
    """
    Test that it can handle some invalid credentials
    """
    auth_endpoint = supply_test_config['RDP_BASE_URL'] + supply_test_config['RDP_AUTH_URL']
    app = supply_test_app

    access_token = None
    refresh_token = None
    expires_in = 0

    requests_mock.post(
        url= auth_endpoint, 
        json = supply_test_mock_data['invalid_auth_json'], 
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

    #print('Exception: '+ excinfo.exconly(tryshort=True))
    
    assert access_token is None, "Invalid Login returns Access Token"
    assert refresh_token is None, "Invalid Login returns Refresh Token"
    assert expires_in == 0, "Invalid Login returns expires_in"
    assert '401' in str(excinfo.value), "Invalid Login returns wrong HTTP Status Code"
    assert 'RDP authentication failure' in str(excinfo.value),"Invalid Login returns wrong Exception description"

    json_error = json.loads(str(excinfo.value).split('-')[1])
    assert type(json_error) is dict, "Invalid Login returns wrong Exception detail type"

def test_login_rdp_none_empty_params(supply_test_app):
    """
    Test that the function can handle none/empty input
    """

    app = supply_test_app

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

def test_request_esg(supply_test_config,supply_test_app, supply_test_mock_data, requests_mock):
    """
    Test that it can request ESG Data
    """
    esg_endpoint = supply_test_config['RDP_BASE_URL'] + supply_test_config['RDP_ESG_URL']

    app = supply_test_app

    universe = 'TEST.RIC'

    requests_mock.get(
        url= esg_endpoint, 
        json = supply_test_mock_data['valid_esg_json'], 
        status_code = 200,
        headers = {'Content-Type':'application/json'}
        )

    # Calling RDPHTTPController rdp_authentication() method
    response = app.rdp_request_esg(
        esg_endpoint, supply_test_mock_data['valid_auth_json']['access_token'], 
        universe)
    # verifying basic response
    assert type(response) is dict, "Invalid Data type returns"
    assert 'data' in response
    assert 'headers' in response
    assert 'universe' in response

if __name__ == '__main__':
    test_login_rdp_success()