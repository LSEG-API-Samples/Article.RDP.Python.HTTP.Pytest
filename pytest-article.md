# Getting Start Unit Test with Pytest for an HTTP REST Python Application
- version: 1.0
- Last update: Feb 2023
- Environment: Windows
- Prerequisite: [Access to RDP credentials](#prerequisite)

Example Code Disclaimer:
ALL EXAMPLE CODE IS PROVIDED ON AN “AS IS” AND “AS AVAILABLE” BASIS FOR ILLUSTRATIVE PURPOSES ONLY. REFINITIV MAKES NO REPRESENTATIONS OR WARRANTIES OF ANY KIND, EXPRESS OR IMPLIED, AS TO THE OPERATION OF THE EXAMPLE CODE, OR THE INFORMATION, CONTENT, OR MATERIALS USED IN CONNECTION WITH THE EXAMPLE CODE. YOU EXPRESSLY AGREE THAT YOUR USE OF THE EXAMPLE CODE IS AT YOUR SOLE RISK.

## <a id="pytest_intro"></a>Introduction to Python Pytest framework

The [pytest](https://docs.pytest.org/en/7.2.x/) is one of the most popular all-purpose Python testing framework. This open-source framework lets developers/QAs write a small, readable, and scalable test cases that suitable for both simple function testing and complex applications. Comparing to the bulky class-based unit test framework like Python's built-in [unittest](https://docs.python.org/3.9/library/unittest.html), the pytest framework has easier learning curve with more flexibility.

Pytest Features:
- Use the Python standard [assert statement](https://docs.python.org/3.9/reference/simple_stmts.html#assert) for verifying expectations and values in Python tests, no more ```self.assertXXX``` methods like the unittest
- [Auto-discovery](https://docs.pytest.org/en/7.2.x/explanation/goodpractices.html#test-discovery) of test modules and functions
- [Modular fixtures](https://docs.pytest.org/en/7.2.x/reference/fixtures.html#fixture) for managing small or parametrized long-lived test resources
- You can run unittest cases with pytest too!
- Provide a lot of official and community plugins for extending the framework capability and integrations.

The pytest framework has the following requirements:
- The test cases file name must follow the form ```test_*.py``` or ```\*_test.py``` in the current directory and its subdirectories
- The test cases can be ```test``` prefixed test functions or methods outside of class
- The test cases can be ```test``` prefixed test functions or methods inside ```Test``` prefixed test classes (without an ```__init__``` method)
- Uses Python standard assert keyword

Example from [pytest official page](https://docs.pytest.org/en/7.1.x/getting-started.html#create-your-first-test):
``` Python
# test_sample.py
def func(x):
    return x + 1


def test_answer():
    assert func(3) == 5
```

To run the test, just run the following command:
``` bash
pytest .
```
Result:
``` bash
=========================== test session starts ============================
platform linux -- Python 3.x.y, pytest-7.x.y, pluggy-1.x.y
rootdir: /home/sweet/project
collected 1 item

test_sample.py F                                                     [100%]

================================= FAILURES =================================
_______________________________ test_answer ________________________________

    def test_answer():
>       assert func(3) == 5
E       assert 4 == 5
E        +  where 4 = func(3)

test_sample.py:6: AssertionError
========================= short test summary info ==========================
FAILED test_sample.py::test_answer - assert 4 == 5
============================ 1 failed in 0.12s =============================
```

Please find more detail about the pytest framework from the following resources:
- [pytest official page](https://docs.pytest.org/en/7.2.x/)
- [pytest getting started page](https://docs.pytest.org/en/7.2.x/getting-started.html)
- [Using pytest - Real Python](https://realpython.com/lessons/using-pytest/)

## <a id="rdp_workflow"></a>RDP APIs Application Workflow

Refinitiv Data Platform entitlement check is based on OAuth 2.0 specification. The first step of an application workflow is to get a token from RDP Auth Service, which will allow access to the protected resource, i.e. data REST API. 

The API requires the following access credential information:
- Username: The username. 
- Password: Password associated with the username. 
- Client ID: This is also known as ```AppKey```, and it is generated using an App key Generator. This unique identifier is defined for the user or application and is deemed confidential (not shared between users). The client_id parameter can be passed in the request body or as an “Authorization” request header that is encoded as base64.

Once the authentication success, the function gets the RDP Auth service response message and keeps the following RDP token information in the variables.
- **access_token**: The token used to invoke REST data API calls as described above. The application must keep this credential for further RDP APIs requests.
- **refresh_token**: Refresh token to be used for obtaining an updated access token before expiration. The application must keep this credential for access token renewal.
- **expires_in**: Access token validity time in seconds.

Next, after the application received the Access Token (and authorization token) from RDP Auth Service, all subsequent REST API calls will use this token to get the data. Please find more detail regarding RDP APIs workflow in the following resources:
- [RDP APIs: Introduction to the Request-Response API](https://developers.refinitiv.com/en/api-catalog/refinitiv-data-platform/refinitiv-data-platform-apis/tutorials#introduction-to-the-request-response-api) page.
- [RDP APIs: Authorization - All about tokens](https://developers.refinitiv.com/en/api-catalog/refinitiv-data-platform/refinitiv-data-platform-apis/tutorials#authorization-all-about-tokens) page.

## <a id="project_info"></a>Project Structure

This example project is a Python console application that login to the RDP platform, then requests the company's Environmental Social and Governance (ESG) data and meta information from the RDP ESG and Search Explore services respectively. The project structure is as follows:


```
.
├── .env
├── .env.test
├── LICENSE.md
├── README.md
├── app.py
├── pytest-article.md
├── rdp_controller
│   ├── __init__.py
│   └── rdp_http_controller.py
├── requirements.txt
├── requirements_test.txt
└── tests
    ├── __init__.py
    ├── conftest.py
    ├── data
    │   ├── test_auth_fixture.json
    │   ├── test_esg_fixture.json
    │   ├── test_esg_invalid_fixture.json
    │   ├── test_search_fixture.json
    │   ├── test_search_invalid_fixture.json
    │   └── test_token_expire_fixture.json
    ├── pytest.ini
    ├── test_app.py
    └── test_rdp_http_controller.py
```

*Note*: The Docker and git related files are not shown in the project structure above. 

* app.py: The main console application.
* rdp_controller/rdp_http_controller.py: The main HTTP operations class. This is our focusing class for unit testing.
* tests/conftest.py: The root file that provides fixtures for all test cases in the ```tests``` folder.
* tests/pytest.ini: The pytest settings configuration file.
* tests/test_rdp_http_controller.py: The main test cases file that tests all rdp_http_controller.py class's methods. This is our focus test suite in this project.
* tests/test_app.py: The test suite class that tests some app.py methods.
* tests/data: The test suite resource files.

### <a id="pytest_set_Env"></a>Setting Unit Test Environment

Let’s start with the class that operates HTTP request-response messages with the RDP services.

It loads the test configurations such as the RDP APIs URLs from a ```.env.test``` environment variables file.

Let's start with setting up the test configurations, resources and environment variables. This project keeps the test configurations such as mock RDP credentials, API URLs in a ```${project root}/.env.test``` environment variables file. And then uses the [pytest-dotenv](https://pypi.org/project/pytest-dotenv/) plugin it to the ```os.environ``` variable without hardcoded path reference to the file.

To load a custom environment variables into pytest, we create a pytest configuration file named ```pytest.ini``` at the root of ```tests``` folder to specify where the ```env_var``` is.

``` ini
[pytest]
env_files = ../.env.test
```
*Note*: This plugin uses the [python-dotenv](https://pypi.org/project/python-dotenv/) under the hood, so the python-dotenv dependency will be installed too.

This ```os.environ``` environment variables and the ```RDPHTTPController``` class will be used in almost every test cases, so we set them as a *fixtures*. The fixture can be are data, class, preconditions states, context, or resources needed to run a test. Unlike the unittest framework,the [pytest fixture](https://docs.pytest.org/en/6.2.x/fixture.html) is in a function form that can be used in a modular manner.

The pytest fixtures are defined using the ```@pytest.fixture``` decorator. It can be defined in a test case (supports only in that test case) or in a ```conftest.py``` file (for sharing fixtures to all test cases in the same directory). This project uses the later case, so the content of a ```conftest.py``` file is as follows:

``` Python
# conftest.py

import pytest
import sys
import os

sys.path.append('..')

from rdp_controller import rdp_http_controller

# Supply test environment variables
@pytest.fixture(scope='class')
def supply_test_config():
    return os.environ

# Supply test RDPHTTPController class
@pytest.fixture(scope='class')
def supply_test_class():
    return rdp_http_controller.RDPHTTPController()
```
The ```supply_test_config``` fixture function is for the ```os.environ``` environment variable dictionary and the ```supply_test_class``` fixture function is for sharing the ```RDPHTTPController``` class among test cases. The test cases can use those fixture functions separately based on each test requirement. 

You may be noticed the ````scope='class'``` in the ```@pytest.fixture(scope='class')``` decorator, it means the fixture will be destroyed during teardown of the last test in the class.

That is all for the fixture preparation.

### <a id="pytest_rdp_authen"></a>Unit Testing RDP APIs Authentication with Pytest

Moving on to the next topic, the class that operates HTTP request-response messages with the RDP services. The ```rdp_controller/rdp_http_controller.py``` class uses the Requests library to send and receive data with the RDP HTTP REST APIs. The code for the RDP authentication is shown below.

``` Python
# rdp_controller/rdp_http_controller.py

import requests
import json

class RDPHTTPController():

    # Constructor Method
    def __init__(self):
        self.scope = 'trapi'
        self.client_secret = ''
        pass
    
    # Send HTTP Post request to get Access Token (Password Grant and Refresh Grant) from the RDP Auth Service
    def rdp_authentication(self, auth_url, username, password, client_id, old_refresh_token = None):

        if not auth_url or not username or not password or not client_id:
            raise TypeError('Received invalid (None or Empty) arguments')

        access_token = None
        refresh_token = None
        expires_in = 0
        if old_refresh_token is None: # For the Password Grant scenario
            payload=f'username={username}&password={password}&grant_type=password&scope={self.scope}&takeExclusiveSignOnControl=true&client_id={client_id}'
        else:  # For the Refresh Token scenario
            payload=f'username={username}&refresh_token={old_refresh_token}&grant_type=refresh_token&client_id={client_id}'

        # Send HTTP Request
        try:
            response = requests.post(auth_url, 
                headers = {'Content-Type':'application/x-www-form-urlencoded'}, 
                data = payload, 
                auth = (client_id, self.client_secret)
                )
        except Exception as exp:
            print(f'Caught exception: {exp}')
    

        if response.status_code == 200:  # HTTP Status 'OK'
            print('Authentication success')
            access_token = response.json()['access_token']
            refresh_token = response.json()['refresh_token']
            expires_in = int(response.json()['expires_in'])
        if response.status_code != 200:
            print(f'RDP authentication failure: {response.status_code} {response.reason}')
            print(f'Text: {response.text}')
            raise requests.exceptions.HTTPError(f'RDP authentication failure: {response.status_code} - {response.text} ', response = response )
        
        return access_token, refresh_token, expires_in
```

The ```rdp_authentication()``` method above just create the request message payload, and send it to the RDP Auth service as an HTTP Post request. The return values can be as follows
- If the authentication success, returns the access_token, refresh_token, and expires_in information to the caller.
- If the URL or credentials parameters are empty or none, raise the TypeError exception to the caller.
- If the authentication fails, raise the Requests' HTTPError exception to the caller with HTTP status response information.

Let’s leave the ```rdp_authentication()``` method there and continue with the test case. The basic test case scenario is to check if the ```rdp_authentication()``` method can handle a valid RDP login and empty parameters scenarios. 

The test class is ```tests\test_rdp_http_controller.py``` file (please noticed a *tests* prefixed). The basic test case code for the rdp_authentication() method is as follows:

``` Python
# test_rdp_http_controller.py

import pytest
import requests
import json

def test_rdp_login(supply_test_config,supply_test_class):
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

    # Calling RDPHTTPController rdp_authentication() method
    access_token, refresh_token, expires_in = app.rdp_authentication(auth_endpoint, username, password, client_id)
    assert access_token is not None
    assert refresh_token is not None
    assert expires_in > 0
```