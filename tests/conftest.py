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
import json
import sys
import pathlib
import os

sys.path.append('..')
from dotenv import dotenv_values

from rdp_controller import rdp_http_controller
from app import convert_pandas

config = dotenv_values('../.env.test')

@pytest.fixture
def supply_test_config():
    return config


@pytest.fixture
def supply_test_class():
    return rdp_http_controller.RDPHTTPController()

@pytest.fixture
def supply_test_app():
    return convert_pandas

@pytest.fixture
def supply_test_mock_json():
    #  Mock the RDP Auth Token success Response JSON
    valid_auth_json = {
        'access_token': 'access_token_mock1mock2mock3mock4mock5',
        'refresh_token': 'refresh_token_mock1mock2mock3mock4mock5',
        'expires_in': '600',
        'scope': 'test1 test2 test3 test4 test5',
        'token_type': 'Bearer'
    }

    # Mock the RDP Auth Token Expire Response JSON
    token_expire_json = {
        'error': {
            'id': 'XXXXXXXXXX',
            'code': '401',
            'message': 'token expired',
            'status': 'Unauthorized'
        }
    }

    invalid_auth_json = {
        'error': 'invalid_client',
        'error_description': 'Invalid Application Credential.',
    }

    search_explore_payload = {
        'View': 'Entities',
        'Filter': '',
        'Select': 'IssuerCommonName,DocumentTitle,RCSExchangeCountryLeaf,IssueISIN,ExchangeName,ExchangeCode,SearchAllCategoryv3,RCSTRBC2012Leaf',
    }


    return {
        'valid_auth_json': valid_auth_json,
        'invalid_auth_json': invalid_auth_json,
        'token_expire_json': token_expire_json,
        'search_explore_payload': search_explore_payload
    }

