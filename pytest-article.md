# Getting Start Unit Test with Pytest for an HTTP REST Python Application
- version: 1.0
- Last update: Feb 2023
- Environment: Windows
- Prerequisite: [Access to RDP credentials](#prerequisite)

Example Code Disclaimer:
ALL EXAMPLE CODE IS PROVIDED ON AN “AS IS” AND “AS AVAILABLE” BASIS FOR ILLUSTRATIVE PURPOSES ONLY. REFINITIV MAKES NO REPRESENTATIONS OR WARRANTIES OF ANY KIND, EXPRESS OR IMPLIED, AS TO THE OPERATION OF THE EXAMPLE CODE, OR THE INFORMATION, CONTENT, OR MATERIALS USED IN CONNECTION WITH THE EXAMPLE CODE. YOU EXPRESSLY AGREE THAT YOUR USE OF THE EXAMPLE CODE IS AT YOUR SOLE RISK.

## <a id="pytest_intro"></a>Introduction to Python Pytest framework

The [pytest](https://docs.pytest.org/en/7.2.x/) is one of the most popular all-purpose Python testing frameworks. This open-source framework lets developers/QAs write small, readable, and scalable test cases that are suitable for both simple function testing and complex applications. Comparing to the bulky class-based unit test framework like Python's built-in [unittest](https://docs.python.org/3.9/library/unittest.html), the pytest framework has an easier learning curve with more flexibility.

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
│   ├── __init__.py
│   └── rdp_http_controller.py
├── requirements.txt
├── requirements_test.txt
└── tests
    ├── __init__.py
    ├── conftest.py
    ├── data
    │   ├── test_esg_fixture.json
    │   ├── test_esg_invalid_fixture.json
    │   ├── test_search_fixture.json
    │   └── test_search_invalid_fixture.json
    ├── pytest.ini
    ├── test_app.py
    └── test_rdp_http_controller.py
```

*Note*: The Docker and git-related files are not shown in the project structure above. 

* app.py: The main console application.
* rdp_controller/rdp_http_controller.py: The main HTTP operations class. This is our focus class for unit testing.
* tests/conftest.py: The root file that provides fixtures for all test cases in the ```tests``` folder.
* tests/pytest.ini: The pytest settings configuration file.
* tests/test_rdp_http_controller.py: The main test cases file that tests all rdp_http_controller.py class's methods. This is our focus test suite in this project.
* tests/test_app.py: The test suite class that tests some app.py methods.
* tests/data: The test suite resource files.

### <a id="pytest_set_Env"></a>Setting Unit Test Environment

Let’s start with the class that operates HTTP request-response messages with the RDP services.

It loads the test configurations such as the RDP APIs URLs from a ```.env.test``` environment variables file.

Let's start with setting up the test configurations, resources, and environment variables. This project keeps the test configurations such as mock RDP credentials, and API URLs in a ```${project root}/.env.test``` environment variables file. And then uses the [pytest-dotenv](https://pypi.org/project/pytest-dotenv/) plugin to the ```os.environ``` variable without hardcoded path reference to the file.

To load a custom environment variables into pytest, we create a pytest configuration file named ```pytest.ini``` at the root of ```tests``` folder to specify where the ```env_var``` is and overriding any variables already defined in the process' environment.

``` ini
[pytest]
env_override_existing_values = 1
env_files = ../.env.test
```
*Note*: This plugin uses the [python-dotenv](https://pypi.org/project/python-dotenv/) under the hood, so the python-dotenv dependency will be installed too.

This ```os.environ``` environment variables and the ```RDPHTTPController``` class will be used in almost every test case, so we set them as a *fixtures*. The fixture can be are data, class, preconditions states, context, or resources needed to run a test. Unlike the unittest framework,the [pytest fixture](https://docs.pytest.org/en/6.2.x/fixture.html) is in a functional form that can be used in a modular manner.

The pytest fixtures are defined using the ```@pytest.fixture``` decorator. It can be defined in a test case (supports only in that test case) or in a ```conftest.py``` file (for sharing fixtures to all test cases in the same directory). This project uses the latter case, so the content of a ```conftest.py``` file is as follows:

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

You may be noticed the ````scope='class'``` in the ```@pytest.fixture(scope='class')``` decorator, which means the fixture will be destroyed during teardown of the last test in the class.

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
        except requests.exceptions.RequestException as exp:
            print(f'Caught exception: {exp}')
            return None, None, None

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

The test class is ```tests\test_rdp_http_controller.py``` file (please noticed a *tests* prefixed). The basic test case code for the ```rdp_authentication()``` method is as follows:

``` Python
# test_rdp_http_controller.py

import pytest
import requests
import json

def test_login_rdp_success(supply_test_config,supply_test_class):
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
    assert access_token is not None, "access token is None, success RDP Authentication returns invalid data"
    assert refresh_token is not None, "refresh token is None, success RDP Authentication returns invalid data"
    assert expires_in > 0, "expires_in is 0, success RDP Authentication returns invalid data"
```

The ```test_login_rdp_success()``` test case *requests* the ```supply_test_config``` and ```supply_test_class``` fixtures as function parameters. We get the RDPHTTPController object (as ```app``` function variable) and the RDP Auth URL endpoint string (as ```auth_endpoint``` function variable) from the *supply_test_config* and *supply_test_class* fixtures to use as the test case's resources. 

The ```test_login_rdp_success()``` is a test case for the successful RDP Authentication login scenario. It just sends the RDP Auth Service URL and RDP credentials to the ```RDPHTTPController.rdp_authentication()``` method and checks the response token information. Please noticed that a unit test just focuses on if the rdp_authentication() returns no empty/zero token information only. The token content validation would be in a system test (or later) phase.

``` Python
    assert access_token is not None, "access token is None, success RDP Authentication returns invalid data"
    assert refresh_token is not None, "refresh token is None, success RDP Authentication returns invalid data"
    assert expires_in > 0, "expires_in is 0, success RDP Authentication returns invalid data"
```

Please see more detail about the assertions in the test on the [pytest framework](https://docs.pytest.org/en/7.1.x/how-to/assert.html page.

What is about checking how the ```rpd_authentication()``` handles empty or none parameters? We create a new ```test_login_rdp_none_empty_params()``` test case to check if the method throws the TypeError exception and does not return token information to a caller as expected. The code is shown below.

``` Python
# test_rdp_http_controller.py

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
```

The ```test_login_rdp_none_empty_params()``` test case uses [pytest.raises()](https://docs.pytest.org/en/7.1.x/reference/reference.html#pytest.raises) as a context manager to check if the called method throws expected exception type. If the code block does not raise the expected exception (```TypeError``` in the test above), or no exception at all, the check will fail instead.

Please note that the ```pytest.raises()``` method returns the [ExceptionInfo](https://docs.pytest.org/en/7.1.x/reference/reference.html#pytest.ExceptionInfo) object which can be used to inspect the details of the captured exception via ```.type```, ```.value``` and ```.traceback``` attributes. This behavior is a bit different from [unittest assertRaises()](https://docs.python.org/3/library/unittest.html#unittest.TestCase.assertRaises) that returns the context manage that store the caught exception *as is*.

The example of a test runner result is shown below.

``` Bash
$>tests> pytest test_rdp_http_controller.py
====================== test session starts =============================
platform win32 -- Python 3.9.15, pytest-7.2.1, pluggy-1.0.0
rootdir: $>tests>, configfile: pytest.ini
plugins: dotenv-0.5.2
collected 2 items

test_rdp_http_controller.py ..                                            [100%] 

====================== 2 passed in 0.05s =============================
```

However, the test suite above makes HTTP requests to RDP APIs in every run. It is not a good idea to flood requests to external services every time developers run a test suite when they have updated the code or configurations. 

Unit test cases should be able to run independently without relying on external services or APIs. The external dependencies add uncontrolled factors (such as network connection, data reliability, etc) to unit test cases. Those components-to-components testing should be done in an integration testing phase. 

So, how can we unit test HTTP request method calls without sending any HTTP request messages to an actual server? Fortunately, developers can simulate the HTTP request and response messages with *a mock object*.

## <a id="unittest_mocking"></a>Mocking Python HTTP API call with Responses

A mock is a fake object that is constructed to look and act like real data within a testing environment. We can simulate the various scenario of the real data with a mock object, then use a mock library to trick the system into thinking that that mock is the real one. 

The purpose of mocking is to isolate and focus on the code being tested and not on the behavior or state of external dependencies. By mocking out external dependencies, developers can run tests as often without being affected by any unexpected changes or irregularities of those dependencies. Mocking also helps developers save time and computing resources if they have to test HTTP requests that fetch a lot of data.

I have demonstrated how to use the [Responses](https://github.com/getsentry/responses) mocking library in the [previous unittest framework project](https://github.com/Refinitiv-API-Samples/Article.RDP.Python.HTTP.UnitTest). I am using other popular Requests mocking library which is [requests-mock](https://requests-mock.readthedocs.io/en/latest/) with this pytest example.

### <a id="add_mock_test"></a>Adding a mock Object to the test case

So, I will start with a mock object for testing a successful RDP login case. Firstly, create a *supply_test_mock_json* fixture method with a dummy content of the RDP authentication success response message in a *contfest.py* file. 

``` Python
# conftest.py

# Supply test static JSON mock messages
@pytest.fixture(scope='class')
def supply_test_mock_json():
    #  Mock the RDP Auth Token success Response JSON
    valid_auth_json = {
        'access_token': 'access_token_mock1mock2mock3mock4mock5',
        'refresh_token': 'refresh_token_mock1mock2mock3mock4mock5',
        'expires_in': '600',
        'scope': 'test1 test2 test3 test4 test5',
        'token_type': 'Bearer'
    }

    return {
        'valid_auth_json': valid_auth_json
    }
```

And then we can modify ```test_login_rdp_success``` test case and other test cases to request this ```supply_test_mock_json``` fixture as a function argument. 

The requests-mock library provides an external fixture registered with pytest for developers. Developers can simply just specifying ```requests-mock``` as a function parameter without the need to import ```requests-mock``` library in the test files (you still need to install [the library](https://pypi.org/project/requests-mock/)). Once the ```requests-mock``` is loaded to a test case, developers can specify the endpoint URL, HTTP method, status response, response message, etc of that request via a ```requests_mock.post()``` and ```requests_mock.get()``` methods.

Example:

``` Python
# test_rdp_http_controller.py

def test_login_rdp_success(supply_test_config,supply_test_class, supply_test_mock_json, requests_mock):
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
        json = supply_test_mock_json['valid_auth_json'], 
        status_code = 200,
        headers = {'Content-Type':'application/json'}
        )

    # Calling RDPHTTPController rdp_authentication() method
    access_token, refresh_token, expires_in = app.rdp_authentication(auth_endpoint, username, password, client_id)
    # Assertions
    ...
```
The code above set a Responses mock object with the *https://api.refinitiv.com/auth/oauth2/v1/token* URL and HTTP *POST* method. The requests-mock library then returns a ```valid_auth_json``` JSON message with HTTP status *200* and Content-Type *application/json* from the ```supply_test_mock_json``` fixture to the application for all HTTP *POST* request messages to *https://api.refinitiv.com/auth/oauth2/v1/token* URL without any network operations between the machine and the actual RDP endpoint.

### <a id="unittest_rdp_authen_fail"></a>Testing Invalid RDP Client ID Authentication Request-Response

This mock object is also useful for testing false cases such as invalid login too.  The ```test_login_rdp_invalid()``` method is a test case for the RDP Authentication login failure scenario. I am starting by add a new ```invalid_clientid_auth_json``` dummy content of the RDP invalid ClientID log response to a *supply_test_mock_json* fixture method.

``` Python
# conftest.py

# Supply test static JSON mock messages
@pytest.fixture(scope='class')
def supply_test_mock_json():
    #  Mock the RDP Auth Token success Response JSON
    valid_auth_json = {
        ...
    }
    ...
    invalid_clientid_auth_json = {
        'error': 'invalid_client',
        'error_description': 'Invalid Application Credential.',
    }

    return {
        'valid_auth_json': valid_auth_json,
        'invalid_clientid_auth_json': invalid_clientid_auth_json
    }
```

And then we set a Responses mock object for the *https://api.refinitiv.com/auth/oauth2/v1/token* URL and HTTP *POST* method with the expected error response message and status (401 - Unauthorized) that is loaded from this ```supply_test_mock_json``` fixture. 

``` Python
# test_rdp_http_controller.py

def test_login_rdp_invalid_clientID(supply_test_config,supply_test_class, supply_test_mock_json, requests_mock):
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
        json = supply_test_mock_json['invalid_clientid_auth_json'], 
        status_code = 401,
        headers = {'Content-Type':'application/json'}
        )


    username = 'wrong_user1'
    password = 'wrong_password1'
    client_id = 'XXXXX'
    access_token = None
    refresh_token = None
    expires_in = 0
    ...
```
Once the ```rdp_authentication()``` method is called, the test case verifies if the method raises the ```requests.exceptions.HTTPError``` exception with the expected error message and status. The test case also makes assertions to check if the method does not return token information to a caller.

``` Python
# test_rdp_http_controller.py

def test_login_rdp_invalid_clientID(supply_test_config,supply_test_class, supply_test_mock_json, requests_mock):
    ....

    with pytest.raises(requests.exceptions.HTTPError) as excinfo:
        access_token, refresh_token, expires_in = app.rdp_authentication(auth_endpoint, username, password, client_id)
    
    assert access_token is None, "Invalid clientID returns Access Token"
    assert refresh_token is None, "Invalid clientID returns Refresh Token"
    assert expires_in == 0, "Invalid Login returns expires_in"
    assert '401' in str(excinfo.value), "Invalid clientID returns wrong HTTP Status Code"
    assert 'RDP authentication failure' in str(excinfo.value),"Invalid Login returns wrong Exception description"

    json_error = json.loads(str(excinfo.value).split('-')[1])
    assert type(json_error) is dict, "Invalid Login returns wrong Exception detail type"
```

With mocking, a test case never needs to send actual request messages to the RDP APIs, so we can test more scenarios for other RDP services too.

## <a id="rdp_get_data"></a>Unit Testing for RDP APIs Data Request

That brings us to requesting the RDP APIs data. All subsequent REST API calls use the Access Token via the *Authorization* HTTP request message header as shown below to get the data. 
- Header: 
    * Authorization = ```Bearer <RDP Access Token>```

Please notice *the space* between the ```Bearer``` and ```RDP Access Token``` values.

The application then creates a request message in a JSON message format or URL query parameter based on the interested service and sends it as an HTTP request message to the Service Endpoint. Developers can get RDP APIs the Service Endpoint, HTTP operations, and parameters from Refinitiv Data Platform's [API Playground page](https://api.refinitiv.com/) - which is an interactive documentation site developers can access once they have a valid Refinitiv Data Platform account.

The example console application consumes content from the following RDP Services:
- ESG Service ```/data/environmental-social-governance/<version>/views/scores-full``` endpoint that provides full coverage of Refinitiv's proprietary ESG Scores with full history for consumers.
- Discovery Search Explore Service ```/discover/search/<version>/explore``` endpoint that explore Refinitiv data based on searching options.

However, this development article covers the Search Explore Service test cases only. The ESG Service's test cases have the same test logic as the Discovery Search Explore's test cases.

## <a id="pytest_rdp_search"></a>Unit Testing HTTP Request Source Code for The RDP Discovery Search Explore Service

Now let me turn to test the Discovery Search Explore service endpoint. The code in the ```rdp_controller/rdp_http_controller.py``` class for requesting the search result data is shown below.

``` Python
# rdp_controller/rdp_http_controller.py

# Send HTTP Post request to the RDP Search Explore Service
def rdp_request_search_explore(self, search_url, access_token, payload):

    if not search_url or not access_token or not payload:
        raise TypeError('Received invalid (None or Empty) arguments')

    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }

    try:
        response = requests.post(search_url, headers = headers, data = json.dumps(payload))
    except requests.exceptions.RequestException as exp:
        print(f'Caught exception: {exp}')
        return None
        
    if response.status_code == 200:  # HTTP Status 'OK'
        print('Receive Search Explore Data from RDP APIs')
    else:
        print(f'RDP APIs: Search Explore request failure: {response.status_code} {response.reason}')
        print(f'Text: {response.text}')
        raise requests.exceptions.HTTPError(f'Search Explore request failure: {response.status_code} - {response.text} ', response = response )

    return response.json()
```

The ```rdp_request_search_explore()``` method above just create the request message payload, and send it to the RDP Search Explore service as HTTP POST request with the Requests ```requests.post()``` method. The return values can be as follows
- If the request success (HTTP status is 200), returns the response data in JSON message format.
- If the URL or access token, or universe values are empty or none, raise the TypeError exception to the caller.
- If the request fails, raise the Requests' HTTPError exception to the caller with HTTP status response information.

### <a id="unittest_rdp_esg_success"></a>Testing a valid RDP Search Explore Request-Response

The first test case is the request success scenario. I will begin by creating a test-content file with a valid Search Explore response message. A file is *rdp_test_esg_fixture.json* in a *tests/data* folder.

``` JSON
{
  "links": {
    "count": 5
  },
  "variability": "variable",
  "universe": [
    {
      "Instrument": "TEST.RIC",
      "Company Common Name": "TEST ESG Data",
      "Organization PermID": "XXXXXXXXXX",
      "Reporting Currency": "USD"
    }
  ],
  "data": [
    [
      "TEST.RIC",
      "2021-12-31",
      99.9999999999999,
      99.9999999999999,
      ...
    ],
   ...
  ],
  ...
  ,
  "headers": [
    ....
    {
      "name": "TEST 1",
      "title": "ESG Score",
      "type": "number",
      "decimalChar": ".",
      "description": "TEST description"
    }...
  ]
}
```

We are not going to load this data into *conftest.py* fixture because only one test case uses this dummy data. We are using it as a test data resource with the [pytest-datadir](https://pypi.org/project/pytest-datadir/) library. The pytest-datadir will copy the original file to a temporary folder, so changing the file contents won't change the original data file and the test case can use it in the test assertions.

However, the RDP Search request message will be reused by multiple test cases as a based line for each test's request message payload, so we add it as a new ```search_explore_payload``` content to a *supply_test_mock_json* fixture method as follows.

``` Python
# conftest.py

@pytest.fixture(scope='class')
def supply_test_mock_json():
    #  Mock the RDP Auth Token success Response JSON
    ...
    search_explore_payload = {
        'View': 'Entities',
        'Filter': '',
        'Select': 'IssuerCommonName,DocumentTitle,RCSExchangeCountryLeaf,IssueISIN,ExchangeName,ExchangeCode,SearchAllCategoryv3,RCSTRBC2012Leaf',
    }

    return {
        'valid_auth_json': valid_auth_json,
        'invalid_clientid_auth_json': invalid_clientid_auth_json,
        'search_explore_payload': search_explore_payload
    }

```

Next, create the ```test_request_search_explore()``` method in the test_rdp_http_controller.py file to test the easiest test case, the successful ESG data request-response scenario.  
 
``` Python
# test_rdp_http_controller.py

def test_request_search_explore(supply_test_config,supply_test_class, supply_test_mock_json,shared_datadir, requests_mock):
    """
    Test that it can get RIC's metadata via the RDP Search Explore Service
    """
    search_endpoint = supply_test_config['RDP_BASE_URL'] + supply_test_config['RDP_SEARCH_EXPLORE_URL']
    app = supply_test_class
    universe = 'TEST.RIC'
  
    payload = supply_test_mock_json['search_explore_payload']
    payload['Filter'] =f'RIC eq \'{universe}\''

    # Mock RDP ESG View Score valid response JSON
    contents = (shared_datadir / 'test_search_fixture.json').read_text()
    valid_response = json.loads(contents)

    requests_mock.post(
        url= search_endpoint, 
        json = valid_response, 
        status_code = 200,
        headers = {'Content-Type':'application/json'}
        )
    
    ...
```
The code above does the following tasks:
- Injects the test data location via a ```shared_datadir``` function parameter to the test case
- Read the ```test_search_fixture.json``` test data content from a ```shared_datadir``` folder to a ```valid_response``` variable
- Create a request message based on the ```search_explore_payload``` message for the ```supply_test_mock_json``` fixture
- Mock a request to the RDP ```https://api.refinitiv.com/discovery/search/v1/explore``` endpoint URL and ```valid_response``` variable.

When the Requests library receives the HTTP POST request for that URL, it returns a mock Search result JSON object with HTTP Status *200* and Content-Type *application/json* to the application. The ```test_request_search_explore()``` method then verifies if the response data is in JSON/[Dictionaries](https://docs.python.org/3.9/tutorial/datastructures.html#dictionaries) type, and checks if the message contains the basic fields. 

``` Python
# test_rdp_http_controller.py

def test_request_search_explore(supply_test_config,supply_test_class, supply_test_mock_json,shared_datadir, requests_mock):
    """
    Test that it can get RIC's metadata via the RDP Search Explore Service
    """
    ...
    # Calling RDPHTTPController rdp_request_esg() method
    response = app.rdp_request_search_explore(search_endpoint, supply_test_mock_json['valid_auth_json']['access_token'], payload)

    assert type(response) is dict, 'Search request returns wrong data type'
    assert 'Total' in response
    assert 'Hits' in response
```

### <a id="pytest_rdp_search_expire"></a>Testing Requesting RDP Search service with an expired token

That brings us to one of the most common RDP APIs failure scenarios, applications request data from RDP with an expired access token. 
The ```test_request_search_explore_token_expire()``` method is the one for testing this case with the RDP ESG Service. 

The first step is to add a mock token expired message ```token_expire_json``` to a ```supply_test_mock_json``` fixture. We add this to a fixture because we can reuse this token expired message in all RDP data services test cases as well.

``` Python
# conftest.py

@pytest.fixture(scope='class')
def supply_test_mock_json():
    ...
    # Mock the RDP Auth Token Expire Response JSON
    token_expire_json = {
        'error': {
            'id': 'XXXXXXXXXX',
            'code': '401',
            'message': 'token expired',
            'status': 'Unauthorized'
        }
    }

    ...
    return {
        'valid_auth_json': valid_auth_json,
        'invalid_clientid_auth_json': invalid_clientid_auth_json,
        'token_expire_json': token_expire_json,
        'search_explore_payload': search_explore_payload
    }
```

The token expires error message is sent from the RDP services to applications with HTTP error status (401 - **As of Feb 2023**), the ```test_request_search_explore_token_expire()``` method simulates the token expire error message and HTTP 401 status with a mock object as follows.

``` Python
# test_rdp_http_controller.py

def test_request_search_explore_token_expire(supply_test_config,supply_test_class, supply_test_mock_json, requests_mock):
    """
    Test that it can handle token expiration requests
    """
    search_endpoint = supply_test_config['RDP_BASE_URL'] + supply_test_config['RDP_SEARCH_EXPLORE_URL']
    app = supply_test_class
    universe = 'TEST.RIC'
    payload = supply_test_mock_json['search_explore_payload']
    payload['Filter'] =f'RIC eq \'{universe}\''

    requests_mock.post(
        url= search_endpoint, 
        json = supply_test_mock_json['token_expire_json'], 
        status_code = 401,
        headers = {'Content-Type':'application/json'}
        )
    ...

```

Next, this test case verifies if the ```rdp_request_search_explore()``` method raises the ```requests.exceptions.HTTPError``` exception with the expected token expired error message and status.

``` Python
# test_rdp_http_controller.py

def test_request_search_explore_token_expire(supply_test_config,supply_test_class, supply_test_mock_json, requests_mock):
    """
    Test that it can handle token expiration requests
    """
    ...
    # Calling RDPHTTPController rdp_request_search_explore() method
    with pytest.raises(requests.exceptions.HTTPError) as excinfo:
        response = app.rdp_request_search_explore(search_endpoint, supply_test_mock_json['valid_auth_json']['access_token'], payload)

    # verifying basic response

    print('Exception = ' + str(excinfo.value))
    assert '401' in str(excinfo.value), 'Access Token Expire returns wrong HTTP Status Code'
    assert 'Unauthorized' in str(excinfo.value), 'Access Token Expire returns wrong error message'

    json_error = json.loads(str(excinfo.value).split('401 -')[1])
    assert type(json_error) is dict, 'Access Token Expire returns wrong data type'
    assert 'error' in json_error, 'Access Token Expire returns wrong JSON error response'
    assert 'message' in json_error['error'], 'Access Token Expire returns wrong JSON error response'
    assert 'status' in json_error['error'], 'Access Token Expire returns wrong JSON error response'

```

The other common RDP APIs failure scenario is the application sends the request message to RDP without the access token in the HTTP request header. However, the *access token* is one of the ```rdp_request_search_explore()``` method required parameters. If the access token is not presented (None or Empty), the method raises the TypeError exception and does not send an HTTP request message to the RDP. The ```test_request_search_explore_none_empty()``` method is the one that covers this test case. There is also a ```test_request_search_explore_invalid_json()``` test case method in the file that demonstrates how to test invalid JSON request message scenario.

That covers the Discovery Search Explore service test cases. If you are interested in RDP ESG service test cases, please check the ```test_request_esg_xxx``` methods which have the same testing and mocking logic as all previous cases that I have mentions above.

### <a id="pytest_mark"></a>Bonus: Pytest Markers

Now we come to one of the most unique features of pytest, the *markers*. The pytest framework supports test case metadata setting known as *markers* (```pytest.mark```). The markers are used by plugins, and are commonly used to run or skip tests with specific marker. Here are some of the builtin markers:
- *skip*: always skip a test function
- *skipif* - skip a test function if a certain condition is met
- *xfail* - produce an “expected failure” outcome if a certain condition is met
- *parametrize* - perform multiple calls to the same test function.

The framework also supports [custom markers](https://docs.pytest.org/en/7.1.x/example/markers.html#working-with-custom-markers) to match the project's requirement too. Once the custom markers has been set, developers can run ```pytest -m <mark>``` for run test specific tests.

To create custom markers, the first thing you need to do is define your markers for grouping test cases in the ```pytest.ini``` configuration file as follows:

``` INI
[pytest]
markers = 
    test_login: marks RDP login methods test
    test_esg: marks RDP ESG methods test
    test_search: marks RDP Search methods test
    test_valid: marks valid methods call test
    empty_case: marks for None/Empty param methods call test
env_override_existing_values = 1
env_files = ../.env.test
```
Then, add the marker to test methods in ```test_rdp_http_controller.py``` file with ```@pytest.mark.<custom mark>``` decorator. Please see the example modified code below.

``` Python
# test_rdp_http_controller.py

@pytest.mark.test_valid
@pytest.mark.test_login
def test_login_rdp_success(supply_test_config,supply_test_class, supply_test_mock_json, requests_mock):
    """
    Test that it can log in to the RDP Auth Service
    """
    ...

@pytest.mark.test_login
def test_login_rdp_invalid_clientID(supply_test_config,supply_test_class, supply_test_mock_json, requests_mock):
    """
    Test that it can handle some invalid credentials
    """
    ...

@pytest.mark.test_valid
@pytest.mark.test_esg
def test_request_esg(supply_test_config,supply_test_class, supply_test_mock_json,shared_datadir, requests_mock):
    """
    Test that it can request ESG Data
    """
    ...

@pytest.mark.empty_case
@pytest.mark.test_search
def test_request_search_explore_none_empty(supply_test_class,supply_test_mock_json):
    """
    Test that the Search Explore function can handle none/empty input
    """
    ...
```

Please be noticed that you can set multiple markers to each test method. 

In order to run specific markers, you can run pytest with ```-m <mark>``` command as follows:

Example: Run only success scenarios test cases:

``` Bash
(rdp_pytest) C:\rdp_python_pytest\test>pytest -m test_valid -v
=============================================== test session starts ================================================
platform win32 -- Python 3.9.15, pytest-7.2.1, pluggy-1.0.0 -- C:\...\Miniconda3\envs\rdp_pytest\python.exe
cachedir: .pytest_cache
rootdir: C:\rdp_python_pytest\tests, configfile: pytest.ini
plugins: datadir-1.4.1, dotenv-0.5.2, requests-mock-1.10.0
collected 16 items / 12 deselected / 4 selected

test_rdp_http_controller.py::test_login_rdp_su                                                                 [ 25%] 
test_rdp_http_controller.py::test_login_rdp_refreshtoken PASSED                                                [ 50%] 
test_rdp_http_controller.py::test_request_esg PASSED                                                           [ 75%]
test_rdp_http_controller.py::test_request_search_explore PASSED                                                [100%]

=============================================== 4 passed, 12 deselected in 0.18s ================================================ 
```
You can select multiple markers with ```and``` , ```or```, ```not``` operators to combine multiple markers. The following example shows how to specify only RDP ESG service unsuccess test cases.

``` Bash
(rdp_pytest) C:\rdp_python_pytest\test>pytest -m "not test_valid and test_esg" -v 
=============================================== test session starts ================================================
platform win32 -- Python 3.9.15, pytest-7.2.1, pluggy-1.0.0 -- C:\...\Miniconda3\envs\rdp_pytest\python.exe
cachedir: .pytest_cache
rootdir: C:\rdp_python_pytest\tests, configfile: pytest.ini
plugins: datadir-1.4.1, dotenv-0.5.2, requests-mock-1.10.0
collected 16 items / 13 deselected / 3 selected

test_rdp_http_controller.py::test_request_esg_token_expire PASSED                                            [ 33%]
test_rdp_http_controller.py::test_request_esg_invalid_ric PASSED                                             [ 66%]
test_rdp_http_controller.py::test_request_esg_none_empty PASSED                                              [100%] 

=============================================== 3 passed, 13 deselected in 0.13s ================================================
```
Please see more detail about pytest markers and custom markers from the following resources:
- [pytest document: How to mark test functions with attributes](https://docs.pytest.org/en/7.1.x/how-to/mark.html#how-to-mark-test-functions-with-attributes)
- [pytest document: Working with custom markers](https://docs.pytest.org/en/7.1.x/example/markers.html#working-with-custom-markers)
- [pytest document: Raising errors on unknown marks](https://docs.pytest.org/en/stable/how-to/mark.html#raising-errors-on-unknown-marks)

That’s all I have to say about unit testing the Python HTTP code with Requests and Responses libraries.

## <a id="how_to_run"></a>How to run the example test suite

Please see how to run the project test suit in the [README.md](README.md#how_to_run) file.
