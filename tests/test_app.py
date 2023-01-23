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
import pandas as pd

@pytest.mark.test_app
def test_can_convert_json_to_pandas(supply_test_app, shared_datadir ):
    """
    Test that the convert_pandas function can convert JSON to Pandas
    """
    # Mock RDP ESG View Score valid response JSON
    contents = (shared_datadir / 'test_esg_fixture.json').read_text()
    mock_esg_data = json.loads(contents)

    convert_pandas = supply_test_app

    # Call convert_pandas method
    result = convert_pandas(mock_esg_data)

    # Verify if result is none empty Pandas Dataframe object
    assert type(result) is pd.DataFrame, 'Main app convert_pandas() method return wrong data type'
    assert not result.empty, 'Main app convert_pandas() method return wrong data'


@pytest.mark.test_app
def test_can_covert_json_none(supply_test_app):
    """
    Test that the convert_pandas function can convert JSON to Pandas
    """

    convert_pandas = supply_test_app

    with pytest.raises(TypeError) as excinfo:
        result = convert_pandas(None)
    
    assert 'Received invalid (None or Empty) JSON data' in str(excinfo.value),'Empty convert_pandas method call return wrong Exception description'

@pytest.mark.test_app
def test_can_convert_json_invalid(supply_test_app):
    """
    Test that the convert_pandas function can convert JSON to Pandas
    """

    convert_pandas = supply_test_app

    with pytest.raises(TypeError) as excinfo:
        result = convert_pandas({'message':'Invalid'})
    
    assert 'Error converting JSON to Dataframe' in str(excinfo.value),'Invalid JSON convert_pandas method call return wrong Exception description'

if __name__ == '__main__':
    print('This is the test_app.py test file')