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
