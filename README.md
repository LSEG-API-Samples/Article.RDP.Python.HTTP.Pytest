# Getting Start Unit Test with Pytest for an HTTP REST Python Application
- version: Draft
- Last update: Feb 2023
- Environment: Windows
- Prerequisite: [Access to RDP credentials](#prerequisite)

Example Code Disclaimer:
ALL EXAMPLE CODE IS PROVIDED ON AN “AS IS” AND “AS AVAILABLE” BASIS FOR ILLUSTRATIVE PURPOSES ONLY. REFINITIV MAKES NO REPRESENTATIONS OR WARRANTIES OF ANY KIND, EXPRESS OR IMPLIED, AS TO THE OPERATION OF THE EXAMPLE CODE, OR THE INFORMATION, CONTENT, OR MATERIALS USED IN CONNECTION WITH THE EXAMPLE CODE. YOU EXPRESSLY AGREE THAT YOUR USE OF THE EXAMPLE CODE IS AT YOUR SOLE RISK.

## <a id="intro"></a>Introduction

Today, applications are bigger and more complex. A few changes to the source code to add more features or fix bugs can make unexpected behavior in an application. Developers cannot just wait for the test result from the QA team anymore. They need to do unit testing regularly as an integral part of the development process. 

Unit testing is a software testing method that helps developers verify if any changes break the code. Unit testing significantly improves code quality, saves time to find software bugs in an early stage of the development lifecycle, and improves deployment velocity. Unit testing is currently the main process of a modern Agile software development practice such as CI/CD (Continuous Integration/Continuous Delivery), TDD (Test-driven development), etc.

Modern applications also need to connect to other services like APIs, databases, data storage, etc. The unit testing needs to cover those modules too. This example project shows how to run unit test cases for a [Python](https://www.python.org/) application that performs HTTP REST operations which is the most basic task of today's application functionality. With unit testing, developers can verify if their code can connect and consume content via HTTP REST API in any code updates. 

The example project is a part two of the [Getting Start Unit Test for an HTTP REST Application with Python](https://github.com/Refinitiv-API-Samples/Article.RDP.Python.HTTP.UnitTest) project. The first project uses the Python built-in [unittest](https://docs.python.org/3.9/library/unittest.html) as a test framework. This project uses more popular [pytest](https://docs.pytest.org/en/7.2.x/) as a test framework. The target application source code for testing remain the same, it uses a de-facto [Requests](https://requests.readthedocs.io/en/latest/) library to connect to the [Refinitiv Data Platform (RDP) APIs](https://developers.refinitiv.com/en/api-catalog/refinitiv-data-platform/refinitiv-data-platform-apis) as the example HTTP REST APIs.

**Note**:
This demo project is not cover all test cases for the HTTP operations and all RDP APIs services. It aims to give the readers an idea about how to unit test an application that makes an HTTP connection with Python only. 

## Unit Testing Overview

[Unit testing](https://en.wikipedia.org/wiki/Unit_testing) is the smallest test that focuses on checking that a single part of the application operates correctly. It breaks an application into the smallest, isolated, testable component called *units*, and then tests them individually. The unit is mostly a function or method call or procedure in the application source code. Developers and QA can test each unit by sending any data into that unit and see if it functions as intended. 

A unit test helps developers to isolate what is broken in their application easier and faster than testing an entire system as a whole. It is the first level of testing done during the development process before integration testing. It is mostly done by the developers automated or manually to verify their code.

![figure-1](images/01_unittest.png "Unit Testing Life Cycle")


You can find more detail about the unit test concept from the following resources:
- [Python Guide: Testing Your Code](https://docs.python-guide.org/writing/tests/) article.
- [How and when to use Unit Testing properly](https://softwareengineering.stackexchange.com/questions/89064/how-and-when-to-use-unit-testing-properly) post.

## Introduction to Pytest framework

TBD

## <a id="whatis_rdp"></a>What is Refinitiv Data Platform (RDP) APIs?

The [Refinitiv Data Platform (RDP) APIs](https://developers.refinitiv.com/en/api-catalog/refinitiv-data-platform/refinitiv-data-platform-apis) provide various Refinitiv data and content for developers via easy-to-use Web-based API.

RDP APIs give developers seamless and holistic access to all of the Refinitiv content such as Environmental Social and Governance (ESG), News, Research, etc, and commingled with their content, enriching, integrating, and distributing the data through a single interface, delivered wherever they need it.  The RDP APIs delivery mechanisms are the following:
* Request - Response: RESTful web service (HTTP GET, POST, PUT or DELETE) 
* Alert: delivery is a mechanism to receive asynchronous updates (alerts) to a subscription. 
* Bulks:  deliver substantial payloads, like the end-of-day pricing data for the whole venue. 
* Streaming: deliver real-time delivery of messages.

This example project is focusing on the Request-Response: RESTful web service delivery method only.  

![figure-2](images/02_rdp.png "Refinitiv Data Platform")

For more detail regarding the Refinitiv Data Platform, please see the following APIs resources: 
- [Quick Start](https://developers.refinitiv.com/en/api-catalog/refinitiv-data-platform/refinitiv-data-platform-apis/quick-start) page.
- [Tutorials](https://developers.refinitiv.com/en/api-catalog/refinitiv-data-platform/refinitiv-data-platform-apis/tutorials) page.

## <a id="prerequisite"></a>Prerequisite

This demo project requires the following dependencies.

1. RDP Access credentials.
2. Python [Anaconda](https://www.anaconda.com/distribution/) or [MiniConda](https://docs.conda.io/en/latest/miniconda.html) distribution/package manager.
3. Internet connection.

Please contact your Refinitiv representative to help you to access the RDP account and services. You can find more detail regarding the RDP access credentials set up from the lease see the *Getting Started for User ID* section of the [Getting Start with Refinitiv Data Platform](https://developers.refinitiv.com/en/article-catalog/article/getting-start-with-refinitiv-data-platform) article.

## <a id="how_to_run"></a>How to run the example test suite

The first step is to unzip or download the example project folder into a directory of your choice, then set up Python or Docker environments based on your preference.

### <a id="python_example_run"></a>Run example test suite in a console

1. Open Anaconda Prompt and go to the project's folder.
2. Run the following command in the Anaconda Prompt application to create a Conda environment named *rdp_pytest* for the project.
    ``` bash
    (base) $>conda create --name rdp_pytest python=3.9
    ```
3. Once the environment is created, activate a Conda *rdp_pytest* environment with this command in Anaconda Prompt.
    ``` bash
    (base) $>conda activate rdp_pytest
    ```
4. Run the following command to the dependencies in the *rdp_pytest* environment 
    ``` bash
    (rdp_pytest) $>pip install -r requirements.txt
    ```
5. Once the dependencies installation process is success, Go to the project's *tests* folder, then run the following command to run the ```test_rdp_http_controller.py``` test suite.
    ``` bash
    (http_unittest) $>tests\pytest .
    ```
### <a id="docker_example_run"></a>Run example test suite in Docker

1. Start Docker
2. Open a console, then go to the *project root* and run the following command to build a Docker image.
    ```
    $> docker build . -t python_pytest
    ```
3. Run a Docker container with the following command: 
    ```
    $> docker run -it --name python_pytest python_pytest
    ```
    You can pass pytest arguments too. The following example runs only test cases for the RDP Login API only.

    ```
    $> docker run -it --name python_pytest python_pytest -m test_login -v
    ```
4. To stop and delete a Docker container, press ``` Ctrl+C``` (or run ```docker stop python_pytest```) then run the following command:
    ```
    $> docker rm python_pytest
    ```
5. To delete a Docker image, run the ```docker rmi python_pytest``` after a container is removed.

Example Result:
``` Bash
(rdp_pytest) C:\rdp_python_pytest\test>pytest .
=============================================== test session starts ================================================
platform win32 -- Python 3.9.15, pytest-7.2.1, pluggy-1.0.0
rootdir: C:\rdp_python_pytest\test    
plugins: requests-mock-1.10.0
collected 6 items

test_rdp_http_controller.py ......                                                                            [100%]

================================================ 6 passed in 0.08s =================================================
```

## <a id="references"></a>References

That brings me to the end of my unit test example project. For further details, please check out the following resources:
* [Refinitiv Data Platform APIs page](https://developers.refinitiv.com/en/api-catalog/refinitiv-data-platform/refinitiv-data-platform-apis) on the [Refinitiv Developer Community](https://developers.refinitiv.com/) website.
* [Refinitiv Data Platform APIs Playground page](https://api.refinitiv.com).
* [Refinitiv Data Platform APIs: Introduction to the Request-Response API](https://developers.refinitiv.com/en/api-catalog/refinitiv-data-platform/refinitiv-data-platform-apis/tutorials#introduction-to-the-request-response-api).
* [Refinitiv Data Platform APIs: Authorization - All about tokens](https://developers.refinitiv.com/en/api-catalog/refinitiv-data-platform/refinitiv-data-platform-apis/tutorials#authorization-all-about-tokens).
* [Limitations and Guidelines for the RDP Authentication Service](https://developers.refinitiv.com/en/article-catalog/article/limitations-and-guidelines-for-the-rdp-authentication-service) article.
* [Getting Started with Refinitiv Data Platform](https://developers.refinitiv.com/en/article-catalog/article/getting-start-with-refinitiv-data-platform) article.
* [Python pytest framework official page](https://docs.pytest.org/en/7.2.x/).
* [Python requests-mock library page](https://requests-mock.readthedocs.io/en/latest/).


For any questions related to Refinitiv Data Platform APIs, please use the [RDP APIs Forum](https://community.developers.refinitiv.com/spaces/231/index.html) on the [Developers Community Q&A page](https://community.developers.refinitiv.com/).

## Developers Articles

TBD.