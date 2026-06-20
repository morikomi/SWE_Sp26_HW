# Software Engineering - Spring 2026 - Homework

- Name Surname:
- ID:

### A Simple Web Application for Earth-Orbiting Satellites
This application allows you to run queries to the [TLE API](https://tle.ivanstanojevic.me/) to get the latest TLE information for a satellite/space object and calculate predicted position and velocity for the given time. There are intentionally placed code smells and missing parts throughout the application. Application-specific information can be found in this file. Homework instructions are provided in the Teams assignment. Do not modify any files that are not specified in the homework instructions.

The instructions in this file are intended for Linux systems, however, you may adapt them for use on Windows.

### Prerequisites
- Python 3.12 or higher

### Setup

1. Clone the repository or download and unzip the given zip file.
```
git clone <repository_link>
```

2. Change directory.
```
cd <repository_name>
```

3. Create a virtual environment and activate it. Following command will create a virtual environment under "venv" directory.
```
python -m venv venv
```
```
source venv/bin/activate
```

4. Install required packages. (Make sure that the virtual environment is activated.)
```
pip install -r requirements.txt
```

### How to run?
- Make sure that the virtual environment is activated.
- Run the following command. You can access the application on localhost:5000
```
flask run
```

### Testing
Tests are written using the unittest framework in the test_main.py and test_utils.py files, corresponding to main/views.py and main/utils.py. All test case method definitions must start with "test_" to be discovered. There are example test cases in both files with mocked requests.get function for the external API requests. You may use the "mocked_requests_get" function with "MockResponse" for any further test cases. You can check the [unittest](https://docs.python.org/3.12/library/unittest.html) and [coverage.py](https://coverage.readthedocs.io/en/7.8.2/index.html) documentation for more information.

- Run tests
```
python -m unittest discover
```
- Calculate test coverage
```
coverage run --branch -m unittest discover
```
- Get a coverage report
```
coverage report
```
- Get a HTML coverage report
```
coverage html
```
