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
sys.path.append('..')
from dotenv import dotenv_values

from rdp_controller import rdp_http_controller

#app = rdp_http_controller.RDPHTTPController()

config = dotenv_values("../.env.test")

@pytest.fixture
def supply_test_config():
    #return { 'config': config, 'app': app}
    return config

@pytest.fixture
def supply_test_app():
    app = rdp_http_controller.RDPHTTPController()
    return app

@pytest.fixture
def supply_test_mock_data():
    valid_auth_json = None
    # Loading Mock the RDP Auth Token success Response JSON
    with open('./fixtures/rdp_test_auth_fixture.json', 'r') as file_input:
        valid_auth_json = json.loads(file_input.read())

    valid_esg_json = None
    # Loading Mock RDP ESG View Score valid response JSON
    with open('./fixtures/rdp_test_esg_fixture.json', 'r') as file_input:
        valid_esg_json = json.loads(file_input.read())

    token_expire_json = None
    # Mock the RDP Auth Token Expire Response JSON
    with open('./fixtures/rdp_test_token_expire_fixture.json', 'r') as file_input:
        token_expire_json = json.loads(file_input.read())

    invalid_auth_json = {
        'error': 'invalid_client',
        'error_description':'Invalid Application Credential.'
    }

    invalid_esg_ric_json = {
        'error': {
            'code': 412,
            'description': 'Unable to resolve all requested identifiers.'
        }
    }
    
    return { 
        'valid_auth_json': valid_auth_json,
        'invalid_auth_json': invalid_auth_json,
        'valid_esg_json': valid_esg_json,
        'token_expire_json': token_expire_json,
        'invalid_esg_ric_json': invalid_esg_ric_json
        }